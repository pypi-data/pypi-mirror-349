"""
Exception classes for Nekuda SDK
"""


class NekudaError(Exception):
    """Base exception for all Nekuda SDK errors"""

    pass


class NekudaApiError(NekudaError):
    """Exception raised for API errors"""

    def __init__(self, message: str, code: str, status_code: int):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(f"[{code}] {message} (Status: {status_code})")


class NekudaConnectionError(NekudaError):
    """Exception raised for connection errors"""

    pass


class NekudaValidationError(NekudaError):
    """Exception raised for validation errors"""

    pass


# ----------------------------------------------------------------------
# Granular exception hierarchy (mirrors Stripe-like ergonomics) ---------
# ----------------------------------------------------------------------


class AuthenticationError(NekudaApiError):
    """401 – API key missing or invalid."""


class InvalidRequestError(NekudaApiError):
    """400/404 – Invalid parameters or resource not found."""


class RateLimitError(NekudaApiError):
    """429 – Too many requests."""


class ServerError(NekudaApiError):
    """5xx – Internal error on Nekuda side."""
