"""StationResponse"""

from dataclasses import dataclass
from typing import Dict, List

from novastar_client.models.meta import ApiVersion, AttributionAndUsage, ResponseInfo
from novastar_client.models.normalize_payload import normalize_payload_with_sequence
from novastar_client.models.station import Station


@dataclass
class StationResponse:
    """StationResponse dataclass handling multiple parts of the NovaStar
    Station returned payload.  Differences returned when 'jsonFormat' query parameter
    set to 'bare' or 'named'.

    """

    api_version: ApiVersion
    attribution_and_usage: AttributionAndUsage
    response_info: ResponseInfo
    stations: List[Station]
    sequence_key: str = "stations"

    @classmethod
    def from_api(cls, data: Dict) -> "StationResponse":
        """from_api classmethod parsing json to this dataclass

        Parameters
        ----------
        data : Dict
            NovaStar json payload described by Station (see NovaStar API Schemas).

        Returns
        -------
        StationResponse
            ApiVersion, AttributionAndUsage, ResponseInfo, and Station dataclasses.
        """

        meta, data = normalize_payload_with_sequence(data, cls.sequence_key)  # type: ignore

        return cls(
            api_version=ApiVersion.from_api(meta.get("apiVersion", {})),
            attribution_and_usage=AttributionAndUsage.from_api(
                meta.get("attributionAndUsage", {})
            ),
            response_info=ResponseInfo.from_api(meta.get("responseInfo", {})),
            stations=[Station.from_api(item) for item in data],
        )
