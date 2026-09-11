"""Email Agent
Drafts context-aware replies to customer emails using Claude.
Falls back to a template-based draft if no API key is configured,
so the project still runs end-to-end without credentials.
"""
import os

try:
    import anthropic
except ImportError:
    anthropic = None


SYSTEM_PROMPT = (
    "You are a helpful, professional customer support assistant. "
    "Draft a concise, empathetic reply to the customer's email below. "
    "Do not invent order numbers or facts you don't have."
)


class EmailAgent:
    def __init__(self, model: str = "claude-sonnet-4-6"):
        self.model = model
        self.api_key = os.environ.get("ANTHROPIC_API_KEY")
        self.client = anthropic.Anthropic() if (anthropic and self.api_key) else None

    def draft_reply(self, customer_email: str) -> str:
        if self.client:
            resp = self.client.messages.create(
                model=self.model,
                max_tokens=400,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": customer_email}],
            )
            return resp.content[0].text
        # Fallback template draft when no API key is set
        return (
            "Hi there,\n\nThanks for reaching out! We've received your message:\n"
            f'"{customer_email.strip()}"\n\n'
            "Our team is looking into this and will follow up shortly.\n\n"
            "Best regards,\nSupport Team\n\n"
            "[NOTE: Set ANTHROPIC_API_KEY to enable AI-generated replies]"
        )

    def run(self, inbox: list[str]) -> list[dict]:
        drafts = []
        for email in inbox:
            draft = self.draft_reply(email)
            drafts.append({"incoming": email, "draft_reply": draft})
            print(f"[EmailAgent] Draft ready for: {email[:50]}...")
        return drafts


if __name__ == "__main__":
    sample_inbox = [
        "Hi, my order #1234 hasn't arrived yet, it's been 2 weeks. Can you help?",
        "Do you offer bulk discounts for orders over 100 units?",
    ]
    EmailAgent().run(sample_inbox)
