import re
from typing import Protocol, List
from packages.core.models.guardrails import GuardResponse
from packages.core.enums import GuardAction, GuardCheckType

class GuardEngine(Protocol):
    def validate(self, text: str, checks: List[GuardCheckType]) -> GuardResponse:
        ...

class SimpleRegexEngine:
    def validate(self, text: str, checks: List[GuardCheckType]) -> GuardResponse:
        findings = []
        filtered_text = text
        safe = True
        action = GuardAction.ALLOWED

        if GuardCheckType.PII in checks:
            # Simple email check
            emails = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', text)
            if emails:
                findings.append(f"PII detected: {len(emails)} email(s)")
                for email in emails:
                    filtered_text = filtered_text.replace(email, "[REDACTED_EMAIL]")
                action = GuardAction.REDACTED

        if GuardCheckType.SECRETS in checks:
            # Simple API key pattern
            keys = re.findall(r'(sk-[a-zA-Z0-9]{32,})', text)
            if keys:
                findings.append("Secret detected: OpenAI API Key pattern")
                safe = False
                action = GuardAction.BLOCKED

        if GuardCheckType.INJECTION in checks:
            patterns = ["ignore previous instructions", "system prompt", "you are now"]
            if any(p in text.lower() for p in patterns):
                findings.append("Potential prompt injection detected")
                safe = False
                action = GuardAction.BLOCKED

        return GuardResponse(
            safe=safe,
            action=action,
            filtered_text=filtered_text,
            findings=findings
        )

from .injection_service import InjectionService
from .smuggling_service import SmugglingService
from .pii_service import PIIService
from .dos_service import DoSService
from .safety_service import SafetyService
from .output_service import OutputService

class AdvancedGuardEngine:
    def __init__(self):
        self.injection_service = InjectionService()
        self.smuggling_service = SmugglingService()
        self.pii_service = PIIService()
        self.dos_service = DoSService()
        self.safety_service = SafetyService()
        self.output_service = OutputService()

    def validate(self, text: str, checks: List[GuardCheckType]) -> GuardResponse:
        findings = []
        filtered_text = text
        safe = True
        action = GuardAction.ALLOWED

        if GuardCheckType.DOS in checks:
            if self.dos_service.scan(text):
                findings.append("DoS protection: Input exceeds token limit")
                safe = False
                action = GuardAction.BLOCKED

        if GuardCheckType.SMUGGLING in checks:
            if self.smuggling_service.scan(text):
                findings.append("Token smuggling detected (encoded payload)")
                safe = False
                action = GuardAction.BLOCKED

        if GuardCheckType.INJECTION in checks:
            if self.injection_service.scan(text):
                findings.append("Potential prompt injection detected")
                safe = False
                action = GuardAction.BLOCKED

        if GuardCheckType.HARMFUL_CONTENT in checks:
            # Scan both input and output (assuming text could be either or both)
            if self.safety_service.scan(text) or self.output_service.scan_content(text):
                findings.append("Harmful content detected (Safety/Output block)")
                safe = False
                action = GuardAction.BLOCKED

        if GuardCheckType.MALFORMED_OUTPUT in checks:
            if not self.output_service.validate_structure(text, expected_format="json"):
                findings.append("Structural failure: Invalid JSON output detected")
                safe = False
                action = GuardAction.BLOCKED

        if GuardCheckType.PII in checks:
            filtered_text, pii_findings = self.pii_service.scan(filtered_text)
            if pii_findings:
                findings.extend(pii_findings)
                if action == GuardAction.ALLOWED:
                    action = GuardAction.REDACTED

        return GuardResponse(
            safe=safe,
            action=action,
            filtered_text=filtered_text,
            findings=findings
        )

class GuardrailFactory:
    @staticmethod
    def get_engine(engine_type: str = "advanced") -> GuardEngine:
        if engine_type == "simple":
            return SimpleRegexEngine()
        if engine_type == "advanced":
            return AdvancedGuardEngine()
        raise ValueError(f"Unknown engine type: {engine_type}")
