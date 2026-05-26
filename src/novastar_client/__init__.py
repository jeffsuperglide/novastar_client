"""
Importing all the modules
"""

# __version__ = "1.0.0"
# my_package/__init__.py
from importlib.metadata import version, PackageNotFoundError

from novastar_client import models
from novastar_client import services
from novastar_client import transform

from novastar_client.client import NovaStarClient
from novastar_client.config import NovaStarConfig
from novastar_client.session import NovaStarSession

__all__ = [
    "models",
    "services",
    "transform",
    "NovaStarClient",
    "NovaStarConfig",
    "NovaStarSession",
    "cli",  # type: ignore
]

try:
    __version__ = version("my-package")
except PackageNotFoundError:
    __version__ = "v0.1.0"  # or some sensible default
