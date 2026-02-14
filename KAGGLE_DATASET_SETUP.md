# Quick Guide: LED Model Dataset Setup for Kaggle

This guide helps you set up the LED model as a Kaggle dataset for VeriSum.

## 🎯 Choose Your Method

### ⚡ Method 1: Auto-Download (Easiest - Recommended for Beginners)

**No setup required!** Just run the notebook and let it download automatically.

**Pros:**
- Zero configuration
- Always gets the latest model
- No manual file management

**Cons:**
- First run takes 3-5 minutes to download
- Requires internet access in Kaggle
- Downloads every time you use a new notebook

**Steps:**
1. Run Cell 1 (install dependencies)
2. Run Cell 2 (clone GitHub repo)
3. Run Cell 3 (start server)
4. Wait 3-5 minutes for model download on first run
5. Done! ✅

---

### 🚀 Method 2: Use Existing Kaggle Dataset (Faster)

**Best for**: Frequent use, faster startup times

**Steps:**

#### Step 1: Search for Existing Dataset
```
1. Open your Kaggle notebook
2. Click "+ Add Data" button (right sidebar)
3. Search for: "led-large-16384-arxiv"
4. Look for datasets with these files:
   - config.json
   - pytorch_model.bin
   - tokenizer_config.json
5. Click "Add" on a suitable dataset
```

#### Step 2: Verify Dataset Path
```python
# Run this in a Kaggle cell to check:
import os
print("Available datasets:")
print(os.listdir('/kaggle/input/'))

# You should see something like:
# ['led-arxiv-model', 'other-datasets']
```

#### Step 3: Update model_loader.py (if needed)
If your dataset has a different name, update this line:

```python
# In ai_pipeline/model_loader.py, line ~8:
KAGGLE_PATH = "/kaggle/input/YOUR-DATASET-NAME-HERE/led_model_saved"

# Common paths:
# "/kaggle/input/led-arxiv-model/led_model_saved"
# "/kaggle/input/led-large-16384-arxiv/"
# "/kaggle/input/led-model/"
```

#### Step 4: Test
Run Cell 3 and check for:
```
✅ Found saved model at: /kaggle/input/led-arxiv-model/led_model_saved
🚀 Model Loaded Successfully on P100 GPU (Float32 Mode)!
```

---

### 🔨 Method 3: Create Your Own Dataset (Advanced)

**Best for**: When no dataset exists, you want full control

#### Step 1: Download Model Locally

On your local machine, create a Python script:

```python
# download_led_model.py
from transformers import LEDForConditionalGeneration, LEDTokenizer

print("Downloading LED model...")
model_name = "allenai/led-large-16384-arxiv"

# Download model and tokenizer
model = LEDForConditionalGeneration.from_pretrained(model_name)
tokenizer = LEDTokenizer.from_pretrained(model_name)

# Save to local folder
save_path = "./led_model_saved"
model.save_pretrained(save_path)
tokenizer.save_pretrained(save_path)

print(f"✅ Model saved to {save_path}")
print(f"📦 Size: ~1.6 GB")
```

Run it:
```bash
pip install transformers torch
python download_led_model.py
```

Wait ~5-10 minutes for download.

#### Step 2: Create Kaggle Dataset

1. **Compress (optional but recommended)**:
   ```bash
   # On Windows (PowerShell):
   Compress-Archive -Path led_model_saved -DestinationPath led_model_saved.zip
   
   # On Mac/Linux:
   zip -r led_model_saved.zip led_model_saved/
   ```

2. **Upload to Kaggle**:
   - Go to https://www.kaggle.com/datasets
   - Click "New Dataset"
   - Drag and drop `led_model_saved.zip` or the folder
   - Fill in details:
     - **Title**: "LED Large 16384 ArXiv Model"
     - **Subtitle**: "Fine-tuned Longformer for document summarization"
     - **Description**: "LED model from HuggingFace: allenai/led-large-16384-arxiv"
   - Choose visibility: Public or Private
   - Click "Create"

3. **Add to your VeriSum notebook**:
   - Open your notebook
   - Click "+ Add Data" → "Your Datasets"
   - Select your LED dataset
   - Click "Add"

#### Step 3: Update Path

```python
# In ai_pipeline/model_loader.py:
KAGGLE_PATH = "/kaggle/input/led-large-16384-arxiv-model/led_model_saved"
# Adjust based on your dataset name
```

---

## 🔍 Verification Checklist

After setup, verify everything works:

### ✅ Check 1: Dataset is Mounted
```python
# Run in Kaggle cell:
import os
print(os.listdir('/kaggle/input/'))
# Should show your LED dataset
```

### ✅ Check 2: Model Files Exist
```python
# Run in Kaggle cell:
import os
dataset_path = '/kaggle/input/led-arxiv-model/led_model_saved'  # Adjust name
if os.path.exists(dataset_path):
    print("✅ Dataset found!")
    print("Files:", os.listdir(dataset_path))
else:
    print("❌ Dataset not found at:", dataset_path)
```

Expected files:
- `config.json`
- `pytorch_model.bin` (1.5 GB)
- `tokenizer_config.json`
- `vocab.json`
- `merges.txt`
- `special_tokens_map.json`

### ✅ Check 3: Model Loads Successfully
Run Cell 3 and look for:
```
⏳ WARMING UP MODELS...
✅ Found saved model at: /kaggle/input/...
🚀 Model Loaded Successfully on P100 GPU (Float32 Mode)!
✅ Models Ready!
```

---

## 🐛 Troubleshooting

### "FileNotFoundError: led_model_saved"

**Problem**: Path mismatch between dataset and code

**Solution**:
```python
# Find actual path:
import os
for item in os.listdir('/kaggle/input/'):
    print(f"Dataset: {item}")
    if 'led' in item.lower():
        full_path = f"/kaggle/input/{item}"
        print(f"  Contents: {os.listdir(full_path)}")

# Update model_loader.py with correct path
```

### "Model downloaded but still slow"

**Problem**: Using auto-download instead of dataset

**Check**: Run Cell 3 and look at output:
- ✅ `Found saved model at: /kaggle/input/...` = Using dataset (fast)
- ⬇️ `Downloading from HuggingFace...` = Auto-download (slow)

**Solution**: Add dataset properly (see Method 2)

### "Dataset added but not detected"

**Problem**: Kaggle needs to refresh

**Solution**:
1. Restart kernel: Kernel → Restart
2. Re-run Cell 3
3. Check dataset shows in right sidebar under "Data"

---

## 📊 Comparison: Methods

| Method | Setup Time | First Run | Subsequent Runs | Best For |
|--------|------------|-----------|-----------------|----------|
| Auto-Download | 0 min | 3-5 min | 3-5 min | Beginners, one-time use |
| Existing Dataset | 1 min | 1-2 min | 1-2 min | Regular use, fastest |
| Create Dataset | 30 min | 1-2 min | 1-2 min | Control, sharing with others |

---

## 💡 Pro Tips

1. **For beginners**: Use Method 1 (auto-download) - just run and forget
2. **For frequent use**: Use Method 2 (existing dataset) - saves 2-3 minutes per run
3. **For teams**: Use Method 3 (create dataset) - share one dataset across notebooks
4. **First time**: Method 1 to test, then upgrade to Method 2 if you like it
5. **Save money**: Dataset avoids re-downloading 1.6GB repeatedly (saves Kaggle bandwidth)

---

## 🔗 Useful Links

- **HuggingFace Model**: https://huggingface.co/allenai/led-large-16384-arxiv
- **Kaggle Datasets**: https://www.kaggle.com/datasets
- **Your Kaggle Notebooks**: https://www.kaggle.com/code
- **Kaggle Documentation**: https://www.kaggle.com/docs

---

## ❓ Still Stuck?

1. **Check logs**: Look at Cell 3 output for error messages
2. **GitHub Issues**: https://github.com/Rohitdhawan47/verisum/issues
3. **Kaggle Comments**: Comment on the notebook
4. **Use auto-download**: When in doubt, skip datasets and let it download

---

**Remember**: Auto-download always works as a fallback! Datasets are just for speed optimization.

**Last Updated**: February 2025
