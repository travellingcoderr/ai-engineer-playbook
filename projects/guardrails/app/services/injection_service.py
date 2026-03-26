import re

class InjectionService:
    def __init__(self):
        self.patterns = [
            r"ignore.*previous.*instruction",
            r"reveal.*system.*prompt",
            r"you.*are.*now",
            r"forget.*everything",
            r"start.*acting.*as",
            r"bypass.*security",
            r"show.*me.*the.*prompt",
            r"what.*is.*your.*system.*message",
            r"system.*instruction",
            r"assistant.*is.*now.*restricted",
            r"unrestricted",
            r"jailbreak"
        ]

    def scan(self, text: str) -> bool:
        lowercase_text = text.lower()
        for pattern in self.patterns:
            if re.search(pattern, lowercase_text):
                return True
        return False
