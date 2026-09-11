"""RAG query engine: retrieve relevant chunks, then generate a grounded answer."""
import os

try:
    import anthropic
except ImportError:
    anthropic = None

SYSTEM_PROMPT = (
    "You are an internal company knowledge assistant. "
    "Answer the employee's question using ONLY the provided context. "
    "If the answer isn't in the context, say you don't have that information "
    "and suggest they contact HR/the relevant team. "
    "Always mention which source document(s) you used."
)


class QueryEngine:
    def __init__(self, vector_store, model: str = "claude-sonnet-4-6"):
        self.vector_store = vector_store
        self.model = model
        self.api_key = os.environ.get("ANTHROPIC_API_KEY")
        self.client = anthropic.Anthropic() if (anthropic and self.api_key) else None

    def answer(self, question: str, top_k: int = 3) -> str:
        results = self.vector_store.search(question, top_k=top_k)
        context = "\n\n".join(
            f"[Source: {r['source']}]\n{r['text']}" for r in results
        )

        if self.client:
            resp = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                system=SYSTEM_PROMPT,
                messages=[{
                    "role": "user",
                    "content": f"Context:\n{context}\n\nQuestion: {question}",
                }],
            )
            return resp.content[0].text

        # Fallback (no API key): show retrieved context directly
        sources = ", ".join(sorted({r["source"] for r in results}))
        return (
            f"[No ANTHROPIC_API_KEY set — showing raw retrieved context]\n\n"
            f"Most relevant sources: {sources}\n\n{context}"
        )
