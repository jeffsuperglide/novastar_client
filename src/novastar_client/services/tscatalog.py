"""NovaStar Time Series Catalog API

Returns
-------
StationsResponse
    StationsResponse is a class
"""

from dataclasses import dataclass
from typing import Any, Dict

from novastar_client.session import NovaStarSession
from novastar_client.models import TsCatalogResponse


@dataclass
class TimeSeriesCatalogAPI:
    """TimeSeriesCatalogAPI getting a list of Response classes"""

    def __init__(self, session: NovaStarSession):
        self.session = session
        self.path = "tscatalog"
        self.default_params: Dict[str, Any] = {
            "dataInterval": "*",
            "dataType": "*",
            "debug": str(False).lower(),
            "format": "json",
            "formatPrettyPrint": str(True).lower(),
            "includeAlarmTs": str(True).lower(),
            "includeCalibrationTs": str(True).lower(),
            "includeNovaScoreTs": str(True).lower(),
            "includeProblemTs": str(True).lower(),
            "includeRatedTs": str(True).lower(),
            "includeRatingTs": str(True).lower(),
            "includeRawTs": str(True).lower(),
            "includeScaledTs": str(True).lower(),
            "includeStandardCalculatedIntervalTs": str(True).lower(),
            "jsonFormat": "full",
            "xmlFormat": "full",
        }

    def get(self, *, raw: bool = False, **kwargs) -> TsCatalogResponse:
        """get tscatalog

        Returns
        -------
        TsCatalogResponse
            TsCatalogResponse class from tscatalog returned json
        """

        params: Dict[str, str] = {**self.default_params, **kwargs}
        data: Any = self.session.get(self.path, params=params)

        if raw:
            return data

        return TsCatalogResponse.from_api(data)
