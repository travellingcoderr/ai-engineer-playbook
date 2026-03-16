import re
from typing import Protocol, List
from ..models.guard_models import GuardResponse

class GuardEngine(Protocol):
    def validate(self, text: str, checks: List[str]) -> GuardResponse:
        ...

class SimpleRegexEngine:
    def validate(self, text: str, checks: List[str]) -> GuardResponse:
        findings = []
        filtered_text = text
        safe = True
        action = "allowed"

        if "pii" in checks:
            # Simple email check
            emails = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', text)
            if emails:
                findings.append(f"PII detected: {len(emails)} email(s)")
                for email in emails:
                    filtered_text = filtered_text.replace(email, "[REDACTED_EMAIL]")
                action = "redacted"

        if "secrets" in checks:
            # Simple API key pattern
            keys = re.findall(r'(sk-[a-zA-Z0-9]{32,})', text)
            if keys:
                findings.append("Secret detected: OpenAI API Key pattern")
                safe = False
                action = "blocked"

        if "injection" in checks:
            patterns = ["ignore previous instructions", "system prompt", "you are now"]
            if any(p in text.lower() for p in patterns):
                findings.append("Potential prompt injection detected")
                safe = False
                action = "blocked"

        return GuardResponse(
            safe=safe,
            action=action,
            filtered_text=filtered_text,
            findings=findings
        )

class GuardrailFactory:
    @staticmethod
    def get_engine(engine_type: str = "simple") -> GuardEngine:
        if engine_type == "simple":
            return SimpleRegexEngine()
        # Placeholder for more complex engines (e.g., using transformers or external APIs)
        raise ValueError(f"Unknown engine type: {engine_type}")
