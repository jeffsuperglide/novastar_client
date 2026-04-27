"""
NovaStarClient Class
"""

from novastar_client.config import NovaStarConfig
from novastar_client.services.station import StationsAPI
from novastar_client.services.tscatalog import TimeSeriesCatalogAPI
from novastar_client.services.timeseries import TimeSeriesAPI
from novastar_client.session import NovaStarSession


class NovaStarClient:
    """Client Class defining configurations and endpoint APIs"""

    def __init__(
        self, config: NovaStarConfig | None = None, auth_token: str | None = None
    ):

        self.config = config or NovaStarConfig()
        self.session = NovaStarSession(self.config, auth_token=auth_token)

        self.stations = StationsAPI(self.session)
        self.tscatalog = TimeSeriesCatalogAPI(self.session)
        self.timeseries = TimeSeriesAPI(self.session)
