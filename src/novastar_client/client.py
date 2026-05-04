"""NovaStarClient Class"""

import logging

from novastar_client.logging_utils import configure_package_logging
from novastar_client.config import NovaStarConfig
from novastar_client.services.station import StationsAPI
from novastar_client.services.timeseries import TimeSeriesAPI
from novastar_client.services.tscatalog import TimeSeriesCatalogAPI
from novastar_client.services.datatype import DataTypesAPI
from novastar_client.session import NovaStarSession

logger = logging.getLogger(__name__)


class NovaStarClient:
    """Client Class defining configurations and endpoint APIs

    Package APIs are defined here with a NovaStarSession class as an argument.
    """

    def __init__(
        self, config: NovaStarConfig | None = None, auth_token: str | None = None
    ):

        self.config = config or NovaStarConfig()

        configure_package_logging(self.config)
        logger.info(
            "NovaStar configurations: base url=%s api root=%s api version=%s"
            " timeout=%s verify ssl=%s",
            self.config.base_url,
            self.config.api_root,
            self.config.api_version,
            self.config.timeout,
            self.config.verify_ssl,
        )

        self.session = NovaStarSession(self.config, auth_token=auth_token)

        self.stations = StationsAPI(self.session)
        self.tscatalog = TimeSeriesCatalogAPI(self.session)
        self.timeseries = TimeSeriesAPI(self.session)
        self.datatypes = DataTypesAPI(self.session)
