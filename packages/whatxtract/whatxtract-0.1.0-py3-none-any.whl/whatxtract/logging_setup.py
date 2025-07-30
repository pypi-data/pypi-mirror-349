"""Logging setup for the whatxtract package."""

import sys
import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler

try:
    from colorlog import ColoredFormatter
except ImportError:
    import sys
    import subprocess

    print('[*] Installing colorlog...')
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'colorlog'])
    from colorlog import ColoredFormatter


# fmt: off
LOG_LEVEL           = logging.INFO
LOG_DIR             = Path.cwd() / 'logs'
LOG_FILE            = LOG_DIR / f'/{__package__}.log'
LOG_FORMAT          = '[%(asctime)s] %(levelname)s - %(message)s'
LOG_DIR.mkdir(exist_ok=True, parents=True)
# fmt: on


class PrefixedFormatter(logging.Formatter):
    """Adds a prefix to log messages."""

    def format(self, record):
        """Format the log message with a prefix."""
        if record.levelno == logging.INFO:
            record.msg = f'   {record.msg}' if record.msg.startswith('[') else f'   [ ! ] {record.msg}'
        elif record.levelno == logging.DEBUG:
            record.msg = f'  {record.msg}' if record.msg.startswith('[') else f'  [ ~ ] {record.msg}'
        elif record.levelno == logging.ERROR:
            record.msg = f'  {record.msg}' if record.msg.startswith('[') else f'  [ x ] {record.msg}'
        return super().format(record)


class PrefixedColorFormatter(ColoredFormatter):
    """Adds a prefix to log messages and uses colored output."""

    def format(self, record):
        """Format the log message with a prefix and colored output."""
        if record.levelno == logging.INFO:
            record.msg = f'   {record.msg}' if record.msg.startswith('[') else f'   [ ! ] {record.msg}'
        elif record.levelno == logging.DEBUG:
            record.msg = f'  {record.msg}' if record.msg.startswith('[') else f'  [ ~ ] {record.msg}'
        elif record.levelno == logging.ERROR:
            record.msg = f'  {record.msg}' if record.msg.startswith('[') else f'  [ x ] {record.msg}'
        return super().format(record)


class StreamToLogger:
    """Redirects print() calls to a logger as INFO while preserving console output."""

    def __init__(self, _logger: logging.Logger):
        """Initialize a new logger instance."""
        self.logger = _logger

    def write(self, message):
        """Write a message to the logger."""
        message = message.strip()
        if message:
            self.logger.info(message)

    def flush(self):
        """Flush the stream, if applicable, otherwise do nothing."""
        pass


def setup_logger(name: str = __package__) -> logging.Logger:
    """Sets up and returns a logger instance with console and rotating file handlers."""
    _logger = logging.getLogger(name)
    _logger.setLevel(LOG_LEVEL)

    if not _logger.handlers:
        # Formatter for files
        file_formatter = PrefixedFormatter(LOG_FORMAT)

        # Colored formatter for console
        if ColoredFormatter:
            color_formatter = PrefixedColorFormatter(
                '%(log_color)s%(asctime)s [%(levelname)s] %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                log_colors={
                    'DEBUG': 'cyan',
                    'INFO': 'green',
                    'WARNING': 'yellow',
                    'ERROR': 'red',
                    'CRITICAL': 'bold_red',
                },
            )
        else:
            color_formatter = file_formatter  # fallback

        # Console handler with colors
        stream_handler = logging.StreamHandler(sys.__stdout__)
        stream_handler.setFormatter(color_formatter)
        _logger.addHandler(stream_handler)

        # Rotating file handler (5MB, 3 backups)
        rotating_handler = RotatingFileHandler(LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3)
        rotating_handler.setFormatter(file_formatter)
        _logger.addHandler(rotating_handler)

    # Redirect print() output
    sys.stdout = StreamToLogger(_logger)

    return _logger


# Create a logger instance for the package and redirect print() output to it.
# This can be imported by other modules to use the logger.
logger = setup_logger(__package__)
