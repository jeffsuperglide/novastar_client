"""Stations Service API"""

import dataclasses
from typing import Any, Dict

from novastar_client.models import StationResponse
from novastar_client.session import NovaStarSession


@dataclasses.dataclass
class StationsAPI:
    """StationsAPI dataclass"""

    def __init__(self, session: NovaStarSession):
        self.session = session
        self.path = "stations"
        self.default_params: Dict[str, Any] = {
            "debug": str(False).lower(),
            "format": "json",
            "formatPrettyPrint": str(False).lower(),
            "includeRetiredStations": str(False).lower(),
            "includeTestStations": str(False).lower(),
            "jsonFormat": "bare",
            "xmlFormat": "full",
        }

    def get(self, *, raw: bool = False, **kwargs) -> StationResponse | Dict | None:
        """NovaStarSession GET method providing raw json or StationResponse

        Returns
        -------
        StationResponse
            StationResponse dataclass defined in the models module.

        Dict
            Raw JSON.
        """

        params: Dict[str, str] = {**self.default_params, **kwargs}
        data: Any = self.session.get(self.path, params=params)

        # Handle data problem.
        if data is None:
            return None

        # Get the raw json.
        if raw:
            return data

        # Get the StationResponse dataclass.
        return StationResponse.from_api(data)
