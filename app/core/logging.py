import logging
import sys

from app.core.config import get_settings


class SensitiveDataFilter(logging.Filter):
    """Filter that masks passwords or key if they accidentally appear in log messages."""

    SENSISTIVE_KEY = ("password", "token", "secret", "api_key", "authorization")

    def filter(self, record: logging.LogRecord) -> bool:
        message = record.getMessage()
        # any sensitive keyword is detected in log text, mask it

        for key in self.SENSISTIVE_KEY:
            if key in message.lower():
                record.msg = (
                    f"[REDACTED - SENSITIVE DATA DETECTED IN LOG] (module: {record.module})"
                )
                record.args = ()  # Prevent re-formatting
                break
        return True


def setup_logging() -> None:
    """Configure application-wide structured logging format and log levels."""
    settings = get_settings()

    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    # Standard structured format

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console Handler directed to stdout
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    console_handler.addFilter(SensitiveDataFilter())

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Remove existing handlers to avoid duplicate log entries (common in reload mode)
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    root_logger.addHandler(console_handler)

    # Quiet down overly verbose third-party libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Return a logger instance with the given name."""
    return logging.getLogger(name)
