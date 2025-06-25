from sentence_transformers import SentenceTransformer

# Load the TSDAE BERT model from Hugging Face
model = SentenceTransformer('tartspuppy/bert-base-uncased-tsdae-encoder')

# Save the model to a local directory
model.save('tsdae-bert-base-uncased-local')