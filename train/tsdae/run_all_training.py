# run_all_training.py

"""
🚀 One-Step Pipeline Runner
Runs tokenizer, MLM, and TSDAE training in sequence.

Ensure:
- data/corpus.txt exists
- config.py is properly set
"""

from train_tokenizer import train_tokenizer
from train_mlm import train_mlm
from train_tsdae import train_tsdae

if __name__ == "__main__":
    print("\n====================")
    print("🔤 1. Training Tokenizer...")
    print("====================")
    train_tokenizer()

    print("\n====================")
    print("📚 2. Training MLM Model...")
    print("====================")
    train_mlm()

    print("\n====================")
    print("🧠 3. Fine-tuning TSDAE...")
    print("====================")
    train_tsdae()

    print("\n✅ All steps completed successfully!")
