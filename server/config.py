import os
from pathlib import Path

# -----------------------------
# Base directories
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"

# -----------------------------
# Input corpus
# -----------------------------
CORPUS_FILE = DATA_DIR / "corpus.txt"

# -----------------------------
# Tokenizer / Model paths
# -----------------------------
TOKENIZER_DIR = DATA_DIR / "tokenizer"
TOKENIZER_FILE = TOKENIZER_DIR / "tokenizer.json"
VOCABULARY_SIZE = 32000

# MLM model output
BERT_MLM_MODEL_DIR = DATA_DIR / "bert-mlm"

# TSDAE model output
TSDAE_MODEL_DIR = DATA_DIR / "tsdae"

# -----------------------------
# Model Hyperparameters
# -----------------------------
MAX_SEQ_LENGTH = 128
EMBEDDING_DIM = 768  # matches BERT hidden size

# -----------------------------
# FAISS
# -----------------------------
FAISS_INDEX_PATH = DATA_DIR / "faiss.index"
FAISS_IVF_INDEX_PATH = DATA_DIR / "faiss_ivf.index"
TOP_K = 30

# -----------------------------
# Database (MongoDB only)
# -----------------------------
MONGO_DB_NAME = "Semantic"
MONGO_DB_PORT = 27017
MONGO_DB_HOST = "mongodb://localhost"

# -----------------------------
# File root directory (for browsing)
# -----------------------------
FILE_ROOT_DIR = Path("E:/Test/Images").resolve()

# -----------------------------
# Logging
# -----------------------------
LOGS_DIR.mkdir(exist_ok=True)

# -----------------------------
# API Token for protected endpoints
# -----------------------------
API_TOKEN = "my-secret-token"
