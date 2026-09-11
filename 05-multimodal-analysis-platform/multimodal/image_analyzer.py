"""Image modality.
For this starter version, we accept a text `image_note` (e.g. from a
vision model or human tag) describing the photo, and flag quality issues.
Swap `analyze_note()` for a real vision-model call (e.g. Claude vision
input) when you have actual image files.
"""

ISSUE_KEYWORDS = {"scuff", "scratch", "crack", "damage", "broken", "dent", "dirty"}


class ImageAnalyzer:
    def analyze_note(self, image_note: str) -> dict:
        note_lower = image_note.lower()
        issues = [kw for kw in ISSUE_KEYWORDS if kw in note_lower]
        return {
            "has_quality_issue": len(issues) > 0,
            "detected_issues": issues,
            "raw_note": image_note,
        }

    # Placeholder for a real implementation using Claude's vision input:
    # def analyze_image_file(self, image_path: str) -> dict:
    #     ...send base64 image to Claude with a vision-capable model...
