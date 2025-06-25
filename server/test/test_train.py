# test_train.py

from sentence_transformers import SentenceTransformer
from torch.nn.functional import cosine_similarity
import torch

# Load trained TSDAE model
model = SentenceTransformer("models/tsdae/", device="cuda")

# Test sentences
sentences = [
    "The cat sat on the mat.",
    "A feline was resting on the rug.",
    "Today is a sunny day.",
    "Quantum physics is fascinating."
]

# Generate embeddings
embeddings = model.encode(sentences, convert_to_tensor=True)

# Compare similarity between the first sentence and the rest
print("\nCosine Similarities:")
for i in range(1, len(sentences)):
    sim = cosine_similarity(embeddings[0], embeddings[i], dim=0)
    print(f" - Sentence 0 vs {i}: {sim.item():.4f}")
