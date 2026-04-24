"""
NovaStarClient Class
"""

from src.novastar_client.config import NovaStarConfig
from src.novastar_client.services.station import StationsAPI
from src.novastar_client.session import NovaStarSession


class NovaStarClient:
    """Client Class defining configurations and endpoint APIs"""

    def __init__(
        self, config: NovaStarConfig | None = None, auth_token: str | None = None
    ):

        self.config = config or NovaStarConfig()
        self.session = NovaStarSession(self.config, auth_token=auth_token)

        self.stations = StationsAPI(self.session)
        # self.timeseries = TimeSeriesAPI(self.session)
