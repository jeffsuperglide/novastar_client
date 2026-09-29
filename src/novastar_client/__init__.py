"""
Importing all the modules
"""

# __version__ = "1.0.0"
# my_package/__init__.py
from importlib.metadata import PackageNotFoundError, version

from packaging.version import Version

from novastar_client import models, services, transform
from novastar_client.client import NovaStarClient
from novastar_client.config import NovaStarConfig
from novastar_client.session import NovaStarSession

__all__ = [
    "NovaStarClient",
    "NovaStarConfig",
    "NovaStarSession",
    "cli",  # type: ignore
    "models",
    "services",
    "transform",
]

try:
    raw_version = version("novastar_client")
    __version__ = f"v{Version(raw_version).base_version}"
except PackageNotFoundError:
    __version__ = "v0.1.0"  # or some sensible default
