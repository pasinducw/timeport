"""Logging configuration for the time tracker application."""

import os
import logging
from logging.handlers import RotatingFileHandler
from typing import Optional

def setup_logging(app_name: str = 'timetracker', log_level: Optional[str] = None) -> None:
    """Configure application logging.
    
    Args:
        app_name: Name of the application for the log file.
        log_level: Optional logging level (DEBUG, INFO, etc). Defaults to INFO.
    """
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Set default log level
    level = getattr(logging, log_level.upper()) if log_level else logging.INFO

    # Create formatters and handlers
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(levelname)s - %(message)s'
    )

    # File handler
    file_handler = RotatingFileHandler(
        f'logs/{app_name}.log',
        maxBytes=1024 * 1024,  # 1MB
        backupCount=10
    )
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(level)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(level)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    # Create app logger
    logger = logging.getLogger(app_name)
    logger.info(f"Logging configured with level: {logging.getLevelName(level)}")
