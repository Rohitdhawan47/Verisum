import streamlit as st
import requests
import time
import re

# Page configuration
st.set_page_config(
    page_title="AI Document Summarizer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #ffffff 0%, #fef5f8 50%, #ffffff 100%);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Hide default padding */
    .block-container {
        padding-top: 2rem;
    }
    
    /* Main heading */
    .main-heading {
        font-size: 3.5rem;
        font-weight: 700;
        color: #1f2937;
        text-align: center;
        margin-top: 3rem;
        margin-bottom: 1rem;
        letter-spacing: -0.02em;
        line-height: 1.2;
    }
    
    /* Tagline */
    .tagline {
        font-size: 1.2rem;
        color: #6b7280;
        text-align: center;
        margin-bottom: 3rem;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* Upload box container */
    .upload-container {
        max-width: 600px;
        margin: 0 auto;
        padding: 3rem;
        border-radius: 1.5rem;
        border: 2px solid #fce7f3;
        background: linear-gradient(to bottom right, #fef5f8, white);
        box-shadow: 0 0 30px rgba(251, 207, 232, 0.15);
        text-align: center;
        transition: all 0.4s ease;
    }
    
    .upload-container:hover {
        box-shadow: 
            0 0 40px rgba(251, 207, 232, 0.6),
            0 0 80px rgba(249, 168, 212, 0.4);
        transform: translateY(-5px);
        border-color: #f9a8d4;
    }
    
    /* Upload icon */
    .upload-icon {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        background: linear-gradient(135deg, #fbcfe8, #f9a8d4);
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1.5rem;
        font-size: 3rem;
        box-shadow: 0 8px 20px rgba(251, 207, 232, 0.3);
    }
    
    /* Page selector box */
    .page-selector-box {
        background: white;
        border: 2px solid #e5e7eb;
        border-radius: 1rem;
        padding: 1.5rem;
        margin-top: 2rem;
    }
    
    .page-selector-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 1rem;
    }
    
    /* Scanning animation */
    .scanning-container {
        max-width: 800px;
        margin: 8rem auto;
        text-align: center;
    }
    
    .scanning-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 3rem;
    }
    
    .scanning-box {
        position: relative;
        width: 100%;
        height: 400px;
        background: linear-gradient(to bottom right, #f9fafb, #e5e7eb);
        border-radius: 1.5rem;
        overflow: hidden;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        border: 2px solid #e5e7eb;
    }
    
    .scanning-line {
        position: absolute;
        left: 0;
        right: 0;
        height: 8px;
        background: linear-gradient(to right, transparent, #fbcfe8, transparent);
        box-shadow: 0 0 20px rgba(251, 207, 232, 0.6);
        animation: scan 1.5s linear infinite;
    }
    
    @keyframes scan {
        0% { top: 0%; }
        100% { top: 100%; }
    }
    
    .scanning-icon {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 8rem;
        color: #9ca3af;
        opacity: 0.3;
    }
    
    .scanning-text {
        color: #6b7280;
        font-size: 1.2rem;
        margin-top: 2rem;
        font-weight: 500;
    }
    
    /* Results page */
    .results-heading {
        font-size: 3rem;
        font-weight: 700;
        color: #1f2937;
        text-align: center;
        margin: 2rem 0 3rem 0;
    }
    
    /* Panel styling */
    .panel {
        background-color: white;
        border-radius: 1.5rem;
        border: 2px solid #e5e7eb;
        padding: 2rem;
        min-height: 600px;
        max-height: 800px;
        overflow-y: auto;
    }
    
    .panel-title {
        font-size: 1.8rem;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #e5e7eb;
    }
    
    /* Summary cards with colors */
    .summary-card {
        padding: 1.5rem;
        border-radius: 1rem;
        margin-bottom: 1.5rem;
        border: 2px solid;
    }
    
    .summary-card-green {
        background-color: #d1fae5;
        border-color: #6ee7b7;
    }
    
    .summary-card-blue {
        background-color: #dbeafe;
        border-color: #93c5fd;
    }
    
    .summary-card-yellow {
        background-color: #fef3c7;
        border-color: #fde047;
    }
    
    .summary-card-pink {
        background-color: #fce7f3;
        border-color: #f9a8d4;
    }
    
    .summary-anchor {
        font-weight: 700;
        font-size: 1.1rem;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    
    .summary-text {
        color: #374151;
        line-height: 1.7;
        font-size: 1rem;
    }
    
    /* Highlighted source text */
    .source-paragraph {
        padding: 1rem;
        margin-bottom: 1rem;
        background: #f9fafb;
        border-radius: 0.5rem;
        line-height: 1.8;
        color: #1f2937;
    }
    
    .highlight-green {
        background-color: #d1fae5;
        padding: 0.2rem 0.4rem;
        border-radius: 0.3rem;
    }
    
    .highlight-blue {
        background-color: #dbeafe;
        padding: 0.2rem 0.4rem;
        border-radius: 0.3rem;
    }
    
    .highlight-yellow {
        background-color: #fef3c7;
        padding: 0.2rem 0.4rem;
        border-radius: 0.3rem;
    }
    
    .highlight-pink {
        background-color: #fce7f3;
        padding: 0.2rem 0.4rem;
        border-radius: 0.3rem;
    }
    
    /* Error styling */
    .error-box {
        background-color: #fee2e2;
        border: 2px solid #fca5a5;
        border-radius: 1rem;
        padding: 1.5rem;
        color: #991b1b;
        margin: 2rem auto;
        max-width: 600px;
        text-align: center;
    }
    
    .success-box {
        background-color: #d1fae5;
        border: 2px solid #6ee7b7;
        border-radius: 1rem;
        padding: 1rem;
        color: #065f46;
        margin: 1rem auto;
        text-align: center;
        font-weight: 600;
    }
    
</style>
""", unsafe_allow_html=True)

# ============= CONFIGURATION =============
# Your existing backend URL
BACKEND_URL =  "https://nomistic-unpessimistic-andrew.ngrok-free.dev"

# ============= HELPER FUNCTIONS =============

def check_backend_health():
    """Check if backend is reachable"""
    try:
        response = requests.get(f"{BACKEND_URL}/docs", timeout=30)
        return response.status_code == 200
    except:
        return False

def get_pdf_page_count(uploaded_file):
    """Get total pages by sending PDF to backend"""
    try:
        # Send to backend just to get page count
        files = {"file": uploaded_file.getvalue()}
        data = {"page_num": 0}  # Dummy page
        
        response = requests.post(
            f"{BACKEND_URL}/summarize",
            files=files,
            data=data,
            timeout=300
        )
        
        if response.status_code == 200:
            # Extract page count from raw_text or use PyMuPDF locally
            import fitz
            doc = fitz.open(stream=uploaded_file.getvalue(), filetype="pdf")
            total_pages = len(doc)
            doc.close()
            return total_pages
        return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

def process_pages_backend(uploaded_file, pages_to_process):
    """Send PDF to backend for processing multiple pages"""
    all_results = []
    
    for page_num in pages_to_process:
        try:
            # Prepare the request
            files = {"file": ("document.pdf", uploaded_file.getvalue(), "application/pdf")}
            data = {"page_num": page_num - 1}  # Backend uses 0-indexed
            
            # Send request
            response = requests.post(
                f"{BACKEND_URL}/summarize",
                files=files,
                data=data,
                timeout=300
            )
            
            if response.status_code == 200:
                result = response.json()
                all_results.append({
                    "page_number": page_num,
                    "summaries": result["results"],
                    "raw_text": result["raw_text"]
                })
            else:
                st.error(f"Error processing page {page_num}")
                
        except Exception as e:
            st.error(f"Error on page {page_num}: {str(e)}")
    
    return all_results

def parse_page_input(page_input_str, total_pages):
    """Parse user's page input string"""
    try:
        page_input_str = page_input_str.strip().lower()
        
        if page_input_str == "all":
            return list(range(1, total_pages + 1))
        
        pages = []
        parts = page_input_str.replace(' ', '').split(',')
        
        for part in parts:
            if '-' in part:
                start, end = part.split('-')
                start, end = int(start), int(end)
                if start > end:
                    start, end = end, start
                pages.extend(range(start, min(end + 1, total_pages + 1)))
            else:
                page_num = int(part)
                if 1 <= page_num <= total_pages:
                    pages.append(page_num)
        
        return sorted(list(set(pages)))
    except:
        return None

def add_highlights_to_text(raw_text, summaries):
    """Add color highlights to raw text based on source sentences"""
    colors = ['green', 'blue', 'yellow', 'pink']
    highlighted_text = raw_text
    
    for i, summary_item in enumerate(summaries):
        color = colors[i % len(colors)]
        
        # Get source sentences for this summary
        source_sentences = summary_item.get('source_sentences', [])
        
        for sentence in source_sentences:
            # Only highlight substantial text to avoid messy partial matches
            if len(sentence.strip()) > 20:  
                
                # 1. Escape special regex characters (like parentheses)
                escaped = re.escape(sentence.strip())
                
                # --- THE FIX ---
                # 2. Replace literal spaces with a regex pattern that matches 
                #    spaces OR newlines (\s+). This allows matches even if 
                #    the PDF text wraps to a new line.
                pattern = escaped.replace(r'\ ', r'\s+')
                
                # 3. Replace with highlighted version
                # We use \1 to keep the original formatting (newlines) inside the highlight
                highlighted_text = re.sub(
                    f'({pattern})',
                    f'<span class="highlight-{color}">\\1</span>',
                    highlighted_text,
                    count=1,
                    flags=re.IGNORECASE
                )
    
    return highlighted_text

# ============= SESSION STATE =============
if 'page' not in st.session_state:
    st.session_state.page = 'upload'
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None
if 'total_pages' not in st.session_state:
    st.session_state.total_pages = None
if 'selected_pages' not in st.session_state:
    st.session_state.selected_pages = None
if 'results' not in st.session_state:
    st.session_state.results = None

# ============= PAGE 1: UPLOAD =============
if st.session_state.page == 'upload':
    st.markdown('<div class="main-heading">Artificial Intelligence Driven Document Summarizer</div>', unsafe_allow_html=True)
    st.markdown('<div class="tagline">Transform lengthy documents into concise summaries with GPU-powered AI</div>', unsafe_allow_html=True)
    
    # Check backend
    if check_backend_health():
        st.markdown('<div class="success-box">✅ Backend Connected</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="error-box"><strong>❌ Backend Offline</strong><br>Make sure your Colab notebook is running!</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('''
        <div class="upload-container">
            <div class="upload-icon">📤</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #f9a8d4; margin-bottom: 0.5rem;">Upload Your Document</div>
            <div style="color: #9ca3af; margin-bottom: 1.5rem;">Drag and drop your PDF file</div>
        </div>
        ''', unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("Choose a PDF file", type=['pdf'], key="pdf_uploader", label_visibility="collapsed")
        
        if uploaded_file is not None:
            st.session_state.uploaded_file = uploaded_file
            
            with st.spinner("Reading PDF..."):
                total_pages = get_pdf_page_count(uploaded_file)
            
            if total_pages:
                st.session_state.total_pages = total_pages
                
                st.markdown(f'''
                <div class="page-selector-box">
                    <div class="page-selector-title">📄 PDF loaded: {total_pages} pages</div>
                    <p style="color: #6b7280; margin-bottom: 1rem;">Select which pages to summarize:</p>
                </div>
                ''', unsafe_allow_html=True)
                
                page_input = st.text_input(
                    "Enter pages",
                    placeholder=f'e.g., "all", "1,2,3", "1-5", "1,3,5-7"',
                    help=f"Available pages: 1-{total_pages}"
                )
                
                if st.button("🚀 Start Summarization", type="primary", use_container_width=True):
                    if not page_input:
                        st.error("Please enter page numbers!")
                    else:
                        selected_pages = parse_page_input(page_input, total_pages)
                        
                        if not selected_pages:
                            st.error(f"Invalid page selection! Enter pages between 1-{total_pages}")
                        else:
                            st.session_state.selected_pages = selected_pages
                            st.session_state.page = 'processing'
                            st.rerun()

# ============= PAGE 2: PROCESSING =============
elif st.session_state.page == 'processing':
    st.markdown('<div class="scanning-container">', unsafe_allow_html=True)
    st.markdown('<div class="scanning-title">Analyzing Document with AI 🤖</div>', unsafe_allow_html=True)
    st.markdown('''
        <div class="scanning-box">
            <div class="scanning-line"></div>
            <div class="scanning-icon">📄</div>
        </div>
    ''', unsafe_allow_html=True)
    st.markdown(f'<div class="scanning-text">Processing {len(st.session_state.selected_pages)} page(s) using GPU acceleration...</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Process pages
    results = process_pages_backend(st.session_state.uploaded_file, st.session_state.selected_pages)
    
    if results:
        st.session_state.results = results
        time.sleep(1)
        st.session_state.page = 'results'
        st.rerun()
    else:
        st.error("Processing failed!")
        time.sleep(2)
        st.session_state.page = 'upload'
        st.rerun()

# ==========================================
# PAGE 3: RESULTS
# ==========================================
elif st.session_state.page == 'results':
    st.markdown('<div class="main-heading">Analysis Complete</div>', unsafe_allow_html=True)
    
    if st.button("← Process Another Document", type="secondary"):
        st.session_state.page = 'upload'
        st.session_state.results = None
        st.rerun()
    
    results = st.session_state.results
    
    # Define colors to match Left and Right panels
    colors = ['green', 'blue', 'yellow', 'pink']
    
    # Iterate through processed pages
    for page_result in results:
        page_num = page_result['page_number']
        summaries = page_result['summaries']
        
        st.markdown(f"### 📄 Page {page_num}")
        
        col1, col2 = st.columns([1, 1], gap="large")
        
        # --- LEFT PANEL: KEY SUMMARIES ---
        with col1:
            left_html = '<div class="panel"><div class="panel-title">Key Summaries</div>'
            
            if not summaries:
                left_html += '<div style="color:red">No summary available.</div>'
            else:
                for i, topic in enumerate(summaries):
                    # 1. Pick Color
                    color = colors[i % len(colors)]
                    
                    anchor = topic['anchor_word']
                    summary = topic['summary']
                    source = " ".join(topic['source_sentences']).replace('"', '&quot;')
                    
                    left_html += f"""
<div class="summary-card summary-card-{color}">
<div class="summary-anchor">📌 {anchor}</div>
<div class="summary-text">{summary}</div>
<details style="cursor:pointer; color:#555; font-size:0.9rem; margin-top:10px;">
<summary>View Evidence</summary>
<div class="source-box" style="margin-top:5px;">{source}</div>
</details>
</div>"""
            left_html += '</div>'
            st.markdown(left_html, unsafe_allow_html=True)
            
        # --- RIGHT PANEL: EXACT SOURCE TEXT ---
        with col2:
            right_html = '<div class="panel"><div class="panel-title">Source Context</div>'
            
            if not summaries:
                right_html += '<div style="color:gray">No text processed.</div>'
            else:
                for i, topic in enumerate(summaries):
                    # 1. Pick SAME Color as Left Panel
                    color = colors[i % len(colors)]
                    
                    # 2. Get the Exact Text Chunk used for this summary
                    # (No regex matching needed, this IS the text)
                    chunk_text = " ".join(topic['source_sentences'])
                    
                    # 3. Render it highlighted
                    right_html += f"""
<div class="source-paragraph highlight-{color}">
<strong style="opacity:0.5; font-size:0.8em;">SECTION {i+1}</strong><br>
{chunk_text}
</div>"""
            
            right_html += '</div>'
            st.markdown(right_html, unsafe_allow_html=True)
        
        st.markdown("---")