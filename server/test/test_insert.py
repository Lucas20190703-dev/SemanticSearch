from services.faiss_service import HybridSearchEngine

if __name__ == "__main__":
    engine = HybridSearchEngine()
    
    while True:
        q = input("🔍 Enter query (or 'exit'): ")
        if q.lower() == 'exit':
            break

        results = engine.query(q)
        print("\n📄 Top Matches:\n")
        for i, (doc_id, text, score) in enumerate(results, 1):
            print(f"🔹 Rank {i} | ID: {doc_id} | Score: {score:.4f}")
            print(f"   → {text}\n")

    engine.close()