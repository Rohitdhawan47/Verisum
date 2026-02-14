# VeriSum Dependencies Overview

This document explains all dependencies used in the VeriSum project, split between local (frontend) and Kaggle (backend) environments.

## 📦 Local Dependencies (requirements.txt)

Install these on your local machine to run the Streamlit frontend:

```bash
pip install -r requirements.txt
```

### Required Packages:

| Package | Version | Purpose |
|---------|---------|---------|
| `streamlit` | ≥1.31.0 | Web interface framework |
| `requests` | ≥2.31.0 | HTTP communication with backend |
| `PyMuPDF` | ≥1.23.8 | PDF page counting (lightweight usage) |

**Total Size**: ~50 MB  
**Installation Time**: ~1-2 minutes

---

## 🖥️ Kaggle Backend Dependencies

These are installed automatically in the Kaggle notebook (Cell 1). **You don't need to install these locally.**

### Core Dependencies:

```bash
# Critical Fixes
protobuf==3.20.3          # Fix TensorFlow/Protobuf conflicts
PyMuPDF                   # Advanced PDF parsing (full features)

# Server & Networking
pyngrok                   # ngrok tunnel creation
fastapi                   # API framework
uvicorn                   # ASGI server
python-multipart          # File upload handling
nest_asyncio              # Async support in Jupyter
streamlit                 # (For compatibility, not used on backend)

# AI & ML
transformers              # HuggingFace model loading
torch                     # PyTorch deep learning
bitsandbytes              # Model quantization (optional)
accelerate                # Training optimization

# NLP & Keywords  
sentence-transformers     # Semantic embeddings
keybert                   # Keyword extraction

# Vision (Optional)
einops                    # Tensor operations
```

**Total Size**: ~5-8 GB (includes models)  
**Installation Time**: ~3-5 minutes on Kaggle

---

## 🔍 Dependency Details

### Why PyMuPDF appears twice?

- **Local (frontend)**: Only uses `fitz` for counting pages - lightweight
- **Kaggle (backend)**: Full PDF parsing with advanced text extraction

### Why fix protobuf?

```python
!pip uninstall -y protobuf
!pip install protobuf==3.20.3
```

TensorFlow and newer protobuf versions conflict, causing `MessageFactory` errors. Version 3.20.3 is stable.

### Why uninstall `fitz` package?

```python
!pip uninstall -y fitz
!pip install -U PyMuPDF
```

There's a fake `fitz` package on PyPI that conflicts with PyMuPDF's `fitz` module. We uninstall it first.

---

## 📥 Model Downloads (Automatic on Kaggle)

These are downloaded automatically when the backend starts:

1. **LED Model** (`allenai/led-large-16384-arxiv`)
   - Size: ~1.6 GB
   - Cached at: `/kaggle/input/led-arxiv-model/` (if added as dataset)
   
2. **KeyBERT Embeddings** (`all-MiniLM-L6-v2`)
   - Size: ~90 MB
   - Cached automatically by sentence-transformers

3. **Tokenizers**
   - Size: ~5 MB
   - Cached with models

---

## 🐍 Python Version Requirements

| Environment | Python Version | Notes |
|-------------|----------------|-------|
| Local | ≥3.9 | Streamlit requires 3.9+ |
| Kaggle | 3.10.x | Pre-installed on Kaggle |

---

## 💾 Storage Requirements

### Local Machine:
- **Code**: ~5 MB
- **Dependencies**: ~50 MB
- **Total**: ~55 MB

### Kaggle Notebook:
- **Code**: ~5 MB  
- **Dependencies**: ~5 GB
- **Models**: ~1.7 GB
- **Total**: ~6.7 GB (within Kaggle's limits)

---

## 🚀 Quick Start Commands

### Local Setup:
```bash
# Clone repository
git clone https://github.com/Rohitdhawan47/verisum.git
cd verisum

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run frontend
streamlit run app.py
```

### Kaggle Setup:
Just run the three notebook cells in order:
1. Cell 1: Install dependencies (~3-5 min)
2. Cell 2: Clone GitHub repo (~30 sec)
3. Cell 3: Start server (~2 min for model loading)

---

## 🔧 Optional Dependencies

### For Development:

```bash
# Code formatting
pip install black flake8

# Testing
pip install pytest pytest-cov

# Type checking
pip install mypy
```

### For Production:

```bash
# Environment management
pip install python-dotenv

# Logging
pip install loguru

# Monitoring
pip install prometheus-client
```

---

## ⚠️ Common Installation Issues

### Issue 1: Streamlit won't install
```bash
# Solution: Upgrade pip first
pip install --upgrade pip
pip install streamlit
```

### Issue 2: PyMuPDF import error
```bash
# Solution: Reinstall with no-cache
pip uninstall PyMuPDF
pip install PyMuPDF --no-cache-dir
```

### Issue 3: Requests SSL errors
```bash
# Solution: Upgrade certifi
pip install --upgrade certifi
```

### Issue 4: Kaggle kernel crashes during install
```python
# Solution: Install packages one at a time in Cell 1
!pip install -q pyngrok
!pip install -q fastapi
# ... etc
```

---

## 📊 Dependency Tree

```
VeriSum Project
│
├── Local Frontend (requirements.txt)
│   ├── streamlit
│   │   ├── click
│   │   ├── pandas
│   │   └── ... (auto-installed)
│   ├── requests
│   │   ├── urllib3
│   │   ├── certifi
│   │   └── charset-normalizer
│   └── PyMuPDF (fitz)
│       └── minimal dependencies
│
└── Kaggle Backend (Cell 1)
    ├── transformers
    │   ├── torch
    │   ├── numpy
    │   ├── tokenizers
    │   └── ... (many dependencies)
    ├── fastapi
    │   ├── starlette
    │   ├── pydantic
    │   └── uvicorn
    ├── keybert
    │   ├── sentence-transformers
    │   ├── scikit-learn
    │   └── torch
    └── PyMuPDF (full features)
```

---

## 🔄 Updating Dependencies

### Local:
```bash
# Update all packages
pip install --upgrade -r requirements.txt

# Update specific package
pip install --upgrade streamlit
```

### Kaggle:
Simply re-run Cell 1 with updated version numbers.

---

## 📝 Notes

1. **Virtual Environment Recommended**: Keeps local dependencies isolated
2. **Kaggle Auto-Installs**: Most ML packages are pre-installed on Kaggle
3. **Model Caching**: First run is slow, subsequent runs are fast
4. **Offline Mode**: Backend won't work offline (needs ngrok)

---

## 🆘 Support

If you encounter dependency issues:
1. Check Python version: `python --version`
2. Check pip version: `pip --version`
3. Try clean install: `pip install -r requirements.txt --force-reinstall`
4. Open an issue on [GitHub](https://github.com/Rohitdhawan47/verisum/issues)

---

**Last Updated**: February 2026
