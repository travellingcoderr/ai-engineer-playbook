from enum import Enum

class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class MetricUnit(str, Enum):
    COUNT = "count"
    SECONDS = "seconds"
    PERCENT = "percent"
    BYTES = "bytes"
