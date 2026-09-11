"""Fusion Engine
Combines text, image, and audio signals into ONE business insight.
"""
import os

try:
    import anthropic
except ImportError:
    anthropic = None

from .text_analyzer import TextAnalyzer
from .image_analyzer import ImageAnalyzer
from .audio_analyzer import AudioAnalyzer

SYSTEM_PROMPT = (
    "You are a business insight analyst. Given signals extracted from a "
    "customer's text review, product photo notes, and support call transcript, "
    "write a 2-3 sentence combined business insight: what's the real underlying "
    "issue, how severe/urgent is it, and what action should the business take?"
)


class FusionEngine:
    def __init__(self, model: str = "claude-sonnet-4-6"):
        self.text_analyzer = TextAnalyzer()
        self.image_analyzer = ImageAnalyzer()
        self.audio_analyzer = AudioAnalyzer()
        self.model = model
        self.api_key = os.environ.get("ANTHROPIC_API_KEY")
        self.client = anthropic.Anthropic() if (anthropic and self.api_key) else None

    def analyze(self, record: dict) -> dict:
        text_result = self.text_analyzer.analyze(record["text_review"])
        image_result = self.image_analyzer.analyze_note(record["image_note"])
        audio_result = self.audio_analyzer.analyze_transcript(record["call_transcript"])

        # Simple severity heuristic combining all 3 modalities
        severity = 0
        severity += 1 if text_result["sentiment"] == "negative" else 0
        severity += 1 if image_result["has_quality_issue"] else 0
        severity += 1 if audio_result["is_urgent"] else 0

        combined = {
            "product": record.get("product", "Unknown"),
            "text_signal": text_result,
            "image_signal": image_result,
            "audio_signal": audio_result,
            "severity_score": severity,  # 0-3
        }

        combined["business_insight"] = self._generate_insight(combined)
        return combined

    def _generate_insight(self, combined: dict) -> str:
        if self.client:
            prompt = (
                f"Product: {combined['product']}\n"
                f"Text sentiment: {combined['text_signal']['sentiment']} "
                f"(signals: {combined['text_signal']['negative_signals']})\n"
                f"Image issues: {combined['image_signal']['detected_issues']}\n"
                f"Call transcript urgency: {combined['audio_signal']['urgency_signals']}\n"
                f"Combined severity (0-3): {combined['severity_score']}"
            )
            resp = self.client.messages.create(
                model=self.model,
                max_tokens=200,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}],
            )
            return resp.content[0].text

        # Fallback rule-based insight when no API key set
        if combined["severity_score"] >= 2:
            return (
                f"[Rule-based] {combined['product']}: Multiple negative signals "
                f"detected across text/image/audio — high-priority quality issue, "
                f"recommend immediate replacement/refund and root-cause review."
            )
        return (
            f"[Rule-based] {combined['product']}: Low combined severity — "
            f"routine follow-up sufficient."
        )
