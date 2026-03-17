from .base import IngestionStrategy
from .console_strategy import ConsoleIngestionStrategy
from .file_strategy import FileIngestionStrategy

class ObservabilityFactory:
    @staticmethod
    def get_strategy(strategy_type: str = "console") -> IngestionStrategy:
        if strategy_type == "console":
            return ConsoleIngestionStrategy()
        elif strategy_type == "file":
            return FileIngestionStrategy()
        raise ValueError(f"Unknown strategy type: {strategy_type}")
