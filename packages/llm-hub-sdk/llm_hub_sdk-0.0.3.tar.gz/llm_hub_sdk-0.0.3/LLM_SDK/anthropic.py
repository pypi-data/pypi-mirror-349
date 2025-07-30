from typing import Dict, List, Any, Optional
from .core import UnifiedChatClient
from .exceptions import SDKError, APIRequestError, ConnectionError, TimeoutError


class AnthropicClient:
    """Client specifically for interacting with Anthropic models."""

    # This class variable defines the provider identifier used when
    # communicating with the UnifiedChatClient. It tells the unified
    # service to route requests to its Anthropic integration.
    _PROVIDER_NAME = "anthropic"

    def __init__(self, base_url: str, model: str, timeout: int = 60):
        """
        Initializes the Anthropic client for a specific model.

        Args:
            base_url: Base URL of the unified FastAPI service.
            model: The specific Claude model name this client instance will use.
            timeout: Request timeout in seconds.
        """
        # --- Initialization Flow ---

        # Step 1: Instantiate the Unified Client
        # A UnifiedChatClient instance is created. This unified client is responsible
        # for the actual HTTP communication with the backend FastAPI service.
        # It's configured with the base_url of that service and a request timeout.
        self.unified_client = UnifiedChatClient(base_url, timeout)

        # Step 2: Validate the Model Name
        # It's crucial that an Anthropic model (e.g., "claude-3-opus-20240229")
        # is specified for this client instance. If no model name is provided,
        # it raises a ValueError because the client wouldn't know which Anthropic
        # model to target.
        if not model:
            raise ValueError("An Anthropic model name must be provided.")

        # Step 3: Store the Model Name
        # The provided model name is stored as an instance attribute. This means
        # this specific AnthropicClient instance will always use this model
        # for its chat operations, unless overridden in a way not shown here.
        self.model = model

    def chat(
        self,
        messages: List[Dict[str, str]],
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Sends a chat request using the pre-configured Anthropic model.

        Args:
            messages: The list of message dictionaries.
            max_tokens: Optional maximum tokens for the response.
            temperature: Optional sampling temperature.
            **kwargs: Additional parameters. Should NOT include provider, model, or messages.

        Returns:
            The API response dictionary.
        """
        # --- Chat Request Flow ---

        # Step 1: Filter Additional Keyword Arguments
        # This line creates a new dictionary `filtered_kwargs`. It takes all
        # keyword arguments passed via `**kwargs` and excludes 'provider', 'model',
        # and 'messages'. This is to prevent accidental overriding of these
        # parameters, which are explicitly set by this AnthropicClient.
        # Other valid Anthropic parameters (e.g., top_p, stop_sequences)
        # passed in `**kwargs` will be preserved.
        filtered_kwargs = {
            k: v
            for k, v in kwargs.items()
            if k not in ["provider", "model", "messages"]
        }

        # Step 2: Delegate to the Unified Client's Chat Method
        # The actual API call is made by invoking the `chat` method of the
        # `self.unified_client` instance. This unified client handles the
        # communication with the backend FastAPI service.
        return self.unified_client.chat(
            # Step 2a: Specify the Provider
            # The `provider` argument is set to `self._PROVIDER_NAME` (which is "anthropic").
            # This tells the unified FastAPI service to route this request to its
            # Anthropic backend integration.
            provider=self._PROVIDER_NAME,
            # Step 2b: Specify the Model
            # The `model` argument is set to `self.model` (the model name stored
            # during initialization, e.g., "claude-3-opus-20240229"). This tells the
            # unified service (and subsequently Anthropic) which specific model to use.
            model=self.model,
            # Step 2c: Pass Through Messages
            # The `messages` list (conversation history) is passed directly to the
            # unified client.
            messages=messages,
            # Step 2d: Pass Through Standard Optional Parameters
            # Optional parameters like `max_tokens` and `temperature` are also
            # passed through. If they are None, the unified client or the
            # backend service might use default values.
            max_tokens=max_tokens,
            temperature=temperature,
            # Step 2e: Pass Through Filtered Additional Parameters
            # Any other keyword arguments (now in `filtered_kwargs`) are unpacked
            # and passed to the unified client. These could be other Anthropic-specific
            # parameters not explicitly listed in this method's signature.
            **filtered_kwargs,
        )
        # Step 3: Return the Response
        # The `self.unified_client.chat()` method is expected to make the HTTP request,
        # handle potential network errors or API errors from the unified service,
        # and return the JSON response from the Anthropic API (as proxied by the
        # unified service). This response is then returned directly by this method.


# This list defines the public interface of this module.
# When someone does `from your_module import *`, only these names will be imported.
__all__ = [
    "AnthropicClient",
    "SDKError",
    "APIRequestError",
    "ConnectionError",
    "TimeoutError",
]
