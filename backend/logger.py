"""
Structured Logging Configuration

Provides centralized, structured logging for the application.
Supports both development and production environments.
"""

import json
import logging
import os
import sys
from datetime import datetime
from typing import Any, Dict


class StructuredFormatter(logging.Formatter):
    """
    JSON formatter for structured logging.
    Outputs logs in JSON format for easy parsing and analysis.
    """

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON"""
        log_data: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        # Add extra fields from record
        if hasattr(record, "extra_fields"):
            log_data.update(record.extra_fields)

        # Add request context if available
        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id
        if hasattr(record, "user_id"):
            log_data["user_id"] = record.user_id
        if hasattr(record, "endpoint"):
            log_data["endpoint"] = record.endpoint

        return json.dumps(log_data)


class DevelopmentFormatter(logging.Formatter):
    """
    Human-readable formatter for development.
    Color-coded and easy to read during local development.
    """

    # ANSI color codes
    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[35m",  # Magenta
        "RESET": "\033[0m",
    }

    def format(self, record: logging.LogRecord) -> str:
        """Format log record with colors"""
        color = self.COLORS.get(record.levelname, self.COLORS["RESET"])
        reset = self.COLORS["RESET"]

        # Format timestamp
        timestamp = datetime.fromtimestamp(record.created).strftime("%H:%M:%S")

        # Format message
        message = (
            f"{color}[{timestamp}] {record.levelname:8s}{reset} "
            f"{record.name} - {record.getMessage()}"
        )

        # Add exception if present
        if record.exc_info:
            message += f"\n{self.formatException(record.exc_info)}"

        return message


def setup_logging(level: str = None, use_json: bool = None) -> logging.Logger:
    """
    Configure application logging.

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        use_json: Use JSON formatting (for production)

    Returns:
        Configured logger instance
    """
    # Determine settings from environment
    if level is None:
        level = os.getenv("LOG_LEVEL", "INFO")
    if use_json is None:
        use_json = os.getenv("LOG_FORMAT", "human") == "json"

    # Get root logger
    logger = logging.getLogger("testbook")
    logger.setLevel(level.upper())

    # Remove existing handlers
    logger.handlers.clear()

    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level.upper())

    # Set formatter based on environment
    if use_json:
        formatter = StructuredFormatter()
    else:
        formatter = DevelopmentFormatter()

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Don't propagate to root logger
    logger.propagate = False

    return logger


def get_logger(name: str = None) -> logging.Logger:
    """
    Get a logger instance.

    Args:
        name: Logger name (usually __name__)

    Returns:
        Logger instance
    """
    if name:
        return logging.getLogger(f"testbook.{name}")
    return logging.getLogger("testbook")


# Example usage in endpoints:
#
# from logger import get_logger
#
# logger = get_logger(__name__)
#
# @router.get("/users/{user_id}")
# async def get_user(user_id: int):
#     logger.info("Fetching user", extra={"extra_fields": {"user_id": user_id}})
#     try:
#         user = fetch_user(user_id)
#         logger.debug("User fetched successfully", extra={"extra_fields": {"username": user.username}})
#         return user
#     except Exception as e:
#         logger.error("Failed to fetch user", exc_info=True, extra={"extra_fields": {"user_id": user_id}})
#         raise
