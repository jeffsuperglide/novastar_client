"""TsCatalogResponse class defining the class for the 'tscatalog' endpoint returned json

Returns
-------
TsCatalogResponse
    json to class return
"""

from dataclasses import dataclass
from typing import List

from novastar_client.models.meta import ApiVersion, AttributionAndUsage, ResponseInfo
from novastar_client.models.normalize_payload import normalize_payload_with_sequence
from novastar_client.models.tscatalog import TsCatalogItem


@dataclass
class TsCatalogResponse:
    """TsCatalogResponse class

    Returns
    -------
    StationsRespnse class
        dataclass with meta plus tscatalog attributes
    """

    api_version: ApiVersion
    attribution_and_usage: AttributionAndUsage
    response_info: ResponseInfo
    tscatalog: List[TsCatalogItem]
    sequence_key: str = "tscatalog"

    @classmethod
    def from_api(cls, data: dict) -> "TsCatalogResponse":
        """from_api convert json to class

        Parameters
        ----------
        data : dict
            input json as a dict

        Returns
        -------
        TsCatalogResponse
            class with attributes meta plus tscatalog
        """

        meta, data = normalize_payload_with_sequence(data, cls.sequence_key)  # type: ignore

        return cls(
            api_version=ApiVersion.from_api(meta.get("apiVersion", {})),
            attribution_and_usage=AttributionAndUsage.from_api(
                meta.get("attributionAndUsage", {})
            ),
            response_info=ResponseInfo.from_api(meta.get("responseInfo", {})),
            tscatalog=[TsCatalogItem.from_api(item) for item in data],
        )

    def get_tsids(self) -> list[str]:
        return [item.time_series_identifier for item in self.tscatalog]
