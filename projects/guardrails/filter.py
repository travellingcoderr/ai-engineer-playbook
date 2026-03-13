
def detect_prompt_injection(text):
    patterns = ["ignore previous instructions","reveal system prompt"]
    return any(p in text.lower() for p in patterns)
