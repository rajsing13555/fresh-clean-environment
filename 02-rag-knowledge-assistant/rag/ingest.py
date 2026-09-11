"""Document ingestion & chunking."""
from pathlib import Path

DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"


def load_documents(docs_dir: Path = DOCS_DIR) -> list[dict]:
    """Load all .txt/.md files as {source, text} dicts."""
    documents = []
    for path in sorted(docs_dir.glob("*")):
        if path.suffix in (".txt", ".md"):
            documents.append({"source": path.name, "text": path.read_text()})
    return documents


def chunk_text(text: str, chunk_size: int = 300, overlap: int = 50) -> list[str]:
    """Simple sliding-window word chunker."""
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks or [text]


def build_chunks(docs_dir: Path = DOCS_DIR) -> list[dict]:
    """Return list of {source, chunk_text} for all documents."""
    all_chunks = []
    for doc in load_documents(docs_dir):
        for chunk in chunk_text(doc["text"]):
            all_chunks.append({"source": doc["source"], "text": chunk})
    return all_chunks
