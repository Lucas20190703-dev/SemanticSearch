# train/train_tsdae.py

"""
====================================
🧠 TSDAE Sentence Embedding Training
====================================

This script fine-tunes the MLM model using TSDAE (Transformer-based Denoising AutoEncoder)
to generate high-quality sentence embeddings suitable for semantic search and clustering.

📥 Input:
- `data/corpus.txt` (same as used for tokenizer and MLM)
- Pretrained MLM model: `models/bert-mlm/`
- Trained tokenizer: `models/tokenizer/`

📤 Output:
- Fine-tuned sentence embedding model (TSDAE) saved to: models/tsdae/

⚙️ Key Details:
- SentenceTransformers framework
- No labeled data needed (unsupervised)
- Learns to reconstruct noised input sentences
- Outputs dense vector embeddings for each sentence

🛠 Usage:
$ python train/train_tsdae.py

Ensure both tokenizer and MLM model are trained beforehand.
Paths are controlled by `config.py`.
"""
# train/train_tsdae.py

from sentence_transformers import models, SentenceTransformer, losses, InputExample
from torch.utils.data import DataLoader, Dataset
import random
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import TSDAE_MODEL_DIR, CORPUS_FILE, BERT_MLM_MODEL_DIR, MAX_SEQ_LENGTH

# Enhanced denoising dataset (no NLTK) with word drop, shuffle, and mask
class SimpleDenoisingDataset(Dataset):
    def __init__(self, sentences):
        self.examples = []
        for s in sentences:
            noised = self.add_noise(s)
            self.examples.append(InputExample(texts=[noised, s]))

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, idx):
        return self.examples[idx]

    def add_noise(self, sentence):
        words = sentence.strip().split()
        if len(words) < 5:
            return sentence

        # 1. Randomly drop words
        keep_prob = 0.8
        words = [w for w in words if random.random() < keep_prob]

        # 2. Random masking
        mask_prob = 0.2
        masked = []
        for w in words:
            if random.random() < mask_prob:
                masked.append("[MASK]")
            else:
                masked.append(w)

        # 3. Slight shuffle
        if len(masked) > 4:
            idxs = list(range(len(masked)))
            random.shuffle(idxs)
            masked = [masked[i] for i in idxs]

        return " ".join(masked)

def train_tsdae():
    word_embedding_model = models.Transformer(
        model_name_or_path=BERT_MLM_MODEL_DIR,
        max_seq_length=MAX_SEQ_LENGTH
    )
    pooling_model = models.Pooling(
        word_embedding_model.get_word_embedding_dimension(),
        pooling_mode='mean'
    )

    model = SentenceTransformer(modules=[word_embedding_model, pooling_model])

    with open(CORPUS_FILE, encoding="utf-8") as f:
        sentences = [line.strip() for line in f if line.strip()]

    train_dataset = SimpleDenoisingDataset(sentences)
    train_dataloader = DataLoader(train_dataset, batch_size=32, shuffle=True)

    train_loss = losses.DenoisingAutoEncoderLoss(model, decoder_name_or_path=BERT_MLM_MODEL_DIR)

    model.fit(
        train_objectives=[(train_dataloader, train_loss)],
        epochs=1,
        weight_decay=0.01,
        scheduler='warmupcosine',
        warmup_steps=100,
        output_path=TSDAE_MODEL_DIR
    )

    os.makedirs(TSDAE_MODEL_DIR, exist_ok=True)
    model.save(TSDAE_MODEL_DIR)

    print("✅ TSDAE training complete.")

if __name__ == "__main__":
    train_tsdae()
