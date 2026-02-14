import streamlit as st
import torch
from transformers import LEDForConditionalGeneration, LEDTokenizer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from peft import PeftModel
from keybert import KeyBERT 
import os

@st.cache_resource
def load_summarizer():
    # PATHS
    KAGGLE_PATH = "/kaggle/input/led-arxiv-model/led_model_saved"
    BACKUP_ID = "allenai/led-large-16384-arxiv"
    
    print(f"--- 🔄 Loading LED Model (P100 Optimized / FP32) ---")

    # 1. Determine Path
    if os.path.exists(KAGGLE_PATH):
        print(f"✅ Found saved model at: {KAGGLE_PATH}")
        load_path = KAGGLE_PATH
    else:
        print(f"⬇️ Downloading from HuggingFace (Backup)...")
        load_path = BACKUP_ID

    # 2. Load Tokenizer
    tokenizer = LEDTokenizer.from_pretrained(load_path)

    # 3. Load Model -- P100 OPTIMIZATION HERE
    # - We removed 'torch_dtype=torch.float16' (Crashes P100)
    # - We use 'torch_dtype=torch.float32' (Native Speed for P100)
    # - We explicitly send to .to("cuda")
    try:
        model = LEDForConditionalGeneration.from_pretrained(
            load_path,
            torch_dtype=torch.float32  # <--- CRITICAL CHANGE FOR P100
        ).to("cuda")
        
        # 4. optimize Generation Config for P100
        # P100 has high memory bandwidth, so we can afford slightly better search beams
        try:
            model.generation_config = GenerationConfig.from_pretrained(load_path)
            model.generation_config.max_length = 512
            model.generation_config.num_beams = 4 # Keep 4 for quality, P100 handles it easily
            # Ensure the model knows it's generating text
            model.generation_config.early_stopping = True
            model.generation_config.no_repeat_ngram_size = 3
        except:
            pass 

        print("🚀 Model Loaded Successfully on P100 GPU (Float32 Mode)!")
        return model, tokenizer

    except Exception as e:
        print(f"❌ CRITICAL ERROR loading model: {e}")
        return None, None

@st.cache_resource
def load_keybert():
    """
    Loads KeyBERT (CPU-light, but can use GPU if available)
    """
    print("Loading KeyBERT...")
    model = KeyBERT(model='all-MiniLM-L6-v2') # Explicitly using a fast, small model
    return model
