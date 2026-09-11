"""Audio modality.
Accepts an already-transcribed call transcript (string) and analyzes it.
For real audio files, plug in `openai-whisper` (or any ASR) to produce
the transcript first, then feed it into `analyze_transcript()`.
"""
from .text_analyzer import TextAnalyzer

URGENCY_KEYWORDS = {"replacement", "refund", "cancel", "broken", "stopped", "urgent"}


class AudioAnalyzer:
    def __init__(self):
        self.text_analyzer = TextAnalyzer()

    def analyze_transcript(self, transcript: str) -> dict:
        sentiment_result = self.text_analyzer.analyze(transcript)
        transcript_lower = transcript.lower()
        urgency_hits = [kw for kw in URGENCY_KEYWORDS if kw in transcript_lower]
        return {
            **sentiment_result,
            "is_urgent": len(urgency_hits) > 0,
            "urgency_signals": urgency_hits,
            "transcript": transcript,
        }

    # Placeholder for real ASR:
    # def transcribe(self, audio_path: str) -> str:
    #     import whisper
    #     model = whisper.load_model("base")
    #     return model.transcribe(audio_path)["text"]
