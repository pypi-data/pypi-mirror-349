from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class Currency(BaseModel):
    """
    Represents a currency in the exchange rates system.
    """
    code: str
    name: str
    numeric_code: Optional[str] = Field(None, alias="numericCode")
    obsolete: bool
    
    class Config:
        populate_by_name = True


class Provider(BaseModel):
    """
    Represents a data provider for exchange rates.
    """
    code: str
    description: str
    country: str
    reference_currency: str = Field(alias="referenceCurrency")
    time_series: bool = Field(alias="timeSeries")
    monthly: bool
    country_code: str = Field(alias="countryCode")
    
    class Config:
        populate_by_name = True


class ExchangeRateResponse(BaseModel):
    """
    Represents an exchange rate response from the API.
    """
    provider: str
    date: datetime
    base: str
    exchange_rates: Dict[str, float] = Field(alias="exchangeRates")
    
    class Config:
        populate_by_name = True


class ConversionResponse(BaseModel):
    """
    Represents a currency conversion response from the API.
    """
    provider: str
    date: datetime
    base: str
    amount: float
    conversions: Dict[str, float]
    
    class Config:
        populate_by_name = True


class ErrorResponse(BaseModel):
    """
    Represents an error response from the API.
    """
    message: str
    error_code: int = Field(alias="errorCode")
    
    class Config:
        populate_by_name = True
