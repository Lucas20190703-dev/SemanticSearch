from sentence_transformers import SentenceTransformer
from config import TSDAE_MODEL_DIR, CORPUS_FILE

model = SentenceTransformer(TSDAE_MODEL_DIR, device="cpu")

with open(CORPUS_FILE, encoding="utf-8") as f:
    sentences = [line.strip() for line in f if line.strip()]