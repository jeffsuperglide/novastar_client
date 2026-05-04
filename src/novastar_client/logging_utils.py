"""Package logging utilities"""

import logging

from novastar_client.config import NovaStarConfig

logging.getLogger("novastar_client").addHandler(logging.NullHandler())


def configure_package_logging(config: NovaStarConfig) -> None:
    """configure_package_logging configure logging at package level.

    Parameters
    ----------
    config : NovaStarConfig
        novastar_client configuration dataclass.
    """

    level_name = config.log_level.upper()
    level = getattr(logging, level_name, logging.INFO)

    root = logging.getLogger()
    root.handlers.clear()

    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(config.log_format))

    root.setLevel(level)
    root.addHandler(handler)
