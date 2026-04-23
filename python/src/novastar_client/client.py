# src/novastar_client/client.py
from .config import NovaStarConfig
from .session import NovaStarSession
from .services.stations import StationsAPI
from .services.timeseries import TimeSeriesAPI


class NovaStarClient:
    def __init__(
        self, config: NovaStarConfig | None = None, auth_token: str | None = None
    ):
        self.config = config or NovaStarConfig()
        self.session = NovaStarSession(self.config, auth_token=auth_token)

        self.stations = StationsAPI(self.session)
        self.timeseries = TimeSeriesAPI(self.session)
