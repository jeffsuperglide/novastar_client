# src/novastar_client/models/stations_response.py
from dataclasses import dataclass
from typing import List

from .meta import ApiVersion, AttributionAndUsage, ResponseInfo
from .station import Station


@dataclass
class StationsResponse:
    api_version: ApiVersion
    attribution_and_usage: AttributionAndUsage
    response_info: ResponseInfo
    stations: List[Station]

    @classmethod
    def from_api(cls, data: dict) -> "StationsResponse":
        return cls(
            api_version=ApiVersion.from_api(data.get("apiVersion", {})),
            attribution_and_usage=AttributionAndUsage.from_api(
                data.get("attributionAndUsage", {})
            ),
            response_info=ResponseInfo.from_api(data.get("responseInfo", {})),
            stations=[Station.from_api(item) for item in data.get("stations", [])],
        )
