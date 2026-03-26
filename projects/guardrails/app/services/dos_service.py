class DoSService:
    def __init__(self, token_limit: int = 1000):
        self.token_limit = token_limit

    def estimate_tokens(self, text: str) -> int:
        # Rough estimate: 4 chars per token
        return len(text) // 4

    def scan(self, text: str) -> bool:
        return self.estimate_tokens(text) > self.token_limit
