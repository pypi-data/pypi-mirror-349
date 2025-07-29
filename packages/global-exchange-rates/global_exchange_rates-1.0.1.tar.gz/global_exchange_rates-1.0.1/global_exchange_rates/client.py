from datetime import date, datetime
from typing import Dict, List, Optional, Type, TypeVar, Any, cast, Union, Iterable
import json

import anyio
import httpx
from pydantic import BaseModel

from .exceptions import ApiException
from .models import Currency, ExchangeRateResponse, ConversionResponse, ErrorResponse, Provider

T = TypeVar('T', bound=BaseModel)


class GlobalExchangeRates:
    """
    Client for accessing the Global Exchange Rates API.
    """
    
    # Define base URL as a class constant like in the C# version
    _BASE_URL = "https://api.globalexchangerates.org/v1"

    def __init__(
        self,
        api_key: str,
        client: Optional[httpx.AsyncClient] = None,
    ):
        """
        Initialize a new GlobalExchangeRates instance.

        Args:
            api_key: The API key for authentication with the Global Exchange Rates API.
            client: Optional external httpx.AsyncClient to use. If provided, it won't be closed by this client.
        """
        if not api_key:
            raise ValueError("API key cannot be empty")
            
        self._api_key = api_key
        self._client = client
        self._external_client = client is not None
        self._headers = {"Subscription-Key": api_key, "X-Source": "Python"}

    async def __aenter__(self) -> 'GlobalExchangeRates':
        """
        Enter the async context manager.
        """
        if not self._external_client and self._client is None:
            self._client = httpx.AsyncClient(base_url=self._BASE_URL, headers=self._headers)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Exit the async context manager.
        """
        if not self._external_client and self._client is not None:
            await self._client.aclose()
            self._client = None

    async def _send_request(
        self,
        endpoint_path: str,
        response_model: Type[T],
        params: Optional[Dict[str, str]] = None,
    ) -> T:
        """
        Send a request to the API and parse the response.

        Args:
            endpoint_path: API endpoint path.
            response_model: Pydantic model to parse the response into.
            params: Optional query parameters.

        Returns:
            Parsed response as the specified Pydantic model.

        Raises:
            ApiException: If the API returns an error.
        """
        if self._client is None:
            raise RuntimeError(
                "HTTP client not initialized. Use the client as an async context manager "
                "or provide an external client."
            )

        url = endpoint_path
        if self._external_client and not self._client.base_url:
            url = f"{self._BASE_URL}{endpoint_path}"
            
        response = await self._client.get(url, params=params)

        if not response.is_success:
            try:
                error_data = ErrorResponse.model_validate_json(response.content)
                error_code = error_data.error_code
                api_message = error_data.message
            except Exception:
                error_code = None
                api_message = None

            message = f"API request failed with status code {response.status_code}"
            raise ApiException(
                message=message,
                status_code=response.status_code,
                error_code=error_code,
                api_message=api_message,
            )

        if hasattr(response_model, "__origin__") and response_model.__origin__ is list:
            item_model = response_model.__args__[0]  
            data = json.loads(response.content)
            return [item_model.model_validate(item) for item in data]
        else:
            return response_model.model_validate_json(response.content)

    # Helper method for synchronous operations
    def _run_async(self, coro_func, *args, **kwargs):
        """
        Run an asynchronous function synchronously.
        
        Args:
            coro_func: The asynchronous function to run
            *args: Positional arguments to pass to the function
            **kwargs: Keyword arguments to pass to the function
            
        Returns:
            The result of the asynchronous function
        """
        async def _run_with_client():
            client = httpx.AsyncClient(base_url=self._BASE_URL, headers=self._headers)
            self._client = client
            try:
                return await coro_func(*args, **kwargs)
            finally:
                await client.aclose()
                if not self._external_client:
                    self._client = None
        
        if self._client is not None:
            return anyio.run(coro_func, *args, **kwargs)
        else:
            return anyio.run(_run_with_client)

    # Currencies API
    
    async def _get_currencies_async(
        self, 
        codes: Optional[Iterable[str]] = None
    ) -> List[Currency]:
        """
        Gets a list of supported currencies.

        Args:
            codes: Optional filter to retrieve specific currency codes.

        Returns:
            A list of currency information.
        """
        params = {}
        if codes:
            params["code"] = ",".join(codes)

        return await self._send_request("/currencies", List[Currency], params)

    def get_currencies(
        self, 
        codes: Optional[Iterable[str]] = None
    ) -> List[Currency]:
        """
        Gets a list of supported currencies (synchronous version).

        Args:
            codes: Optional filter to retrieve specific currency codes.

        Returns:
            A list of currency information.
        """
        return self._run_async(self._get_currencies_async, codes)

    # Latest Exchange Rates API

    async def _get_latest_async(
        self,
        provider: Optional[str] = None,
        currencies: Optional[Iterable[str]] = None,
        base_currency: Optional[str] = None
    ) -> ExchangeRateResponse:
        """
        Gets the latest exchange rates.

        Args:
            provider: Optional provider code.
            currencies: Optional list of currencies to include in the response.
            base_currency: Optional base currency for the rates.

        Returns:
            An exchange rate response containing the rates.
        """
        params = {}
        
        if provider:
            params["provider"] = provider
            
        if currencies:
            params["currencies"] = ",".join(currencies)
            
        if base_currency:
            params["base"] = base_currency
            
        return await self._send_request("/latest", ExchangeRateResponse, params)

    def get_latest(
        self,
        provider: Optional[str] = None,
        currencies: Optional[Iterable[str]] = None,
        base_currency: Optional[str] = None
    ) -> ExchangeRateResponse:
        """
        Gets the latest exchange rates (synchronous version).

        Args:
            provider: Optional provider code.
            currencies: Optional list of currencies to include in the response.
            base_currency: Optional base currency for the rates.

        Returns:
            An exchange rate response containing the rates.
        """
        return self._run_async(
            self._get_latest_async,
            provider,
            currencies,
            base_currency
        )

    # Providers API
    
    async def _get_providers_async(
        self,
        codes: Optional[Iterable[str]] = None,
        country_code: Optional[str] = None
    ) -> List[Provider]:
        """
        Gets a list of supported providers.

        Args:
            codes: Optional filter to retrieve specific provider codes.
            country_code: Optional filter to retrieve providers from a specific country.

        Returns:
            A list of provider information.
        """
        params = {}
        
        if codes:
            params["code"] = ",".join(codes)
            
        if country_code:
            params["countryCode"] = country_code
            
        return await self._send_request("/providers", List[Provider], params)

    def get_providers(
        self,
        codes: Optional[Iterable[str]] = None,
        country_code: Optional[str] = None
    ) -> List[Provider]:
        """
        Gets a list of supported providers (synchronous version).

        Args:
            codes: Optional filter to retrieve specific provider codes.
            country_code: Optional filter to retrieve providers from a specific country.

        Returns:
            A list of provider information.
        """
        return self._run_async(
            self._get_providers_async,
            codes,
            country_code
        )

    # Historical Exchange Rates API

    async def _get_historical_async(
        self,
        date_value: Union[date, datetime, str],
        latest: Optional[bool] = None,
        provider: Optional[str] = None,
        currencies: Optional[Iterable[str]] = None,
        base_currency: Optional[str] = None
    ) -> ExchangeRateResponse:
        """
        Gets historical exchange rates for a specific date.

        Args:
            date_value: The date for which to retrieve historical rates.
            latest: Optional flag to get the latest rates for the specified date.
            provider: Optional provider code.
            currencies: Optional list of currencies to include in the response.
            base_currency: Optional base currency for the rates.

        Returns:
            An exchange rate response containing the rates for the specified date.
        """
        params: Dict[str, str] = {}
        
        # Convert date to required string format
        if isinstance(date_value, (date, datetime)):
            params["date"] = date_value.strftime("%Y-%m-%d")
        else:
            params["date"] = str(date_value)
        
        if latest is not None:
            params["latest"] = str(latest).lower()
            
        if provider:
            params["provider"] = provider
            
        if currencies:
            params["currencies"] = ",".join(currencies)
            
        if base_currency:
            params["base"] = base_currency
            
        return await self._send_request("/historical", ExchangeRateResponse, params)

    def get_historical(
        self,
        date_value: Union[date, datetime, str],
        latest: Optional[bool] = None,
        provider: Optional[str] = None,
        currencies: Optional[Iterable[str]] = None,
        base_currency: Optional[str] = None
    ) -> ExchangeRateResponse:
        """
        Gets historical exchange rates for a specific date (synchronous version).

        Args:
            date_value: The date for which to retrieve historical rates.
            latest: Optional flag to get the latest rates for the specified date.
            provider: Optional provider code.
            currencies: Optional list of currencies to include in the response.
            base_currency: Optional base currency for the rates.

        Returns:
            An exchange rate response containing the rates for the specified date.
        """
        return self._run_async(
            self._get_historical_async,
            date_value,
            latest,
            provider,
            currencies,
            base_currency
        )

    # Currency Conversion API

    async def _convert_async(
        self,
        amount: float,
        base_currency: Optional[str] = None,
        to_currencies: Optional[Iterable[str]] = None,
        provider: Optional[str] = None,
        date_value: Optional[Union[date, datetime, str]] = None
    ) -> ConversionResponse:
        """
        Converts an amount from one currency to others.

        Args:
            amount: The amount to convert.
            base_currency: Optional source currency code.
            to_currencies: Optional target currency codes.
            provider: Optional provider code.
            date_value: Optional date for historical conversions.

        Returns:
            A conversion response containing the converted amounts.
        """
        params: Dict[str, str] = {
            "amount": str(amount)
        }
        
        if base_currency:
            params["base"] = base_currency
            
        if to_currencies:
            params["to"] = ",".join(to_currencies)
            
        if provider:
            params["provider"] = provider
            
        if date_value:
            if isinstance(date_value, (date, datetime)):
                params["date"] = date_value.strftime("%Y-%m-%d")
            else:
                params["date"] = str(date_value)
            
        return await self._send_request("/convert", ConversionResponse, params)

    def convert(
        self,
        amount: float,
        base_currency: Optional[str] = None,
        to_currencies: Optional[Iterable[str]] = None,
        provider: Optional[str] = None,
        date_value: Optional[Union[date, datetime, str]] = None
    ) -> ConversionResponse:
        """
        Converts an amount from one currency to others (synchronous version).

        Args:
            amount: The amount to convert.
            base_currency: Optional source currency code.
            to_currencies: Optional target currency codes.
            provider: Optional provider code.
            date_value: Optional date for historical conversions.

        Returns:
            A conversion response containing the converted amounts.
        """
        return self._run_async(
            self._convert_async,
            amount,
            base_currency,
            to_currencies,
            provider,
            date_value
        )
