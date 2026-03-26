import re

class SafetyService:
    def __init__(self):
        self.harmful_patterns = [
            r"how to build a bomb",
            r"steal credit cards",
            r"hack into",
            r"bypass security"
        ]

    def scan(self, text: str) -> bool:
        lowercase_text = text.lower()
        for pattern in self.harmful_patterns:
            if re.search(pattern, lowercase_text):
                return True
        return False
