"""
Importing all the modules
"""

__version__ = "0.1.0"

import logging

from novastar_client import models
from novastar_client import services
from novastar_client import transform

from novastar_client.client import NovaStarClient
from novastar_client.config import NovaStarConfig
from novastar_client.session import NovaStarSession
from novastar_client.exceptions import NovaStarAPIError

__all__ = [
    "models",
    "services",
    "transform",
    "NovaStarClient",
    "NovaStarConfig",
    "NovaStarSession",
    "NovaStarAPIError",
]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s: %(message)s",
)
