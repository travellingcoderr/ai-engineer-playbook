import re

# 🛡️ PII Scrubber (Personally Identifiable Information)
class PIIScrubber:
    def __init__(self):
        # Simple patterns for Email and SSN
        self.patterns = {
            "EMAIL": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
            "SSN": r"\d{3}-\d{2}-\d{4}"
        }

    def scrub(self, text):
        print("🔍 [Guardrails] Scrubbing for PII data...")
        scrubbed_text = text
        for label, pattern in self.patterns.items():
            scrubbed_text = re.sub(pattern, f"[REDACTED_{label}]", scrubbed_text)
        return scrubbed_text

# ⚖️ Bias Checker (Fairness & Ethics)
class BiasChecker:
    def __init__(self):
        # Forbidden bias terms (Age, Gender, Race, etc.)
        self.bias_keywords = ["old people", "youngest", "women only", "men only", "disabled"]

    def check(self, advice):
        print("🔍 [Guardrails] Checking for ethical Bias...")
        advice = advice.lower()
        found_biases = [word for word in self.bias_keywords if word in advice]
        
        if found_biases:
            return {
                "safe": False,
                "reason": f"Bias terms found: {found_biases}. Advice must be neutral."
            }
        return {"safe": True, "reason": "No obvious biases detected."}

# 🏭 The Guardrails Controller
class ResponsibleAIGuardrails:
    def __init__(self):
        self.scrubber = PIIScrubber()
        self.bias_checker = BiasChecker()

    def validate_and_scrub(self, input_text):
        clean_text = self.scrubber.scrub(input_text)
        bias_report = self.bias_checker.check(clean_text)
        
        return {
            "scrubbed_text": clean_text,
            "bias_report": bias_report
        }

# 🧪 Demo
if __name__ == "__main__":
    guardrails = ResponsibleAIGuardrails()
    
    # Example input with PII and some bias
    dirty_input = "My email is john.doe@email.com. I want a portfolio for old people only."
    
    result = guardrails.validate_and_scrub(dirty_input)
    
    print("\n--- Guardrails Output ---")
    print(f"Scrubbed Text: {result['scrubbed_text']}")
    print(f"Bias Check: {result['bias_report']}")
    
    print("\n💡 Interview Tip: Mention that 'Responsible AI' is a ")
    print("core Purple requirement. Talk about how you'd use LLMs ")
    print("to perform these checks automatically at scale.")
