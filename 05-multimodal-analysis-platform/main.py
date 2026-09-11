import json
from multimodal.fusion_engine import FusionEngine

if __name__ == "__main__":
    with open("sample_data/reviews.json") as f:
        records = json.load(f)

    engine = FusionEngine()
    for record in records:
        result = engine.analyze(record)
        print(f"\n=== {result['product']} ===")
        print(f"Text sentiment: {result['text_signal']['sentiment']}")
        print(f"Image issues: {result['image_signal']['detected_issues']}")
        print(f"Call urgency: {result['audio_signal']['urgency_signals']}")
        print(f"Severity score: {result['severity_score']}/3")
        print(f"Business Insight: {result['business_insight']}")
