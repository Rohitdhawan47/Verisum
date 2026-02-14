# VeriSum - AI-Powered PDF Summarizer 📄🤖

An intelligent document summarization system that uses GPU-accelerated AI models to generate concise summaries of PDF documents. The system features a beautiful Streamlit frontend connected to a powerful Kaggle backend running LED (Longformer Encoder-Decoder) models.

![VeriSum Banner](https://img.shields.io/badge/AI-Document_Summarizer-pink?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green?style=for-the-badge&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red?style=for-the-badge&logo=streamlit)
![Status](https://img.shields.io/badge/Status-Beta-yellow?style=for-the-badge)

## 🚧 Project Status

**Current State: Functional Beta**

This project is **complete and working** but still under active development. Here's what you should know:

- ✅ **Core functionality works**: PDF parsing, summarization, and display are operational
- ✅ **Runs end-to-end**: You can process documents and get results
- ⚠️ **UI needs refinement**: The interface works but could be more polished
- ⚠️ **Solo development**: Built and maintained by one person, so updates take time
- 🔨 **Active improvements**: New features and refinements are ongoing

### 🔬 Current Development Focus

**GROBID Parser Integration (Work in Progress)**
- Working on a new parser version using [GROBID](https://github.com/kermitt2/grobid) for improved academic document structure extraction
- GROBID offers better handling of citations, references, and document sections
- This will be an alternative to the current PyMuPDF-based parser
- **Status**: Experimental - not yet integrated into main branch

**What this means for you:**
- The current PyMuPDF parser is stable and recommended for use
- GROBID parser will be available as an optional upgrade when ready
- Expect the project to evolve with better parsing and UI improvements over time

### 💡 Contributions Welcome!

Since this is a solo project, contributions are highly appreciated:
- UI/UX improvements
- Parser optimizations
- Documentation enhancements
- Bug reports and testing
- Feature suggestions

**TL;DR**: VeriSum works well for its intended purpose but isn't production-grade. Use it, experiment with it, and help make it better!

## 🌟 Features

- **GPU-Accelerated Summarization**: Leverages Kaggle's P100 GPU for fast processing
- **Smart Text Parsing**: Advanced PDF parsing that filters out headers, footers, tables, and metadata
- **Batch Processing**: Process multiple pages simultaneously with intelligent chunking
- **Interactive UI**: Beautiful gradient-themed interface with real-time processing animations
- **Keyword Extraction**: Automatic anchor word generation using KeyBERT
- **Color-Coded Summaries**: Visual highlighting to match summaries with source text
- **Flexible Page Selection**: Process specific pages, ranges, or entire documents

## 🏗️ Architecture

```
┌─────────────────────┐
│   Streamlit App     │
│   (Local Machine)   │
└──────────┬──────────┘
           │
           │ HTTPS
           ↓
┌─────────────────────┐
│   ngrok Tunnel      │
│  (Public Domain)    │
└──────────┬──────────┘
           │
           │
           ↓
┌─────────────────────┐
│   FastAPI Server    │
│  (Kaggle Notebook)  │
│   + LED Model       │
│   + KeyBERT         │
│   + PyMuPDF         │
└─────────────────────┘
```

## 📁 Project Structure

```
verisum/
├── ai_pipeline/
│   ├── __init__.py              # Empty file for package initialization
│   ├── main_pipeline.py         # Core processing pipeline
│   ├── model_loader.py          # LED and KeyBERT model loaders
│   └── parser.py                # Advanced PDF parsing logic
├── app.py                       # Streamlit frontend application
├── requirements.txt             # Local dependencies
└── README.md                    # This file
```

## 🚀 Setup Guide

### Prerequisites

- Python 3.9 or higher
- Kaggle account
- ngrok account (free tier works)
- Git (for cloning repository)

---

## Part 1: Setting Up ngrok 🌐

### 1.1 Create ngrok Account

1. Go to [ngrok.com](https://ngrok.com/)
2. Sign up for a free account
3. Navigate to your [dashboard](https://dashboard.ngrok.com/)

### 1.2 Get Your Auth Token

1. In the ngrok dashboard, go to **"Your Authtoken"** section
2. Copy your authentication token (looks like: `2abc...xyz123`)
3. Save this token - you'll need it for Kaggle setup

### 1.3 Reserve a Static Domain (Optional but Recommended)

1. In the ngrok dashboard, go to **"Domains"**
2. Click **"Create Domain"** or **"New Domain"**
3. You'll get a free static domain like: `nomistic-unpessimistic-andrew.ngrok-free.dev`
4. Copy this domain - you'll use it in both Kaggle and Streamlit

**Why use a static domain?**
- Your URL won't change every time you restart
- No need to update `app.py` constantly
- More professional looking URL

---

## Part 2: Setting Up Kaggle Backend 🖥️

### 2.1 Prepare the Kaggle Environment

1. Go to [Kaggle](https://www.kaggle.com/) and sign in
2. Create a new notebook or use [this one](https://www.kaggle.com/code/rohitdhawan23/verisum)
3. **Important**: Enable GPU acceleration
   - Click on the three dots menu (⋮) in the top right
   - Select **"Accelerator"** → **"GPU P100"**

### 2.2 Add the LED Model as a Kaggle Dataset

The system uses a fine-tuned LED model for summarization. You have **three options**:

> 📘 **Detailed Guide**: See [KAGGLE_DATASET_SETUP.md](KAGGLE_DATASET_SETUP.md) for comprehensive instructions with troubleshooting.

#### **Option A: Auto-Download (Easiest - Recommended for Beginners)**

**No setup required!** The model downloads automatically from HuggingFace.

- **Pros**: Zero configuration, always latest version
- **Cons**: First run takes 3-5 minutes to download 1.6GB
- **Best for**: First-time users, testing, one-time use

**Just run the notebook cells in order - that's it!**

#### **Option B: Use Existing Kaggle Dataset (Faster)**

Search for and add a pre-uploaded dataset:

1. In your Kaggle notebook, click **"+ Add Data"** (right sidebar)
2. Search: `led-large-16384-arxiv` or `led-arxiv-model`
3. Add any dataset containing the LED model files
4. Verify path (usually `/kaggle/input/led-arxiv-model/`)
5. If needed, update `KAGGLE_PATH` in `ai_pipeline/model_loader.py`

**Benefit**: Subsequent runs start in ~1-2 minutes instead of 3-5 minutes

#### **Option C: Create Your Own Dataset (Advanced)**

For full control or if sharing with a team:

1. **Download locally** (your machine):
   ```python
   from transformers import LEDForConditionalGeneration, LEDTokenizer
   model = LEDForConditionalGeneration.from_pretrained("allenai/led-large-16384-arxiv")
   tokenizer = LEDTokenizer.from_pretrained("allenai/led-large-16384-arxiv")
   model.save_pretrained("./led_model_saved")
   tokenizer.save_pretrained("./led_model_saved")
   ```

2. **Upload to Kaggle**:
   - Go to [kaggle.com/datasets](https://www.kaggle.com/datasets) → "New Dataset"
   - Upload the `led_model_saved` folder
   - Make it Public or Private

3. **Add to notebook**: "+ Add Data" → "Your Datasets" → Select your LED dataset

**Which method should I use?**
- **First time?** → Option A (auto-download)
- **Using regularly?** → Option B (existing dataset) 
- **Need control?** → Option C (create your own)

### 2.3 Run the Kaggle Notebook

Copy and paste the following cells into your Kaggle notebook:

#### **Visual Guide: Adding Data in Kaggle**

```
Kaggle Notebook Interface:
┌─────────────────────────────────────────────────┐
│  ☰  VeriSum Notebook    [▶ Run All]  [Save]   │
├─────────────────────────────────────────────────┤
│                                    ┌────────────┤
│  # Your code cells                 │  + Add Data│ ← Click here
│  ...                               ├────────────┤
│                                    │ 📁 Datasets│
│                                    │            │
│                                    │ Search:    │
│                                    │ [_______]  │
│                                    │            │
│                                    │ Results:   │
│                                    │ ☐ led-arxi │ ← Check this
│                                    │ ☐ other... │
│                                    └────────────┘
```

After adding dataset, you'll see it mounted at:
```
/kaggle/input/
├── led-arxiv-model/           ← Your LED model dataset
│   ├── config.json
│   ├── pytorch_model.bin
│   ├── tokenizer_config.json
│   └── ...
└── verisum/                   ← (If you add GitHub as dataset)
```

#### **Cell 1: Install Dependencies**

```python
# --- 1. CRITICAL FIXES (Run First) ---
# Fix the "MessageFactory" Crash (TensorFlow/Protobuf Conflict)
!pip uninstall -y protobuf
!pip install protobuf==3.20.3

# Fix the "Module Not Found: Tools" Crash (The PDF Library Trap)
!pip uninstall -y fitz
!pip install -U PyMuPDF

# --- 2. INSTALL DEPENDENCIES ---
# Server & Networking
!pip install -q pyngrok fastapi uvicorn python-multipart nest_asyncio streamlit

# AI Optimization (Quantization)
!pip install -q bitsandbytes accelerate

# NLP & Keywords
!pip install -q sentence-transformers keybert

# Vision (Moondream)
!pip install -q einops
```

#### **Cell 2: Clone GitHub Repository**

```python
import os
import shutil

# --- CONFIGURATION ---
GITHUB_REPO = "https://github.com/Rohitdhawan47/verisum.git"
BRANCH = "main"
WORKING_DIR = "/kaggle/working"
DEST_FOLDER = f"{WORKING_DIR}/ai_pipeline"

print(f"🔄 Syncing with GitHub...")

# 1. CLEANUP: Delete old pipeline to prevent conflicts
if os.path.exists(DEST_FOLDER):
    shutil.rmtree(DEST_FOLDER)

# 2. CLONE: Download repo to temp folder
if os.path.exists("temp_repo"):
    shutil.rmtree("temp_repo")
    
!git clone -b {BRANCH} {GITHUB_REPO} temp_repo


# 3. INSTALL: Create the folder and move the files
# Now we move ONLY from temp_repo/ai_pipeline

print("📂 Organizing files...")
os.makedirs(DEST_FOLDER, exist_ok=True)


# 🔽 CHANGED: source path
source = "temp_repo/ai_pipeline"


# 🔽 ADDED: safety check
if not os.path.exists(source):
    raise Exception("ai_pipeline folder not found in repo!")


files_moved = 0
for file_name in os.listdir(source):

    # Skip hidden git files if any
    if file_name.startswith(".git"):
        continue
        
    src = os.path.join(source, file_name)
    dst = os.path.join(DEST_FOLDER, file_name)

    shutil.move(src, dst)
    files_moved += 1


# 4. CLEANUP: Delete the empty temp box
shutil.rmtree("temp_repo")


if files_moved > 0:
    print(f"✅ Success! Moved {files_moved} files into 'ai_pipeline/'.")
    print(f"   Contents: {os.listdir(DEST_FOLDER)}")
else:
    print("❌ Warning: No files were found in the repo.")

```

#### **Cell 3: Launch FastAPI Server**

```python
import nest_asyncio
from pyngrok import ngrok
import uvicorn
from fastapi import FastAPI, File, UploadFile, Form
import shutil
import fitz 
import os

# --- KAGGLE SPECIFIC CONFIG ---
os.chdir("/kaggle/working")

# Import your pipeline
print("⏳ WARMING UP MODELS...")
from ai_pipeline.main_pipeline import process_page_pipeline
from ai_pipeline.parser import parse_page 
print("✅ Models Ready!")

# --- SETUP SERVER ---
# Replace with YOUR ngrok token from dashboard.ngrok.com
NGROK_TOKEN = "YOUR_NGROK_TOKEN_HERE"  # ← CHANGE THIS
ngrok.set_auth_token(NGROK_TOKEN)

app = FastAPI()

@app.post("/summarize")
async def summarize_endpoint(page_num: int = Form(...), file: UploadFile = File(...)):
    print(f"Received Page {page_num+1}...")
    
    temp_filename = "server_temp.pdf"
    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    doc = fitz.open(temp_filename)
    page = doc.load_page(page_num)
    raw_text = parse_page(page)
    doc.close()
    
    results, junk, raw_text = process_page_pipeline(temp_filename, page_num)
    
    return {"results": results, "junk": junk, "raw_text": raw_text}

# --- LAUNCH ---
# Replace with YOUR static domain from ngrok (if you have one)
public_url = ngrok.connect(8000, domain="YOUR-DOMAIN.ngrok-free.dev").public_url
print(f"\n🚀 KAGGLE BACKEND LIVE: {public_url}\n")

nest_asyncio.apply()
config = uvicorn.Config(app, host="0.0.0.0", port=8000)
server = uvicorn.Server(config)
await server.serve()
```

**⚠️ Important Changes:**
- Replace `YOUR_NGROK_TOKEN_HERE` with your actual ngrok auth token
- Replace `YOUR-DOMAIN.ngrok-free.dev` with your static domain (or remove `domain=` parameter for random URL)

### 2.4 Run the Cells

1. Run Cell 1 and wait for all packages to install (~2-3 minutes)
2. Run Cell 2 to clone the GitHub repository
3. Run Cell 3 to start the server

You should see output like:
```
⏳ WARMING UP MODELS...
✅ Models Ready!
🚀 KAGGLE BACKEND LIVE: https://nomistic-unpessimistic-andrew.ngrok-free.dev
```

**Copy this URL** - you'll need it for the frontend!

---

## Part 3: Setting Up Local Frontend 💻

### 3.1 Clone the Repository

```bash
git clone https://github.com/Rohitdhawan47/verisum.git
cd verisum
```

### 3.2 Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3.3 Install Dependencies

Create a `requirements.txt` file with:

```txt
streamlit==1.31.0
requests==2.31.0
PyMuPDF==1.23.8
```

Then install:

```bash
pip install -r requirements.txt
```

### 3.4 Configure Backend URL

Open `app.py` and update the `BACKEND_URL` variable:

```python
# Line ~220 in app.py
BACKEND_URL = "https://your-actual-ngrok-url.ngrok-free.dev"
```

Replace with the URL from your Kaggle notebook output.

### 3.5 Run the Frontend

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 🎯 Usage Guide

### Step 1: Upload PDF
1. Open the Streamlit app in your browser
2. Check that "✅ Backend Connected" appears at the top
3. Drag and drop a PDF file or click to browse

### Step 2: Select Pages
Once uploaded, you can specify which pages to process:

- **All pages**: Type `all`
- **Specific pages**: Type `1,3,5`
- **Range**: Type `1-5`
- **Mixed**: Type `1,3,5-7,10`

### Step 3: Process
1. Click "🚀 Start Summarization"
2. Watch the scanning animation while AI processes your document
3. View results with color-coded summaries and source text

### Step 4: Review Results
- **Left Panel**: Key summaries with anchor words
- **Right Panel**: Original source text with color highlights
- Click "View Evidence" to see exact source sentences

---

## 🔧 How It Works

### PDF Parsing Pipeline

1. **Layout Detection**: Identifies single/double-column layouts
2. **Content Filtering**: Removes headers, footers, page numbers, metadata
3. **Table Detection**: Filters out table data while keeping captions
4. **Text Cleaning**: Fixes ligatures, removes math symbols, normalizes whitespace

### Summarization Pipeline

1. **Smart Chunking**: Splits text into ~200-word semantic chunks
2. **Hybrid Processing**: 
   - Short paragraphs (<50 words): Copied as-is
   - Long paragraphs: Summarized using LED model
3. **Keyword Extraction**: KeyBERT identifies anchor words
4. **Batch Generation**: Processes multiple chunks simultaneously for speed

### Model Architecture

- **LED (Longformer Encoder-Decoder)**: Handles long documents (16K tokens)
- **Fine-tuned on arXiv**: Optimized for academic/technical content
- **FP32 Precision**: Configured for P100 GPU compatibility
- **Beam Search**: 4 beams for quality summaries

---

## 📊 Performance

| Metric | Value |
|--------|-------|
| Pages per minute | ~2-3 (with GPU) |
| Max input length | 16,384 tokens |
| Summary length | 20-512 tokens |
| Keyword extraction | 5 per chunk |
| Supported formats | PDF only |

---

## 🐛 Troubleshooting

### Dataset & Model Issues

**Problem**: "Model not found at /kaggle/input/led-arxiv-model/"
- **Solution 1**: Check if dataset is added to notebook
  - Look in right sidebar under "Data Sources"
  - Should see "led-arxiv-model" or similar
- **Solution 2**: Verify the exact path by running in a Kaggle cell:
  ```python
  import os
  print(os.listdir('/kaggle/input/'))
  ```
- **Solution 3**: Update `KAGGLE_PATH` in `ai_pipeline/model_loader.py` to match your actual dataset path
- **Solution 4**: Just let it auto-download (slower but works):
  - Comment out the dataset path in `model_loader.py`
  - Model downloads from HuggingFace automatically

**Problem**: "Cannot find led-arxiv-model dataset in Kaggle search"
- **Solution**: Don't worry! Use auto-download instead
- The model will download automatically from HuggingFace on first run (~3-5 minutes)
- No dataset setup needed - just ensure you have internet access in Kaggle

**Problem**: "Model loading takes forever (>10 minutes)"
- **Solution 1**: Verify GPU is enabled
  - Click Settings (gear icon) → Accelerator → Select "GPU P100"
  - Restart notebook after enabling
- **Solution 2**: First run downloads 1.6GB model (one-time only)
  - Subsequent runs load from cache (~1-2 minutes)
- **Solution 3**: Check internet connection in Kaggle
  - Settings → Internet → Should be "On"

**Problem**: "Out of memory error during model loading"
- **Solution 1**: Ensure GPU is enabled (not CPU)
- **Solution 2**: Close other Kaggle notebooks using GPU
- **Solution 3**: Restart kernel: Kernel → Restart & Clear Output
- **Solution 4**: Check you're using P100 GPU (not T4 which has less memory)

**Problem**: "LED model path mismatch" or "FileNotFoundError"
- **Solution**: Your dataset might be named differently
  ```python
  # Run this in a Kaggle cell to find your dataset
  import os
  for root, dirs, files in os.walk('/kaggle/input/'):
      print(root)
  
  # Then update model_loader.py with the correct path
  KAGGLE_PATH = "/kaggle/input/YOUR-ACTUAL-DATASET-NAME/led_model_saved"
  ```

### Backend Issues

**Problem**: "❌ Backend Offline"
- **Solution**: Check that Kaggle notebook is running (Cell 3)
- Verify ngrok URL in `app.py` matches Kaggle output
- Check ngrok auth token is valid

**Problem**: "Module not found: fitz"
- **Solution**: Run Cell 1 completely, ensure PyMuPDF installs correctly
- Restart Kaggle kernel if needed

**Problem**: Models loading slowly
- **Solution**: First run takes ~2-3 minutes to download models
- Subsequent runs are faster with cached models

### Frontend Issues

**Problem**: Streamlit won't start
- **Solution**: Check Python version (3.9+)
- Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

**Problem**: PDF upload fails
- **Solution**: Ensure file is valid PDF
- Check file size (<100MB recommended)
- Try re-uploading

**Problem**: Summaries look incomplete
- **Solution**: This is a known issue with very long chunks
- The system now merges small chunks to prevent fragmentation
- Try processing fewer pages at once

### ngrok Issues

**Problem**: "Invalid authtoken"
- **Solution**: Verify token copied correctly from dashboard.ngrok.com
- Check for extra spaces or quotes

**Problem**: Domain already in use
- **Solution**: Stop other ngrok instances
- Or use a different domain/remove domain parameter

**Problem**: Free tier limits
- **Solution**: ngrok free tier allows:
  - 1 online ngrok process
  - 40 connections/minute
  - Random URLs (unless you reserve a domain)

---

## 🔐 Security Notes

- **Never commit ngrok tokens** to public repositories
- Use environment variables for sensitive data:
  ```python
  import os
  NGROK_TOKEN = os.getenv("NGROK_TOKEN")
  ```
- Consider using ngrok's IP restrictions for production
- Backend has no authentication - don't expose sensitive data

---

## 📝 Configuration Options

### Model Settings (in `model_loader.py`)

```python
# Adjust beam search quality vs. speed
num_beams = 4  # Higher = better quality, slower

# Summary length
max_length = 512  # Maximum summary tokens
min_length = 20   # Minimum summary tokens

# Brevity control
length_penalty = 0.8  # Lower = more concise
```

### Chunking Settings (in `main_pipeline.py`)

```python
# Chunk size
chunk_size = 200  # Words per chunk

# Minimum chunk for summarization
if word_count < 50:  # Smaller chunks just copied
```

### UI Customization (in `app.py`)

```python
# Change color scheme
colors = ['green', 'blue', 'yellow', 'pink']

# Adjust panel heights
min-height: 600px;
max-height: 800px;
```

---

## 🚧 Known Limitations

### Current System (PyMuPDF Parser)
1. **PDF Only**: Currently only supports PDF format
2. **English Text**: LED model trained primarily on English
3. **Academic Bias**: Fine-tuned on arXiv papers, works best on technical content
4. **Table Summarization**: Tables are filtered out, not summarized
5. **Image Content**: Text in images (scanned PDFs) not extracted
6. **Mathematical Equations**: Complex math may be replaced with [MATH] placeholder
7. **UI Polish**: Interface is functional but not production-grade

### Future Improvements (GROBID Parser - In Development)
The upcoming GROBID-based parser aims to address:
- Better citation and reference extraction
- Improved section structure recognition
- Enhanced handling of complex document layouts
- More accurate metadata extraction

**Note**: GROBID parser is experimental and not yet available in the main release.

---

## 🛣️ Roadmap

### 🔄 In Progress
- [ ] **GROBID Parser Integration** - Alternative parser for better academic document structure extraction (experimental)
- [ ] UI/UX polish and refinement
- [ ] Error handling improvements

### 🎯 Planned Features
- [ ] Add OCR support for scanned PDFs
- [ ] Multi-language support
- [ ] Export summaries to Word/PDF
- [ ] User authentication and session management
- [ ] Direct Google Drive integration
- [ ] Custom model fine-tuning interface
- [ ] Batch processing via API
- [ ] Summary quality scoring

### ⏰ Timeline Note
As a solo-developed project, feature implementation takes time. Priorities may shift based on community feedback and personal availability. Contributions are encouraged to speed up development!

---

## 📚 Tech Stack

### Frontend
- **Streamlit**: Interactive web interface
- **Requests**: HTTP communication with backend
- **PyMuPDF (fitz)**: PDF page counting

### Backend
- **FastAPI**: High-performance API framework
- **PyMuPDF**: Advanced PDF parsing
- **Transformers**: HuggingFace model interface
- **PyTorch**: Deep learning framework
- **KeyBERT**: Keyword extraction
- **Sentence-Transformers**: Semantic embeddings

### Infrastructure
- **ngrok**: Secure tunneling
- **Kaggle**: Free GPU compute (P100)
- **Git/GitHub**: Version control

---

## 🤝 Contributing

**VeriSum is a solo-developed project and contributions are very welcome!** Whether it's fixing a typo, improving the UI, or adding major features - all help is appreciated.

### Why Contribute?
- Help improve a tool that benefits the community
- Learn about document processing, NLP, and AI integration
- Collaborate on real-world ML applications
- Your contributions will have immediate impact

### Areas That Need Help
- 🎨 **UI/UX Design**: Polish the interface, improve user experience
- 🔧 **Parser Development**: Help integrate GROBID or improve PyMuPDF parsing
- 📝 **Documentation**: Improve guides, add examples, write tutorials
- 🐛 **Testing**: Find bugs, test edge cases, validate outputs
- ⚡ **Performance**: Optimize chunking, improve speed, reduce memory usage
- 🌍 **Localization**: Add multi-language support

### How to Contribute

1. **Fork the repository**
   ```bash
   # Click 'Fork' on GitHub, then:
   git clone https://github.com/YOUR-USERNAME/verisum.git
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature-name
   ```

3. **Make your changes**
   - Follow existing code style
   - Test thoroughly (especially with different PDF types)
   - Comment your code where needed

4. **Commit with clear messages**
   ```bash
   git commit -m "Add feature-name: brief description"
   ```

5. **Push and open a Pull Request**
   ```bash
   git push origin feature-name
   ```
   Then open a PR on GitHub with a description of your changes

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/verisum.git
cd verisum

# Create branch
git checkout -b my-feature

# Install dev dependencies
pip install -r requirements.txt
pip install black flake8 pytest  # Code formatting and testing

# Make changes and test
streamlit run app.py

# Format code
black .
flake8 .

# Commit and push
git add .
git commit -m "Description of changes"
git push origin my-feature
```

### Code Style Guidelines
- Use descriptive variable names
- Add docstrings to functions
- Keep functions focused and small
- Comment complex logic
- Format with `black` before committing

### Testing Your Changes
Before submitting:
- [ ] Test with multiple PDF types (single-column, two-column, scanned)
- [ ] Test with different page ranges
- [ ] Verify backend connection works
- [ ] Check for console errors
- [ ] Ensure summaries are coherent

### Questions?
- Open a [GitHub Discussion](https://github.com/Rohitdhawan47/verisum/discussions)
- Comment on related issues
- Reach out through Kaggle

**Remember**: This is a learning-friendly project. Don't be afraid to ask questions or submit imperfect PRs - we'll work through improvements together!

---

## 📄 License

This project is open-source and available under the MIT License.

---

## 👨‍💻 Author

**Rohit Dhawan**
- GitHub: [@Rohitdhawan47](https://github.com/Rohitdhawan47)
- Kaggle: [rohitdhawan23](https://www.kaggle.com/rohitdhawan23)

---

## 🙏 Acknowledgments

- **HuggingFace**: For the Transformers library and LED model
- **Anthropic**: For inspiration from Claude's document analysis
- **Kaggle**: For providing free GPU resources
- **ngrok**: For making backend tunneling simple
- **Streamlit**: For the amazing frontend framework

---

## 📞 Support

Having issues? Here's how to get help:

1. **Check Troubleshooting**: See the section above
2. **GitHub Issues**: [Open an issue](https://github.com/Rohitdhawan47/verisum/issues)
3. **Kaggle Notebook**: Comment on the [notebook](https://www.kaggle.com/code/rohitdhawan23/verisum)

---

## ⭐ Star History

If you find this project useful, please consider giving it a star on GitHub!

---

**Built with ❤️ using AI and Python**
