"""
Utility functions for the MyCANoe library
"""

import os
import time
import logging
from typing import Callable, Any

def setup_logger(name: str, level=logging.INFO) -> logging.Logger:
    """Set up a logger with the given name and level
    
    Args:
        name: Logger name
        level: Logging level
        
    Returns:
        Configured logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Create console handler if no handlers exist
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setLevel(level)
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        
        # Add handler to logger
        logger.addHandler(handler)
    
    return logger

def wait_until(condition: Callable[[], bool], timeout: float = 5.0, interval: float = 0.1) -> bool:
    """Wait until a condition is true or timeout
    
    Args:
        condition: Function that returns True when condition is met
        timeout: Maximum time to wait in seconds
        interval: Time between checks in seconds
        
    Returns:
        True if condition was met, False if timeout
    """
    start_time = time.time()
    while not condition():
        if time.time() - start_time > timeout:
            return False
        time.sleep(interval)
    return True

def validate_file_path(file_path: str, extension: str = None) -> bool:
    """Validate that a file path exists and has the correct extension
    
    Args:
        file_path: Path to validate
        extension: Optional file extension to check (e.g., '.cfg')
        
    Returns:
        True if file exists and has correct extension
    """
    if not os.path.isfile(file_path):
        return False
    
    if extension and not file_path.lower().endswith(extension.lower()):
        return False
    
    return True

def wait(seconds: float) -> None:
    """Wait for the specified number of seconds
    
    Args:
        seconds: Number of seconds to wait
    """
    time.sleep(seconds)

