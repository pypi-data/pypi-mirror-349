from typing import Dict, List, Any, Optional
from .core import UnifiedChatClient
from .exceptions import SDKError, APIRequestError, ConnectionError, TimeoutError


class GeminiClient:
    """Client specifically for interacting with Google Gemini models."""

    # This class variable defines the provider identifier used when
    # communicating with the UnifiedChatClient. It tells the unified
    # service to route requests to its Google Gemini integration.
    _PROVIDER_NAME = "google"

    def __init__(self, base_url: str, model: str, timeout: int = 60):
        """
        Initializes the Gemini client for a specific model.

        Args:
            base_url: Base URL of the unified FastAPI service.
            model: The specific Gemini model name this client instance will use.
            timeout: Request timeout in seconds.
        """
        # --- Initialization Flow ---

        # Step 1: Instantiate the Unified Client
        # A UnifiedChatClient instance is created. This unified client is responsible
        # for the actual HTTP communication with the backend FastAPI service.
        # It's configured with the base_url of that service and a request timeout.
        self._unified_client = UnifiedChatClient(base_url, timeout)

        # Step 2: Validate the Model Name
        # It's crucial that a Gemini model (e.g., "gemini-pro")
        # is specified for this client instance. If no model name is provided,
        # it raises a ValueError because the client wouldn't know which Gemini
        # model to target.
        if not model:
            raise ValueError("A model name must be provided for GeminiClient.")

        # Step 3: Store the Model Name
        # The provided model name is stored as an instance attribute. This means
        # this specific GeminiClient instance will always use this model
        # for its chat operations.
        self.model = model

    def chat(
        self,
        messages: List[Dict[str, str]],
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Sends a chat request using the pre-configured Gemini model.

        Args:
            messages: The list of message dictionaries.
            max_tokens: Optional maximum tokens for the response.
            temperature: Optional sampling temperature.
            **kwargs: Additional parameters for the API call.
                      Unlike the AnthropicClient, this implementation directly passes
                      all **kwargs. Care should be taken by the caller not to override
                      'provider', 'model', or 'messages' if the UnifiedChatClient
                      doesn't explicitly prevent it. (Though standard practice would be
                      for UnifiedChatClient to prioritize its explicit parameters).

        Returns:
            The API response dictionary.
        """
        # --- Chat Request Flow ---

        # Step 1: Delegate to the Unified Client's Chat Method
        # The actual API call is made by invoking the `chat` method of the
        # `self._unified_client` instance. This unified client handles the
        # communication with the backend FastAPI service.
        return self._unified_client.chat(
            # Step 1a: Specify the Provider
            # The `provider` argument is set to `self._PROVIDER_NAME` (which is "google").
            # This tells the unified FastAPI service to route this request to its
            # Google Gemini backend integration.
            provider=self._PROVIDER_NAME,
            # Step 1b: Specify the Model
            # The `model` argument is set to `self.model` (the model name stored
            # during initialization, e.g., "gemini-pro"). This tells the
            # unified service (and subsequently Google) which specific Gemini model to use.
            model=self.model,
            # Step 1c: Pass Through Messages
            # The `messages` list (conversation history) is passed directly to the
            # unified client.
            messages=messages,
            # Step 1d: Pass Through Standard Optional Parameters
            # Optional parameters like `max_tokens` and `temperature` are also
            # passed through. If they are None, the unified client or the
            # backend service might use default values.
            max_tokens=max_tokens,
            temperature=temperature,
            # Step 1e: Pass Through All Additional Keyword Arguments
            # Any other keyword arguments passed via `**kwargs` are unpacked
            # and passed directly to the unified client. These could be other
            # Gemini-specific parameters not explicitly listed in this method's signature
            # (e.g., top_p, top_k, safety_settings).
            **kwargs,
        )
        # Step 2: Return the Response
        # The `self._unified_client.chat()` method is expected to make the HTTP request,
        # handle potential network errors or API errors from the unified service,
        # and return the JSON response from the Google Gemini API (as proxied by the
        # unified service). This response is then returned directly by this method.


# This list defines the public interface of this module.
# When someone does `from your_module import *`, only these names will be imported.
__all__ = [
    "GeminiClient",
    "SDKError",
    "APIRequestError",
    "ConnectionError",
    "TimeoutError",
]
