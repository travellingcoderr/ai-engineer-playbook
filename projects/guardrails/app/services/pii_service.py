import re

class PIIService:
    def __init__(self):
        self.patterns = {
            "email": r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',
            "ssn": r'\b\d{3}-\d{2}-\d{4}\b',
            "phone": r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b',
            "credit_card": r'\b(?:\d[ -]*?){13,16}\b'
        }

    def scan(self, text: str):
        findings = []
        redacted_text = text
        for p_name, pattern in self.patterns.items():
            matches = re.findall(pattern, text)
            if matches:
                findings.append(f"PII detected: {len(matches)} {p_name}(s)")
                for match in matches:
                    redacted_text = redacted_text.replace(match, f"[REDACTED_{p_name.upper()}]")
        return redacted_text, findings
