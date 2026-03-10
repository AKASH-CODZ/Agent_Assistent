"""
Core package for Akash AI Backend.
Contains configuration and security modules.
"""

from .config import settings
from .security import setup_cors

__all__ = ["settings", "setup_cors"]