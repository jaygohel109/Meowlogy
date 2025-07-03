"""
Custom exceptions for the Cat Facts API.
"""


class CatFactsException(Exception):
    """Base exception for Cat Facts API."""
    pass


class DatabaseException(CatFactsException):
    """Exception raised for database-related errors."""
    pass


class ValidationException(CatFactsException):
    """Exception raised for validation errors."""
    pass


class AIServiceException(CatFactsException):
    """Exception raised for AI service errors."""
    pass


class ConfigurationException(CatFactsException):
    """Exception raised for configuration errors."""
    pass


class ExternalAPIException(CatFactsException):
    """Exception raised for external API errors."""
    pass


class FactNotFoundException(CatFactsException):
    """Exception raised when a fact is not found."""
    pass


class DuplicateFactException(CatFactsException):
    """Exception raised when trying to add a duplicate fact."""
    pass 