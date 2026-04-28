"""Time Series Service API"""

import dataclasses
from typing import Any, Dict

from novastar_client.models import TimeSeriesResponse
from novastar_client.session import NovaStarSession


@dataclasses.dataclass
class TimeSeriesAPI:
    """TimeSeriesAPI dataclass"""

    def __init__(self, session: NovaStarSession):
        self.session = session
        self.path = "ts"
        self.default_params: Dict[str, Any] = {
            "dataService": "data",
            "debug": str(False).lower(),
            "flag": "*",
            "format": "json",
            "includeEstimates": str(False).lower(),
            "includeMissing": str(False).lower(),
            "includeProfile": str(False).lower(),
            "includeReports": str(True).lower(),
            "readData": str(True).lower(),
        }

    def get(self, *, raw: bool = False, **kwargs) -> TimeSeriesResponse:
        """NovaStarSession GET method

        Returns
        -------
        TimeSeriesResponse
            TimeSeriesResponse dataclass defined in the models module.
        """

        params: Dict[str, str] = {**self.default_params, **kwargs}
        data: Any = self.session.get(self.path, params=params)

        if raw:
            return data

        return TimeSeriesResponse.from_api(data)
