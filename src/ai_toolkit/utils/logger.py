"""
Logging utilities for AI Character Toolkit.
"""

import logging
import logging.handlers
import os
from pathlib import Path
from typing import Optional

from .config import config


class Logger:
    """Logger wrapper for consistent logging across the toolkit."""

    _loggers = {}

    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """
        Get or create a logger instance.

        Args:
            name: Logger name (usually __name__)

        Returns:
            Logger instance
        """
        if name not in cls._loggers:
            cls._loggers[name] = cls._create_logger(name)
        return cls._loggers[name]

    @classmethod
    def _create_logger(cls, name: str) -> logging.Logger:
        """Create a new logger instance."""
        logger = logging.getLogger(name)

        # Avoid duplicate handlers
        if logger.handlers:
            return logger

        logger.setLevel(getattr(logging, config.get('logging.level', 'INFO')))

        # Create formatter
        formatter = logging.Formatter(
            config.get('logging.format',
                      '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File handler (if configured)
        log_file = config.get('logging.file')
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)

            # Rotating file handler
            max_size = cls._parse_size(config.get('logging.max_size', '10MB'))
            backup_count = config.get('logging.backup_count', 5)

            file_handler = logging.handlers.RotatingFileHandler(
                log_path,
                maxBytes=max_size,
                backupCount=backup_count,
                encoding='utf-8'
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        return logger

    @classmethod
    def _parse_size(cls, size_str: str) -> int:
        """Parse size string (e.g., '10MB') to bytes."""
        size_str = size_str.upper()
        if size_str.endswith('KB'):
            return int(size_str[:-2]) * 1024
        elif size_str.endswith('MB'):
            return int(size_str[:-2]) * 1024 * 1024
        elif size_str.endswith('GB'):
            return int(size_str[:-2]) * 1024 * 1024 * 1024
        else:
            return int(size_str)


# Module-level convenience function
def get_logger(name: str) -> logging.Logger:
    """Get logger instance."""
    return Logger.get_logger(name)


# Context manager for logging performance
class LogTimer:
    """Context manager for timing operations and logging duration."""

    def __init__(self, logger: logging.Logger, operation: str, level: int = logging.DEBUG):
        """
        Initialize timer context manager.

        Args:
            logger: Logger instance
            operation: Description of operation being timed
            level: Logging level for the duration message
        """
        self.logger = logger
        self.operation = operation
        self.level = level

    def __enter__(self):
        """Start timer."""
        import time
        self.start_time = time.time()
        self.logger.log(self.level, f"Starting: {self.operation}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """End timer and log duration."""
        import time
        duration = time.time() - self.start_time
        self.logger.log(self.level, f"Completed: {self.operation} ({duration:.2f}s)")


# Function decorator for logging function calls
def log_calls(logger: Optional[logging.Logger] = None, level: int = logging.DEBUG):
    """
    Decorator to log function calls.

    Args:
        logger: Logger instance (creates new one if not provided)
        level: Logging level for messages
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            import time
            start_time = time.time()

            # Get or create logger
            func_logger = logger or get_logger(func.__module__)

            # Log function call
            func_name = f"{func.__module__}.{func.__name__}"
            func_logger.log(level, f"Calling {func_name} with args={args}, kwargs={kwargs}")

            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                func_logger.log(level, f"Completed {func_name} in {duration:.2f}s")
                return result
            except Exception as e:
                duration = time.time() - start_time
                func_logger.error(f"Failed {func_name} after {duration:.2f}s: {e}")
                raise

        return wrapper
    return decorator