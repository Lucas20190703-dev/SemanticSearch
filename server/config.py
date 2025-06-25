# config.py

import os

# 📁 Paths
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Input corpus
CORPUS_FILE = os.path.join(BASE_DIR, "data", "corpus.txt")

# Tokenizer
TOKENIZER_DIR = os.path.join(BASE_DIR, "models", "tokenizer")
TOKENIZER_FILE = os.path.join(TOKENIZER_DIR, "tokenizer.json")
VOCABULARY_SIZE = 32000  # or adjust as needed

# MLM model output
BERT_MLM_MODEL_DIR = os.path.join(BASE_DIR, "models", "bert-mlm")

# TSDAE model output
TSDAE_MODEL_DIR = os.path.join(BASE_DIR, "models", "tsdae")
#TSDAE_MODEL_DIR = os.path.join(BASE_DIR, "tsdae-bert-base-uncased-local")

# 📏 Model Hyperparameters
MAX_SEQ_LENGTH = 128
EMBEDDING_DIM = 768  # Hidden size for BERT config

# (Optional) Logging
LOGGING_DIR = os.path.join(BASE_DIR, "logs")

# Faiss 
FAISS_INDEX_PATH = os.path.join(BASE_DIR, "models", "faiss.index")
FAISS_IVF_INDEX_PATH = os.path.join(BASE_DIR, "models", "faiss_ivf.index")

# Filter
TOP_K = 30

# Database
MONGO_DB_NAME = "Semantic"

MONGO_DB_PORT = 27017

MONGO_DB_HOST = "mongodb://localhost"

PSQL_DB_CONFIG = {
    "db_name": "semanticsearch",
    "user": "semantic",
    "password": "123456",
    "host": "localhost",
    "port": 5432
}


# Root Directory
FILE_ROOT_DIR = "."