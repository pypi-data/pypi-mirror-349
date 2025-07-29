"""
Custom exceptions for the MyCANoe library
"""

class MyCANoeException(Exception):
    """Base exception for MyCANoe library"""
    pass

class ConnectionError(MyCANoeException):
    """Raised when connection to CANoe fails"""
    pass

class ConfigurationError(MyCANoeException):
    """Raised when there's an issue with CANoe configuration"""
    pass

class MeasurementError(MyCANoeException):
    """Raised when there's an issue with CANoe measurement"""
    pass

class SignalError(MyCANoeException):
    """Raised when there's an issue with CANoe signals"""
    pass