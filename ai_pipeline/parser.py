import fitz  # PyMuPDF
import re

def parse_page(page) -> str:
    """
    Parse a PDF page by filtering out headers, footers, and scattered text,
    keeping only substantial body content.
    """
    
    # Get all text blocks
    blocks = page.get_text("blocks")
    page_height = page.rect.height
    page_width = page.rect.width
    
    # Define margins
    margin_top = page_height * 0.08
    margin_bottom = page_height * 0.92
    margin_left = page_width * 0.10
    margin_right = page_width * 0.90
    
    def count_alpha_words(text):
        """Count words that contain letters (not just numbers/symbols)."""
        words = text.split()
        return sum(1 for word in words if any(c.isalpha() for c in word))
    
    def is_substantial_text(text):
        """
        Check if text block contains substantial content.
        Very lenient to catch various formats.
        """
        text_stripped = text.strip()
        
        # Minimum length check
        if len(text_stripped) < 50:
            return False
        
        # Count words with letters
        alpha_word_count = count_alpha_words(text_stripped)
        if alpha_word_count < 10:
            return False
        
        # Check if it has reasonable alphabetic content
        alpha_chars = sum(c.isalpha() or c.isspace() for c in text_stripped)
        if len(text_stripped) > 0 and alpha_chars / len(text_stripped) < 0.4:
            return False
        
        return True
    
    def is_section_heading(text):
        """
        Detect section headings like 'I. INTRODUCTION', 'D. Sensitivity Analysis', etc.
        """
        text_stripped = text.strip()
        
        # Must be relatively short to be a heading
        if len(text_stripped) > 200:
            return False
        
        # Pattern: Single letter or Roman numeral followed by period and title
        if re.match(r'^[A-Z]{1,3}\.?\s*[A-Z]', text_stripped):
            return True
        
        # Pattern: Number followed by period and title
        if re.match(r'^\d+\.(\d+\.?)?\s*[A-Z]', text_stripped):
            return True
        
        return False
    
    def is_header_footer_metadata(text, y_top, y_bottom):
        """
        Detect headers, footers, page numbers, and metadata.
        """
        text_stripped = text.strip()
        
        # Very short text in margins
        if len(text_stripped) < 100:
            if y_bottom < margin_top or y_top > margin_bottom:
                return True
        
        # Page numbers (just digits)
        if re.match(r'^\d+$', text_stripped):
            return True
        
        # ArXiv identifiers
        if 'arxiv' in text_stripped.lower() or re.search(r'\[cs\.\w+\]', text_stripped):
            return True
        
        # Author info (very short with email/university)
        if len(text_stripped) < 200:
            email_count = text_stripped.lower().count('email:') + text_stripped.count('@')
            uni_count = text_stripped.lower().count('university')
            if email_count > 0 and uni_count > 0:
                return True
        
        return False
    
    def is_table_content(text):
        """
        Detect actual table content (rows of data, not captions).
        Much more aggressive detection.
        """
        text_stripped = text.strip()
        lines = text_stripped.split('\n')
        
        # Check for many checkmarks
        checkmark_count = text.count('✓') + text.count('✗') + text.count('✔') + text.count('✘')
        if checkmark_count > 5:
            return True
        
        # Check for table structure characters
        table_chars = text.count('|') + text.count('─') + text.count('│')
        if table_chars > 10:
            return True
        
        # Check for many short lines (typical of table cells)
        if len(lines) > 5:
            short_lines = sum(1 for line in lines if len(line.strip()) < 30 and len(line.strip()) > 0)
            if short_lines / len(lines) > 0.6:  # More than 60% are short lines
                return True
        
        # Check if text has high density of parentheses and numbers
        # (common in tables like "(2×2) Conv(32)")
        paren_count = text.count('(') + text.count(')')
        digit_count = sum(c.isdigit() for c in text_stripped)
        if len(text_stripped) > 0:
            special_ratio = (paren_count + digit_count) / len(text_stripped)
            if special_ratio > 0.3:  # More than 30% special chars/digits
                return True
        
        # Check if many lines have numbers but very few complete sentences
        if len(lines) > 3:
            numeric_lines = 0
            for line in lines:
                numbers = sum(c.isdigit() for c in line)
                if numbers > 2 and '.' not in line[-3:]:  # Has numbers but not sentence ending
                    numeric_lines += 1
            
            if numeric_lines / len(lines) > 0.4:  # More than 40% are numeric non-sentences
                return True
        
        # Check for common table keywords in isolation
        table_keywords = ['input', 'output', 'dropout', 'dense', 'conv', 'maxpo', 'flatten', 
                         'relu', 'sigmoid', 'merge', 'embedding', 'latent', 'explicit']
        isolated_keywords = 0
        for line in lines:
            line_lower = line.lower().strip()
            if line_lower in table_keywords or any(line_lower == kw for kw in table_keywords):
                isolated_keywords += 1
        
        if isolated_keywords > 3:  # Multiple isolated table keywords
            return True
        
        # Check average line length - tables have short lines
        if len(lines) > 3:
            avg_line_length = sum(len(line.strip()) for line in lines if line.strip()) / max(len([l for l in lines if l.strip()]), 1)
            if avg_line_length < 20:  # Very short average line length
                return True
        
        return False
    
    def looks_like_caption(text):
        """Check if text looks like a figure or table caption."""
        text_lower = text.lower().strip()
        
        # Very specific caption patterns at start of text
        caption_patterns = [
            r'^table\s+[ivxlcdm0-9]+',  # TABLE IV, Table 1, etc.
            r'^figure\s+[0-9]+',          # Figure 1, etc.
            r'^fig\.\s*[0-9]+',           # Fig. 1, etc.
            r'^algorithm\s+[0-9]+',       # Algorithm 1, etc.
        ]
        
        for pattern in caption_patterns:
            if re.match(pattern, text_lower):
                return True
        
        return False
    
    # --- FILTER BLOCKS ---
    content_blocks = []
    
    for b in blocks:
        if b[6] != 0:  # Not a text block
            continue
        
        text = b[4]
        y_top = b[1]
        y_bottom = b[3]
        x_left = b[0]
        x_right = b[2]
        
        # Skip if outside content area vertically
        if y_bottom < margin_top or y_top > margin_bottom:
            continue
        
        # Skip if in side margins
        if x_right < margin_left or x_left > margin_right:
            continue
        
        # Skip headers/footers/metadata
        if is_header_footer_metadata(text, y_top, y_bottom):
            continue
        
        # Skip actual table content (data rows) - THIS IS THE KEY CHECK
        if is_table_content(text):
            continue
        
        # Keep if any of these conditions are true:
        if (is_substantial_text(text) or 
            is_section_heading(text) or 
            looks_like_caption(text)):
            content_blocks.append(b)
    
    # --- DETECT TWO-COLUMN LAYOUT ---
    is_two_column = False
    if len(content_blocks) > 3:
        page_midpoint = page_width / 2
        
        left_blocks = [b for b in content_blocks if (b[0] + b[2]) / 2 < page_midpoint]
        right_blocks = [b for b in content_blocks if (b[0] + b[2]) / 2 >= page_midpoint]
        
        total = len(content_blocks)
        if total > 0:
            left_ratio = len(left_blocks) / total
            right_ratio = len(right_blocks) / total
            
            if left_ratio > 0.05 and right_ratio > 0.05:
                is_two_column = True
    
    # --- PROCESS BASED ON LAYOUT ---
    if is_two_column:
        page_midpoint = page_width / 2
        left_col = [b for b in content_blocks if (b[0] + b[2]) / 2 < page_midpoint]
        right_col = [b for b in content_blocks if (b[0] + b[2]) / 2 >= page_midpoint]
        
        left_col.sort(key=lambda b: b[1])
        right_col.sort(key=lambda b: b[1])
        
        left_text = "\n".join([b[4] for b in left_col])
        right_text = "\n".join([b[4] for b in right_col])
        
        return left_text + "\n" + right_text
    else:
        content_blocks.sort(key=lambda b: b[1])
        return "\n".join([b[4] for b in content_blocks])


def parse_pdf(pdf_path, page_numbers=None):
    """
    Parse PDF file and extract clean text.
    
    Args:
        pdf_path: Path to the PDF file
        page_numbers: List of page numbers to parse (1-indexed), or None for all pages
    
    Returns:
        Parsed text from specified pages
    """
    try:
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        
        # Determine which pages to process
        if page_numbers is None:
            pages_to_process = range(total_pages)
            print(f"Processing all {total_pages} pages...")
        else:
            pages_to_process = []
            for page_num in page_numbers:
                if 1 <= page_num <= total_pages:
                    pages_to_process.append(page_num - 1)
                else:
                    print(f"Warning: Page {page_num} is out of range (1-{total_pages}), skipping...")
            
            if not pages_to_process:
                print("No valid pages to process!")
                doc.close()
                return None
            
            print(f"Processing {len(pages_to_process)} page(s): {sorted([p+1 for p in pages_to_process])}")
        
        all_text = []
        
        for page_idx in pages_to_process:
            page = doc[page_idx]
            print(f"\n{'='*60}")
            print(f"Processing Page {page_idx + 1}")
            print('='*60)
            
            page_text = parse_page(page)
            
            if page_text.strip():
                all_text.append(f"\n--- Page {page_idx + 1} ---\n")
                all_text.append(page_text)
            else:
                print(f"Warning: No content extracted from page {page_idx + 1}")
        
        doc.close()
        
        return "\n".join(all_text)
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


if __name__ == "__main__":
    pdf_path = "path/to/your/paper.pdf"
    
    # Parse specific pages
    result = parse_pdf(pdf_path, page_numbers=[1, 2])
    
    if result:
        print("\n" + "="*60)
        print("FINAL PARSED TEXT")
        print("="*60)
        print(result)
        
        output_file = "parsed_output.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"\n✓ Output saved to {output_file}")
    else:
        print("Failed to parse PDF")