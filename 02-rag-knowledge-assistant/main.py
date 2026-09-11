from rag.ingest import build_chunks
from rag.vector_store import VectorStore
from rag.query_engine import QueryEngine

if __name__ == "__main__":
    print("Building knowledge index from ./docs ...")
    chunks = build_chunks()
    store = VectorStore()
    store.build(chunks)
    engine = QueryEngine(store)

    questions = [
        "How many paid leave days do I get per year?",
        "Can I work remotely from another country?",
        "What's the meal expense limit during business travel?",
    ]
    for q in questions:
        print(f"\nQ: {q}")
        print(f"A: {engine.answer(q)}")
