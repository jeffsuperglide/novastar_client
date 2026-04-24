"""NovaStar Stations API

Returns
-------
StationsResponse
    StationsResponse is a class
"""

from dataclasses import dataclass
from typing import Any

from src.novastar_client.models import StationsResponse


@dataclass
class StationsAPI:
    """StationsAPI getting a list of StationsResponse classes"""

    def __init__(self, session):
        self.session = session
        self.path = "stations"

    def get(self, **kwargs) -> StationsResponse:
        """get stations

        Returns
        -------
        StationsResponse
            StationsResonse class from stations returned json
        """

        data: Any = self.session.get(self.path, params={**kwargs})
        return StationsResponse.from_api(data)
