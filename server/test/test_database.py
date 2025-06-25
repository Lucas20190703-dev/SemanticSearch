import sys, os
import random
import string
import tempfile

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sentence_transformers import SentenceTransformer
from database.mongodb import MongoDB
from config import CORPUS_FILE, TSDAE_MODEL_DIR

model = SentenceTransformer(TSDAE_MODEL_DIR, device="cpu")

with open(CORPUS_FILE, encoding="utf-8") as f:
    sentences = [line.strip() for line in f if line.strip()]
    
    
def generate_random_filename(extension_list=None, length=10):
    if extension_list is None:
        extension_list = ["jpg", "png", "mp4", "avi"]

    name = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    ext = random.choice(extension_list)
    return f"{name}.{ext}"

def generate_random_file_path(directory=None, extension_list=None):
    if directory is None:
        directory = tempfile.gettempdir()  # default system temp dir

    filename = generate_random_filename(extension_list)
    return os.path.join(directory, filename)

def generate_random_creator():
    creators = ["Alex", "Bob", "Lucas", "John", "Felix", "Jack", "William", "Unknown"]
    
    return random.choice(creators)

def generate_random_writer():
    writers = ["Don", "Serhii", "Peter", "Bart", "Denver", "Unknown"]
    return random.choice(writers)

def generate_random_kewords():
    keywords = ["delete", "remove", "clear", "student", "application", "computer", "science", "desktop", "Unknown"]
    return random.choices(keywords)
    
def generate_random_categories():
    categories = ["Economic", "Factory", "Agriculture", "Document", "Construct", "Concert", "Unknown"]
    return random.choices(categories)

def generate_random_caption():
    return random.choice(sentences)

def insert_data():
    
    for _ in range(1000):
        caption = caption = generate_random_caption()
        embedding = model.encode(caption, convert_to_numpy=True).reshape(1, -1).tolist()
        database.insert(
            path = generate_random_file_path(),
            creator = generate_random_creator(),
            caption = caption,
            writer = generate_random_writer(),
            categories = generate_random_categories(),
            keywords = generate_random_kewords(),
            embedding = embedding
        )
    
    
if __name__ == "__main__":
    database = MongoDB()
    
    # database.documents.drop()
    database.clear()
    
    # insert random data
    insert_data()
    
    database.lookup()
    
    
    
    
    
    
    

