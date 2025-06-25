# train/train_tokenizer.py

"""
====================================
🧠 Tokenizer Training Script
====================================

Train a custom subword tokenizer (BPE or Unigram) using the Hugging Face Tokenizers library.
This tokenizer is required to tokenize your corpus effectively for languages not well-covered by
existing pretrained models (e.g., Korean, Chinese, specialized domains).

📥 Input:
- Plain text corpus file (one sentence per line), default: data/corpus.txt

📤 Output:
- Trained tokenizer files saved under: models/tokenizer/

⚙️ Main Components:
- BPE tokenization model
- Whitespace pre-tokenizer
- Vocabulary size: 30,000

🛠 Usage:
$ python train/train_tokenizer.py

Make sure your `CORPUS_FILE` and `TOKENIZER_DIR` are correctly set in `config.py`.
"""


from tokenizers import Tokenizer, models, trainers, pre_tokenizers, normalizers

from transformers import BertTokenizerFast

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import CORPUS_FILE, TOKENIZER_DIR, TOKENIZER_FILE, VOCABULARY_SIZE

def train_tokenizer():
    tokenizer = Tokenizer(models.BPE())
    tokenizer.normalizer = normalizers.Sequence([normalizers.NFD(), normalizers.Lowercase(), normalizers.Strip()])
    tokenizer.pre_tokenizer = pre_tokenizers.Whitespace()

    trainer = trainers.BpeTrainer(
        vocab_size=VOCABULARY_SIZE, 
        special_tokens=["[PAD]", "[UNK]", "[CLS]", "[SEP]", "[MASK]"]
    )
    tokenizer.train([CORPUS_FILE], trainer)

    os.makedirs(TOKENIZER_DIR, exist_ok=True)
    tokenizer.save(TOKENIZER_FILE)

    # Save in Hugging Face format
    hf_tokenizer = BertTokenizerFast(tokenizer_file=TOKENIZER_FILE)
    hf_tokenizer.save_pretrained(TOKENIZER_DIR)
    
    print("✅ Tokenizer training complete")

if __name__ == "__main__":
    train_tokenizer()
