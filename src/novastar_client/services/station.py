"""NovaStar Stations API

Returns
-------
StationsResponse
    StationsResponse is a class
"""

from dataclasses import dataclass
from typing import Any, Dict

from novastar_client.helpers import with_urlencoded_kwargs
from novastar_client.session import NovaStarSession
from novastar_client.models import StationsResponse


@dataclass
class StationsAPI:
    """StationsAPI getting a list of StationsResponse classes"""

    def __init__(self, session: NovaStarSession):
        self.session = session
        self.path = "stations"
        self.default_params: Dict[str, Any] = {
            "debug": str(False).lower(),
            "format": "json",
            "formatPrettyPrint": str(False).lower(),
            "includeRetiredStations": str(False).lower(),
            "includeTestStations": str(False).lower(),
            "jsonFormat": "full",
            "xmlFormat": "full",
        }

    def get(self, *, raw: bool = False, **kwargs) -> StationsResponse:
        """get stations

        Returns
        -------
        StationsResponse
            StationsResonse class from stations returned json
        """

        params: Dict[str, str] = with_urlencoded_kwargs(
            self.default_params, **kwargs
        )
        data: Any = self.session.get(self.path, params=params)

        if raw:
            return data

        return StationsResponse.from_api(data)
