# train/train_mlm.py

"""
====================================
🧠 BERT Pretraining (MLM) Script
====================================

This script trains a BERT-like language model from scratch using Masked Language Modeling (MLM).
It's ideal for unsupervised pretraining on a domain-specific or non-English corpus.

📥 Input:
- `data/corpus.txt` (one sentence per line)
- Trained tokenizer in `models/tokenizer/`

📤 Output:
- MLM-pretrained BERT model in: models/bert-mlm/

⚙️ Configuration:
- 6 transformer layers, 12 attention heads
- Vocab size inferred from tokenizer
- Max position: 512 tokens
- Trained using Hugging Face Transformers `Trainer`

🛠 Usage:
$ python train/train_mlm.py

Make sure your tokenizer is trained and saved before running this.
Edit `config.py` to adjust training parameters or paths.
"""

# train/train_mlm.py

from transformers import (
    BertTokenizerFast, BertConfig, BertForMaskedLM,
    DataCollatorForLanguageModeling, Trainer, TrainingArguments
)
from datasets import load_dataset
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import (
    BERT_MLM_MODEL_DIR, TOKENIZER_DIR, TOKENIZER_FILE,
    CORPUS_FILE, MAX_SEQ_LENGTH, EMBEDDING_DIM
)

def train_mlm():
    tokenizer = BertTokenizerFast.from_pretrained(TOKENIZER_DIR)
    dataset = load_dataset("text", data_files={"train": CORPUS_FILE})

    def tokenize_function(examples):
        return tokenizer(
            examples["text"],
            padding="max_length",
            truncation=True,
            max_length=MAX_SEQ_LENGTH
        )

    dataset = dataset.map(tokenize_function, batched=True)

    config = BertConfig(
        vocab_size=tokenizer.vocab_size,
        max_position_embeddings=MAX_SEQ_LENGTH,
        hidden_size=EMBEDDING_DIM,
        num_attention_heads=12,
        num_hidden_layers=6,
        type_vocab_size=1
    )
    model = BertForMaskedLM(config)

    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm_probability=0.15)

    training_args = TrainingArguments(
        output_dir=BERT_MLM_MODEL_DIR,
        overwrite_output_dir=True,
        num_train_epochs=3,
        per_device_train_batch_size=32,
        save_steps=1000,
        save_total_limit=2,
        logging_dir="./logs"
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset["train"],
        data_collator=data_collator
    )

    trainer.train()
    model.save_pretrained(BERT_MLM_MODEL_DIR)
    
    # The DenoisingAutoEncoderLoss needs to load a decoder model from the checkpoint at BERT_MLM_MODEL_DIR. 
    # But BERT_MLM_MODEL_DIR contains only the model weights (pytorch_model.bin, config.json), 
    # and not the tokenizer files. 
    # And SentenceTransformers internally attempts to load both the model and its tokenizer from this path.
    # ensure TSDAE can find tokenizer
    tokenizer.save_pretrained(BERT_MLM_MODEL_DIR)

    print("✅ MLM model training complete.")

if __name__ == "__main__":
    train_mlm()
