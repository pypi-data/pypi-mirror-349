import re
from smartapi.config import LogLevel
import logging


def _setup_logging(self, log_level: LogLevel) -> None:
    """Configure structured logging for the client."""
    if not self.logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            fmt='%(asctime)s %(name)s %(levelname)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(log_level.value)


def normalize_method_name(name: str) -> str:
    # Convert to lowercase
    name = name.lower()
    # Replace spaces with underscores
    name = name.replace(' ', '_')
    # Remove special characters except underscores
    name = re.sub(r'[^\w_]', '', name)
    return name
