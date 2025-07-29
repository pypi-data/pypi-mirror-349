"""This module provides a singleton class for logging debug messages."""

import sys
from enum import Enum, auto


class LogLevel(Enum):
    """
    Enum for log levels.

    This enum defines different levels of logging severity.
    """

    INFO = auto()
    DEBUG = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()
    UPDATED = auto()


class DebugPipeline:
    """
    Singleton class for the debug pipeline.

    This class is responsible for logging messages to the console
    or a log file.
    """

    _instance = None  # Singleton instance

    def __new__(cls, verbose: bool) -> "DebugPipeline":
        """
        Create a new instance of the DebugPipeline if it doesn't exist.

        :param verbose: Enable verbose mode (prints to stdout).
        """
        if cls._instance is None:
            cls._instance = super(DebugPipeline, cls).__new__(cls)
            cls._instance._initialize(verbose)
        return cls._instance

    def _initialize(self, verbose: bool) -> None:
        """
        Initialize the debug pipeline.

        :param verbose: Enable verbose mode (prints to stdout).
        :param log_file: Optional log file path.
        """
        self.verbose = verbose

    def log(self, message: str, level: LogLevel) -> None:
        """
        Log a message to the pipeline.

        :param message: The debug message.
        :param level: The severity level ('INFO', 'DEBUG', 'ERROR', etc.).
        """
        levelName = f"[{level.name}]"
        formatted_message = f"{levelName:<10} {message}\n"

        # Print to console
        if self.verbose and (level == LogLevel.DEBUG):
            sys.stdout.write(formatted_message)
        if level == LogLevel.INFO:
            sys.stdout.write(formatted_message)
        if level == LogLevel.UPDATED:
            print(f"\r{"[" + LogLevel.INFO.name + "]":<10} {message}", end="")
        if level == LogLevel.WARNING:
            sys.stderr.write(formatted_message)

    def get_debug_pipeline() -> "DebugPipeline":  # type: ignore
        """Retrieve the shared debug pipeline instance."""
        if DebugPipeline._instance is None:
            return DebugPipeline(True)
        return DebugPipeline._instance
