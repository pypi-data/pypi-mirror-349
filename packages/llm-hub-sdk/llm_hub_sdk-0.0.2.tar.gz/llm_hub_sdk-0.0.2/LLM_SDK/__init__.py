# SDK/__init__.py (Temporary Debug Version)
import sys
import os

print(f"--- Executing SDK/__init__.py ---")
print(f"Current directory: {os.getcwd()}")
print(f"Python Path: {sys.path}")
print(f"Attempting to import submodules...")

try:
    from . import gemini

    print(f"Successfully imported .gemini: {gemini}")
except ImportError as e:
    print(f"!!! FAILED to import .gemini: {e}")
    # Optionally: raise e # Re-raise to see full traceback if needed

try:
    from . import openai

    print(f"Successfully imported .openai: {openai}")
except ImportError as e:
    print(f"!!! FAILED to import .openai: {e}")

try:
    from . import anthropic

    print(f"Successfully imported .anthropic: {anthropic}")
except ImportError as e:
    print(f"!!! FAILED to import .anthropic: {e}")

try:
    from .core import SDKError, APIRequestError, ConnectionError, TimeoutError

    print("Successfully imported exceptions from .core")
except ImportError as e:
    print(f"!!! FAILED to import exceptions from .core: {e}")


# Define __all__ (keep as before or simplify)
__all__ = [
    "gemini",
    "openai",
    "anthropic",
    "SDKError",
    "APIRequestError",
    "ConnectionError",
    "TimeoutError",
]

print(f"--- Finished SDK/__init__.py ---")
