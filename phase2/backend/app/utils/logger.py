"""
Logging configuration for the application.
"""
import logging
import sys
import os
from logging.handlers import RotatingFileHandler

# Determine log level from environment
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# Create logs directory if it doesn't exist
LOGS_DIR = "logs"
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)


def setup_logging():
    """
    Configure application logging with console and file handlers.

    Uses structured logging format suitable for production monitoring.
    """
    # Create formatter
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(LOG_LEVEL)
    console_handler.setFormatter(formatter)

    # File handler (rotating)
    file_handler = RotatingFileHandler(
        filename=os.path.join(LOGS_DIR, "app.log"),
        maxBytes=10485760,  # 10MB
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setLevel(LOG_LEVEL)
    file_handler.setFormatter(formatter)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(LOG_LEVEL)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    # Set specific loggers
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

    logging.info(f"Logging configured with level: {LOG_LEVEL}")


# Initialize logging on import
setup_logging()
