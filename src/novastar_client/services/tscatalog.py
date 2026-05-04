"""Time Series Catalog Servie API"""

import dataclasses
from typing import Any, Dict

from novastar_client.models import TsCatalogResponse
from novastar_client.session import NovaStarSession


@dataclasses.dataclass
class TimeSeriesCatalogAPI:
    """TimeSeriesCatalogAPI dataclass"""

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
            "jsonFormat": "bare",
            "xmlFormat": "full",
        }

    def get(self, *, raw: bool = False, **kwargs) -> TsCatalogResponse | None:
        """NovaStarSession GET method

        Returns
        -------
        TsCatalogResponse
            TsCatalogResponse dataclass defined in the models module.
        """

        params: Dict[str, str] = {**self.default_params, **kwargs}
        data: Any = self.session.get(self.path, params=params)

        if data is None:
            return None

        if raw:
            return data

        return TsCatalogResponse.from_api(data)
