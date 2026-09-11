"""Text modality: sentiment + keyword extraction from customer reviews."""

POSITIVE_WORDS = {"amazing", "great", "love", "excellent", "good", "fast", "happy"}
NEGATIVE_WORDS = {"disappointed", "bad", "slow", "drains", "broken", "poor", "stopped"}


class TextAnalyzer:
    def analyze(self, text: str) -> dict:
        words = {w.strip(".,!?").lower() for w in text.split()}
        pos_hits = words & POSITIVE_WORDS
        neg_hits = words & NEGATIVE_WORDS

        score = len(pos_hits) - len(neg_hits)
        if score > 0:
            sentiment = "positive"
        elif score < 0:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        return {
            "sentiment": sentiment,
            "sentiment_score": score,
            "positive_signals": sorted(pos_hits),
            "negative_signals": sorted(neg_hits),
        }
