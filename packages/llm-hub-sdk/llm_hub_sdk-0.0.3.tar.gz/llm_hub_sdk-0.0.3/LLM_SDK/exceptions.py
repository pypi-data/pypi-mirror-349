import requests
import json
from typing import Optional, Any, TYPE_CHECKING

# This block is for type hinting. If TYPE_CHECKING is True (which it is
# during static type checking by tools like MyPy), then the code inside
# the `if TYPE_CHECKING:` block is processed. Otherwise, at runtime, it's skipped.
# This is often used to avoid circular imports for type hints.
if TYPE_CHECKING:
    pass  # No specific types imported here for now, but it's a placeholder.


class SDKError(Exception):
    """
    Base custom exception for all SDK-specific errors.
    This allows users of the SDK to catch a single exception type
    if they want to handle any error originating from this SDK.
    """

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        details: Any = None,
        original_exception: Optional[Exception] = None,
    ):
        """
        Initializes the base SDKError.

        Args:
            message: The primary error message.
            status_code: Optional HTTP status code associated with the error.
            details: Optional additional details about the error (can be any type, often a string or dict).
            original_exception: Optional original exception that caused this SDKError, for tracing.
        """
        # --- Initialization Flow ---

        # Step 1: Call the parent Exception's __init__
        # This ensures that the basic Exception behavior (like storing the message) is handled.
        super().__init__(message)

        # Step 2: Store additional error-specific information
        # These attributes provide more context about the error.
        self.status_code = status_code
        self.details = details
        self.original_exception = original_exception

    def __str__(self) -> str:
        """
        Provides a human-readable string representation of the error,
        including status code and details if available.
        """
        # --- String Representation Flow ---

        # Step 1: Get the base error message from the parent Exception class.
        base_msg = super().__str__()

        # Step 2: Append status code and details if they exist.
        # This constructs a more informative error message for the user.
        if self.status_code and self.details:
            return f"{base_msg} (Status: {self.status_code}, Details: {self.details})"
        elif self.status_code:
            return f"{base_msg} (Status: {self.status_code})"
        elif self.details:
            return f"{base_msg} (Details: {self.details})"

        # Step 3: If no status code or details, return the base message.
        return base_msg


class APIRequestError(SDKError):
    """
    Represents an error that occurred due to a non-2xx HTTP response from the API.
    This typically wraps a `requests.exceptions.HTTPError`.
    """

    def __init__(self, http_error: requests.exceptions.HTTPError):
        """
        Initializes an APIRequestError from a requests.exceptions.HTTPError.

        Args:
            http_error: The HTTPError instance from the requests library.
        """
        # --- Initialization Flow ---

        # Step 1: Extract information from the HTTPError.
        # Get the status code from the response.
        status_code = http_error.response.status_code
        # Get the request URL if available.
        request_url = http_error.request.url if http_error.request else "Unknown URL"
        details = None  # Initialize details
        # Get a summary of the response body, truncated for brevity.
        response_text_summary = (
            http_error.response.text[:500]
            if http_error.response.text
            else "No response body."
        )

        # Step 2: Attempt to parse more specific error details from the JSON response.
        # Many APIs return error details in a JSON format.
        try:
            error_data = http_error.response.json()
            if isinstance(error_data, dict):
                # Common keys for error messages in JSON responses.
                if "detail" in error_data:
                    details = error_data["detail"]
                elif "error" in error_data:
                    if (
                        isinstance(error_data["error"], dict)
                        and "message" in error_data["error"]
                    ):
                        details = error_data["error"]["message"]
                    elif isinstance(error_data["error"], str):
                        details = error_data["error"]
                elif "message" in error_data:
                    details = error_data["message"]

                # If no specific detail key is found, use the whole JSON object as details.
                if details is None:
                    details = (
                        json.dumps(error_data) if error_data else response_text_summary
                    )
            else:
                # If the JSON is not a dict, convert it to a string.
                details = (
                    str(error_data) if error_data is not None else response_text_summary
                )
        except json.JSONDecodeError:
            # If the response is not valid JSON, use the text summary as details.
            details = response_text_summary

        # Step 3: Construct the primary error message.
        message = f"API request to {request_url} failed with status {status_code}"

        # Step 4: Call the parent SDKError's __init__.
        # Pass the constructed message, extracted status_code, details, and the original HTTPError.
        super().__init__(
            message,
            status_code=status_code,
            details=details,
            original_exception=http_error,
        )

        # Step 5: Store the full response object for potential further inspection.
        self.response = http_error.response


class ConnectionError(SDKError):
    """
    Represents an error that occurred due to a failure to connect to the API endpoint.
    This typically wraps a `requests.exceptions.ConnectionError`.
    """

    def __init__(self, connection_error: requests.exceptions.ConnectionError):
        """
        Initializes a ConnectionError from a requests.exceptions.ConnectionError.

        Args:
            connection_error: The ConnectionError instance from the requests library.
        """
        # --- Initialization Flow ---

        # Step 1: Extract the request URL if available.
        request_url = (
            connection_error.request.url if connection_error.request else "Unknown URL"
        )

        # Step 2: Construct the primary error message.
        message = f"Could not connect to API endpoint: {request_url}"

        # Step 3: Call the parent SDKError's __init__.
        # Pass the message, details (as string representation of the original error),
        # and the original ConnectionError.
        super().__init__(
            message, details=str(connection_error), original_exception=connection_error
        )


class TimeoutError(SDKError):
    """
    Represents an error that occurred because an API request timed out.
    This typically wraps a `requests.exceptions.Timeout`.
    """

    def __init__(
        self,
        timeout_error: requests.exceptions.Timeout,
        configured_timeout_sec: Optional[int] = None,
        endpoint_url: Optional[str] = None,
    ):
        """
        Initializes a TimeoutError from a requests.exceptions.Timeout.

        Args:
            timeout_error: The Timeout instance from the requests library.
            configured_timeout_sec: The configured timeout value in seconds, if known.
            endpoint_url: The URL of the endpoint that timed out, if known (can override what's in timeout_error.request).
        """
        # --- Initialization Flow ---

        # Step 1: Determine the request URL.
        # Prioritize the explicitly passed endpoint_url, then the URL from the request object in timeout_error.
        request_url = endpoint_url or (
            timeout_error.request.url if timeout_error.request else "Unknown URL"
        )

        # Step 2: Create a string part indicating the timeout duration, if provided.
        timeout_info = (
            f" after {configured_timeout_sec}s"
            if configured_timeout_sec is not None
            else ""
        )

        # Step 3: Construct the primary error message.
        message = f"Request to {request_url} timed out{timeout_info}"

        # Step 4: Call the parent SDKError's __init__.
        # Pass the message, details (as string representation of the original error),
        # and the original Timeout error.
        super().__init__(
            message, details=str(timeout_error), original_exception=timeout_error
        )


class InvalidResponseError(SDKError):
    """
    Represents an error when the API response is not in the expected format
    (e.g., failed to decode JSON when JSON was expected).
    This is specifically for issues like `json.JSONDecodeError` after a successful (e.g., 200 OK) HTTP request,
    or when the response content is otherwise malformed.
    """

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_text: Optional[str] = None,
        original_exception: Optional[Exception] = None,
    ):
        """
        Initializes an InvalidResponseError.

        Args:
            message: The primary error message.
            status_code: Optional HTTP status code if the response was received.
            response_text: The raw text of the response that was invalid.
            original_exception: The original exception (e.g., json.JSONDecodeError) that caused this.
        """
        # --- Initialization Flow ---

        # Step 1: Prepare details from the response text.
        # Truncate the response text for brevity in the error details.
        details = response_text[:500] if response_text else "No response content."

        # Step 2: Call the parent SDKError's __init__.
        # Pass the message, status_code (if applicable), details, and the original exception.
        super().__init__(
            message,
            status_code=status_code,
            details=details,
            original_exception=original_exception,
        )
