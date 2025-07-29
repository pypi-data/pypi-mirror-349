from typing import Optional


class ApiException(Exception):
    """
    Exception thrown when an API request fails.
    """
    
    def __init__(
        self, 
        message: str,
        status_code: int, 
        error_code: Optional[int] = None, 
        api_message: Optional[str] = None,
        inner_exception: Optional[Exception] = None
    ):
        """
        Initialize a new instance of the ApiException class.
        
        Args:
            message: The exception message.
            status_code: The HTTP status code.
            error_code: The API error code, if available.
            api_message: The API error message, if available.
            inner_exception: The inner exception, if available.
        """
        self.status_code = status_code
        self.error_code = error_code
        self.api_message = api_message
        
        if inner_exception:
            super().__init__(message, inner_exception)
        else:
            super().__init__(message)
    
    def __str__(self) -> str:
        """
        String representation of the exception.
        """
        message_parts = [super().__str__()]
        
        if hasattr(self, "status_code"):
            message_parts.append(f"Status Code: {self.status_code}")
        
        if hasattr(self, "error_code") and self.error_code is not None:
            message_parts.append(f"Error Code: {self.error_code}")
        
        if hasattr(self, "api_message") and self.api_message is not None:
            message_parts.append(f"API Message: {self.api_message}")
        
        return ", ".join(message_parts)
