import json
import re

class OutputService:
    def __init__(self):
        self.harmful_output_patterns = [
            r"<script.*?>",
            r"javascript:",
            r"onerror=",
            r"onload=",
            r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
        ]

    def validate_structure(self, text: str, expected_format: str = "json") -> bool:
        if expected_format == "json":
            try:
                json.loads(text)
                return True
            except json.JSONDecodeError:
                return False
        return True

    def scan_content(self, text: str) -> bool:
        lowercase_text = text.lower()
        for pattern in self.harmful_output_patterns:
            if re.search(pattern, lowercase_text):
                return True
        return False
