"""
Logging Configuration for IB API Tests

Centralized logging setup for all test files.
"""

import logging
import sys
from pathlib import Path
from datetime import datetime


class TestLoggingConfig:
    """
    Logging configuration for IB API tests.

    Provides consistent logging across all test modules.
    """

    # Log levels
    LOG_LEVEL = logging.INFO
    VERBOSE_LOG_LEVEL = logging.DEBUG

    # Log format
    DEFAULT_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    VERBOSE_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    SIMPLE_FORMAT = '%(levelname)s: %(message)s'

    # Date format
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

    # Log file settings
    ENABLE_FILE_LOGGING = True
    LOG_DIR = Path(__file__).parent.parent / 'results' / 'logs'
    LOG_FILE_PREFIX = 'ib_api_tests'
    LOG_FILE_EXTENSION = '.log'

    # Log to console
    ENABLE_CONSOLE_LOGGING = True

    # Capture warnings
    CAPTURE_WARNINGS = True

    @classmethod
    def setup_logging(cls, verbose: bool = False, log_to_file: bool = True):
        """
        Set up logging for tests.

        Args:
            verbose: Enable verbose (DEBUG) logging
            log_to_file: Enable file logging
        """
        # Determine log level
        log_level = cls.VERBOSE_LOG_LEVEL if verbose else cls.LOG_LEVEL

        # Determine format
        log_format = cls.VERBOSE_FORMAT if verbose else cls.DEFAULT_FORMAT

        # Create formatters
        formatter = logging.Formatter(log_format, datefmt=cls.DATE_FORMAT)

        # Get root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(log_level)

        # Clear existing handlers
        root_logger.handlers.clear()

        # Console handler
        if cls.ENABLE_CONSOLE_LOGGING:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(log_level)
            console_handler.setFormatter(formatter)
            root_logger.addHandler(console_handler)

        # File handler
        if log_to_file and cls.ENABLE_FILE_LOGGING:
            log_file = cls._get_log_file_path()

            # Create log directory if not exists
            log_file.parent.mkdir(parents=True, exist_ok=True)

            file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
            file_handler.setLevel(log_level)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)

        # Capture warnings
        if cls.CAPTURE_WARNINGS:
            logging.captureWarnings(True)

        # Set log level for ib_insync to reduce noise
        logging.getLogger('ib_insync.wrapper').setLevel(logging.WARNING)
        logging.getLogger('ib_insync.client').setLevel(logging.WARNING)

        return root_logger

    @classmethod
    def _get_log_file_path(cls) -> Path:
        """
        Get log file path with timestamp.

        Returns:
            Path to log file
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{cls.LOG_FILE_PREFIX}_{timestamp}{cls.LOG_FILE_EXTENSION}"
        return cls.LOG_DIR / filename

    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """
        Get a logger with the specified name.

        Args:
            name: Logger name (usually __name__)

        Returns:
            Logger instance
        """
        return logging.getLogger(name)

    @classmethod
    def setup_test_logger(cls, test_name: str, verbose: bool = False) -> logging.Logger:
        """
        Set up logger for specific test.

        Args:
            test_name: Name of the test
            verbose: Enable verbose logging

        Returns:
            Logger instance
        """
        cls.setup_logging(verbose=verbose)
        logger = cls.get_logger(test_name)
        logger.info(f"Starting test: {test_name}")
        return logger

    @classmethod
    def log_test_start(cls, logger: logging.Logger, test_name: str):
        """Log test start"""
        logger.info("=" * 80)
        logger.info(f"TEST START: {test_name}")
        logger.info("=" * 80)

    @classmethod
    def log_test_end(cls, logger: logging.Logger, test_name: str, success: bool = True):
        """Log test end"""
        status = "SUCCESS" if success else "FAILED"
        logger.info("=" * 80)
        logger.info(f"TEST END: {test_name} - {status}")
        logger.info("=" * 80)

    @classmethod
    def log_test_section(cls, logger: logging.Logger, section_name: str):
        """Log test section separator"""
        logger.info("-" * 60)
        logger.info(f"Section: {section_name}")
        logger.info("-" * 60)


# Convenience function for quick setup
def setup_logging(verbose: bool = False, log_to_file: bool = True) -> logging.Logger:
    """
    Quick setup for logging in tests.

    Args:
        verbose: Enable verbose (DEBUG) logging
        log_to_file: Enable file logging

    Returns:
        Root logger
    """
    return TestLoggingConfig.setup_logging(verbose=verbose, log_to_file=log_to_file)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger for a specific module.

    Args:
        name: Logger name (usually __name__)

    Returns:
        Logger instance
    """
    return TestLoggingConfig.get_logger(name)
