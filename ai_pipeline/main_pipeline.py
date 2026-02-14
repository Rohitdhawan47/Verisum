# --- Import custom modules ---
from .model_loader import load_summarizer, load_keybert
from .parser import parse_page # Only import parser

# --- Import standard libraries ---
import fitz # PyMuPDF
import torch
import re

# --- LOAD MODELS ---
SUMMARIZER, SUM_TOKENIZER = load_summarizer()
KEY_MODEL = load_keybert()

def clean_text(text: str) -> str:
    """
    Cleans raw extracted text.
    """
    # 1. Fix ligatures
    text = text.replace("ﬁ", "fi").replace("ﬂ", "fl").replace("ﬀ", "ff")
    
    # 2. Remove lines that look like equation remnants
    lines = text.split('\n')
    clean_lines = []
    for line in lines:
        if '⊕' in line or '...' in line: continue
        if '=' in line and len(line) < 50: continue 
        clean_lines.append(line)
    text = "\n".join(clean_lines)

    # 3. Remove math placeholders and normalize
    text = re.sub(r'\(\d+\)\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'\b\w*[\^_{}]\w*\b', '[MATH]', text)
    # We DO NOT normalize all whitespace to a single space here anymore.
    # We need to keep '\n' to identify paragraphs.
    text = re.sub(r'[ \t]+', ' ', text).strip()
    
    return text

def chunk_text(text: str, chunk_size: int = 200) -> list[str]:
    """
    Splits text into chunks of approximately 'chunk_size' words.
    FIX: Merges small "orphan" chunks into the previous chunk 
    to prevent fragmentation and hallucinations.
    """
    words = text.split()
    chunks = []
    current_chunk = []
    current_count = 0
    
    for word in words:
        current_chunk.append(word)
        current_count += 1
        
        # Check for chunk boundary (sentence ending)
        if current_count >= chunk_size and word.endswith(('.', '!', '?')):
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_count = 0
            
    # --- THE FIX: HANDLE LEFTOVERS ---
    if current_chunk:
        leftover_text = " ".join(current_chunk)
        
        # If the leftover is tiny (< 50 words) and we already have chunks,
        # MERGE it into the previous chunk instead of making a new one.
        if len(current_chunk) < 50 and chunks:
            chunks[-1] += " " + leftover_text
        else:
            chunks.append(leftover_text)
        
    return chunks

def batch_generate_summary(text_list: list[str], batch_size: int = 4) -> list[str]:
    """
    Summarizes a list of text chunks in batches.
    Optimized for COMPLETENESS and CONCISENESS.
    """
    summaries = []
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    for i in range(0, len(text_list), batch_size):
        batch_texts = text_list[i : i + batch_size]
        
        # Tokenize
        inputs = SUM_TOKENIZER(batch_texts, 
                               return_tensors="pt", 
                               padding=True, 
                               truncation=True, 
                               max_length=4096).to(device)
        
        # Generate with CONCISE settings
        with torch.no_grad():
            summary_ids = SUMMARIZER.generate(
                inputs["input_ids"], 
                num_beams=4,             
                min_length=20,           # Lowered to allow concise summaries
                max_length=512,          # Increased to prevent cut-offs
                length_penalty=0.8,      # Changed from 2.0 to 0.8 (Encourages brevity)
                no_repeat_ngram_size=3,  
                early_stopping=True
            )
        
        # Decode
        batch_summaries = SUM_TOKENIZER.batch_decode(
            summary_ids, 
            skip_special_tokens=True, 
            clean_up_tokenization_spaces=True
        )
        
        summaries.extend(batch_summaries)
        
    return summaries

def process_page_pipeline(pdf_file_path: str, page_num: int):
    """
    Runs the pipeline: Parse -> Clean -> Smart Chunk -> Smart Summarize
    """
    
    # --- 1. PARSE ---
    try:
        doc = fitz.open(pdf_file_path)
        page = doc.load_page(page_num)
    except Exception as e:
        print(f"Error opening PDF: {e}")
        return [], [], ""
        
    raw_text = parse_page(page)
    
    # --- 2. CLEAN ---
    cleaned_text = clean_text(raw_text)
    
    if not cleaned_text or len(cleaned_text) < 50:
        return [], [], raw_text

    # --- 3. SMART CHUNK ---
    # Use new paragraph-based logic
    text_chunks = chunk_text(cleaned_text)
    
    if not text_chunks:
        return [], [], raw_text

    # --- 4. PREPARE FOR HYBRID SUMMARY ---
    # Separate short paragraphs (copy) from long paragraphs (summarize)
    chunks_to_summarize = []
    indices_to_summarize = []
    final_summaries = [""] * len(text_chunks)
    
    for i, chunk in enumerate(text_chunks):
        word_count = len(chunk.split())
        
        # If paragraph is short (<50 words), don't summarize it. Just copy it.
        if word_count < 50:
            final_summaries[i] = chunk 
        else:
            chunks_to_summarize.append(chunk)
            indices_to_summarize.append(i)

    # --- 5. BATCH PROCESSING ---
    
    # Batch A: Keywords (Run on ALL chunks for navigation)
    try:
        keywords_list = KEY_MODEL.extract_keywords(
            docs=text_chunks, 
            keyphrase_ngram_range=(1, 2), 
            stop_words='english', 
            top_n=5
        )
    except Exception as e:
        print(f"KeyBERT Error: {e}")
        keywords_list = [[] for _ in text_chunks]
    
    # Batch B: Summarize (Only the long chunks)
    if chunks_to_summarize:
        # Adjust batch size based on device to prevent crashes
        safe_batch_size = 4 if torch.cuda.is_available() else 1
        generated = batch_generate_summary(chunks_to_summarize, batch_size=safe_batch_size)
        
        for idx, summary in zip(indices_to_summarize, generated):
            final_summaries[idx] = summary

    # --- 6. REASSEMBLE RESULTS ---
    final_output = []
    
    for i, chunk in enumerate(text_chunks):
        # Anchor selection
        candidates = keywords_list[i]
        anchor = f"Part {i+1}"
        
        if candidates:
            for item in candidates:
                if isinstance(item, tuple) or isinstance(item, list): word = item[0]
                elif isinstance(item, str): word = item
                else: continue
                
                if len(word) < 3: continue
                if word.isdigit(): continue
                
                anchor = word.capitalize()
                break
        
        summary = final_summaries[i]
        
        # For UI: Source is now just the paragraph itself
        # We split by sentence just to keep the "Source Box" consistent if needed
        source_sentences = [chunk] 
        
        final_output.append({
            "anchor_word": anchor,
            "summary": summary,
            "source_sentences": source_sentences
        })
        
    return final_output, [], raw_text