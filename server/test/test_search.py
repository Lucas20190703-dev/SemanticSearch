
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from search.hybrid_search import HybridSearchEngine
from app.file_system import *


def test_search():    
    engine = HybridSearchEngine()

    while True:
        q = input("🔍 Enter query (or 'exit'): ")
        if q.lower() == 'exit':
            break

        results = engine.search(q)
        print("\n📄 Top Matches:\n")
        i = 1
        for res in results:
            faiss_id = res["faiss_id"]
            score = res["score"]
            name = res["name"]
            caption = res.get("caption")
            
            print(f"🔹 Rank {i} | ID: {faiss_id} | Score: {score:.4f} | Path: {name}")
            print(f"   → {caption}\n")
            i += 1

    engine.close()
    
    
def test_api():
    # fetch directories
    print("*******************************")
    print(f"Test: directories in {str(ROOT_DIR)}")
    dirs = get_directory_structure(ROOT_DIR)
    
    print(dirs)
    
    dir = (ROOT_DIR / "Images" / "1").resolve()
    
    print("*******************************")
    print(f"Files (Image and Video) in {str(dir)}")
    
    files = get_files_from_directory(dir)
    
    print (files)
    
    
    
if __name__ == "__main__":
    # test_search()
    
    test_api()