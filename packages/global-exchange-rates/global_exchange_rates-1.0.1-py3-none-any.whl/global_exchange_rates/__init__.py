"""
Global Exchange Rates API client for Python.
"""

from .client import GlobalExchangeRates
from .exceptions import ApiException
from .models import (
    Currency,
    Provider,
    ExchangeRateResponse,
    ConversionResponse,
    ErrorResponse,
)

__version__ = "1.0.0"

__all__ = [
    "GlobalExchangeRates",
    "ApiException",
    "Currency",
    "Provider",
    "ExchangeRateResponse",
    "ConversionResponse",
    "ErrorResponse",
]
