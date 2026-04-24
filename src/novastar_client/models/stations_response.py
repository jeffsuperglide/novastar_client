"""StationsResponse class defining the class for the 'stations' endpoint returned json

Returns
-------
StationsResonse
    json to class return
"""

from dataclasses import dataclass
from typing import List

from novastar_client.models.meta import ApiVersion, AttributionAndUsage, ResponseInfo
from novastar_client.models.normalize_payload import normalize_payload_with_sequence
from novastar_client.models.station import Station


@dataclass
class StationsResponse:
    """StationsResponse class

    Returns
    -------
    StationsRespnse class
        dataclass with meta plus stations attributes
    """

    api_version: ApiVersion
    attribution_and_usage: AttributionAndUsage
    response_info: ResponseInfo
    stations: List[Station]
    sequence_key: str = "stations"

    @classmethod
    def from_api(cls, data: dict) -> "StationsResponse":
        """from_api convert json to class

        Parameters
        ----------
        data : dict
            input json as a dict

        Returns
        -------
        StationsResponse
            class with attributes meta plus stations
        """

        meta, data = normalize_payload_with_sequence(data, cls.sequence_key)

        return cls(
            api_version=ApiVersion.from_api(meta.get("apiVersion", {})),
            attribution_and_usage=AttributionAndUsage.from_api(
                meta.get("attributionAndUsage", {})
            ),
            response_info=ResponseInfo.from_api(meta.get("responseInfo", {})),
            stations=[Station.from_api(item) for item in data],
        )
