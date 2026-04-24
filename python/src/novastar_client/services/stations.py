"""NovaStar Stations API

Returns
-------
StationsResponse
    StationsResponse is a class
"""

from dataclasses import dataclass
from typing import Any

from novastar_client.models import StationsResponse


@dataclass
class StationsAPI:
    """StationsAPI getting a list of StationsResponse classes"""

    stations_path: str = "stations"

    def __init__(self, session):
        self.session = session

    def get(self, **kwargs) -> StationsResponse:
        """get stations

        Returns
        -------
        StationsResponse
            StationsResonse class from stations returned json
        """
        params = {**kwargs}
        data: Any = self.session.get(self.stations_path, params=params)
        return StationsResponse.from_api(data)
