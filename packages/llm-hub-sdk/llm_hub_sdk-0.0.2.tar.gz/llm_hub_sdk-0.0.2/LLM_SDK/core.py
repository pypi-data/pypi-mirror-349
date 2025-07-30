import requests
import os
import json
import logging
from typing import Dict, List, Any, Optional, Union

from .exceptions import (
    SDKError,
    APIRequestError,
    ConnectionError,
    TimeoutError,
    InvalidResponseError,
)

logger = logging.getLogger(__name__)


# --- Block 1: UnifiedChatClient Class Definition ---
# This class serves as the primary interface for interacting with a backend chat API.
# It handles request formatting, HTTP communication, response parsing, and error handling,
# aiming to provide a simplified and consistent way to use the chat service.
class UnifiedChatClient:

    # --- Block 1.1: Client Initialization (__init__) ---
    # The constructor for the UnifiedChatClient.
    # Responsibilities:
    # 1. Store the base URL for the target API and a default request timeout.
    # 2. Validate that a base URL is provided.
    # 3. Initialize a 'requests.Session' object, which allows for connection pooling,
    #    persistent parameters (like headers), and improved performance for multiple requests.
    # 4. Set default HTTP headers (e.g., Content-Type, Accept) for all requests made by this client instance.
    def __init__(self, base_url: str, timeout: int = 60):
        if not base_url:
            raise ValueError("base_url cannot be empty.")

        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {"Content-Type": "application/json", "Accept": "application/json"}
        )

    # --- Block 1.2: Chat Method ---
    # This is the core method for sending a chat completion request to the API.
    # Responsibilities:
    # 1. Validate essential input parameters (provider, model, messages).
    # 2. Construct the full API endpoint URL using the configured base URL.
    # 3. Assemble the JSON payload with all necessary and optional chat parameters.
    # 4. Log the outgoing request for debugging purposes.
    # 5. Execute the HTTP POST request and handle the response, including:
    #    - Checking for HTTP error statuses.
    #    - Parsing successful JSON responses.
    #    - Handling various types of exceptions (network errors, timeouts, API errors, JSON decoding errors)
    #      and mapping them to standardized SDK exceptions.
    def chat(
        self,
        provider: str,
        model: str,
        messages: List[Dict[str, str]],
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        if not provider or not model or not messages:
            raise ValueError(
                "`provider`, `model`, and `messages` are required arguments."
            )

        endpoint = f"{self.base_url}/v1/chat"

        payload: Dict[str, Any] = {
            "provider": provider,
            "model": model,
            "messages": messages,
            **({"max_tokens": max_tokens} if max_tokens is not None else {}),
            **({"temperature": temperature} if temperature is not None else {}),
            **kwargs,
        }

        logger.debug(
            f"Sending request to {endpoint} with payload: {json.dumps(payload)}"
        )

        # --- Block 1.2.1: HTTP Request Execution and Response Processing ---
        # This 'try' block attempts the actual HTTP POST request.
        # If successful (2xx status), it then tries to parse the JSON body.
        # It includes a nested 'try-except' to specifically handle JSON decoding errors
        # while still being within the context of a non-HTTP-error response.
        try:
            response = self.session.post(endpoint, json=payload, timeout=self.timeout)
            response.raise_for_status()

            try:
                response_data = response.json()
                logger.debug(
                    f"Received successful response (Status {response.status_code}) from {endpoint}"
                )
                return response_data
            except json.JSONDecodeError as e:
                logger.error(
                    f"Failed to decode JSON response from {endpoint} (Status {response.status_code}). Response text: {response.text[:500]}..."
                )
                raise InvalidResponseError(
                    message=f"Invalid JSON response from API at {endpoint}",
                    status_code=response.status_code,
                    response_text=response.text,
                    original_exception=e,
                ) from e

        # --- Block 1.2.2: Handling Specific Network and HTTP Errors ---
        # These 'except' blocks catch various exceptions that can occur during the HTTP request
        # (e.g., network timeouts, connection problems, or HTTP error statuses like 400 or 500).
        # Each is mapped to a more specific custom SDK exception for consistent error handling by the caller.
        except requests.exceptions.Timeout as e:
            logger.warning(
                f"Request to {endpoint} timed out after {self.timeout}s: {e}"
            )
            raise TimeoutError(
                e, configured_timeout_sec=self.timeout, endpoint_url=endpoint
            ) from e
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection error contacting {endpoint}: {e}")
            raise ConnectionError(e) from e
        except requests.exceptions.HTTPError as e:
            logger.warning(
                f"API request to {endpoint} failed with status {e.response.status_code}. Raw error: {e}"
            )
            raise APIRequestError(e) from e

        # --- Block 1.2.3: Handling Generic Request-Related Errors ---
        # This 'except' block acts as a catch-all for any other exceptions originating from
        # the 'requests' library that weren't caught by the more specific handlers above.
        # It ensures that all known request-related problems are wrapped in a generic SDKError.
        except requests.exceptions.RequestException as e:
            logger.error(
                f"An unexpected requests error occurred contacting {endpoint}: {e}"
            )
            raise SDKError(
                f"An unexpected error occurred during the API request to {endpoint}: {e}",
                original_exception=e,
                details=str(e),
            ) from e
