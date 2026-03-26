import base64
import re
from .injection_service import InjectionService

class SmugglingService:
    def __init__(self):
        self.injection_service = InjectionService()

    def decode_rot13(self, text: str) -> str:
        def rot13_char(c: str) -> str:
            if 'a' <= c <= 'z':
                return chr((ord(c) - ord('a') + 13) % 26 + ord('a'))
            if 'A' <= c <= 'Z':
                return chr((ord(c) - ord('A') + 13) % 26 + ord('A'))
            return c
        return "".join([rot13_char(c) for c in text])

    def scan(self, text: str) -> bool:
        # 1. Check for Base64-like strings
        b64_pattern = r'(?:[A-Za-z0-9+/]{4}){2,}(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?'
        potential_b64s = re.findall(b64_pattern, text)
        
        for b64_str in potential_b64s:
            try:
                decoded = base64.b64decode(b64_str).decode('utf-8', errors='ignore')
                if len(decoded) > 5 and self.injection_service.scan(decoded):
                    return True
            except:
                continue

        # 2. Check for ROT13
        if self.injection_service.scan(self.decode_rot13(text)):
            return True

        # 3. Check for suspicious whitespace manipulation (e.g. "i g n o r e")
        # Remove all whitespace and re-scan
        no_whitespace = "".join(text.split())
        if self.injection_service.scan(no_whitespace):
            return True

        # 4. Check for Unicode Homoglyphs (very basic version)
        # Replacing common cyrillic homoglyphs with latin equivalents
        homoglyphs = str.maketrans("аеорсух", "aeopcux")
        normalized = text.translate(homoglyphs)
        if normalized != text and self.injection_service.scan(normalized):
            return True
            
        return False
