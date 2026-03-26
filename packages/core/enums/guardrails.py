from enum import Enum

class GuardAction(str, Enum):
    ALLOWED = "allowed"
    REDACTED = "redacted"
    BLOCKED = "blocked"

class GuardCheckType(str, Enum):
    PII = "pii"
    INJECTION = "injection"
    SECRETS = "secrets"
    TOXICITY = "toxicity"
    SMUGGLING = "smuggling"
    DOS = "dos"
    HARMFUL_CONTENT = "harmful_content"
    MALFORMED_OUTPUT = "malformed_output"
