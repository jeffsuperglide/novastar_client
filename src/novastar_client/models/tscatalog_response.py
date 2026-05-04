"""TsCatalogResponse class defining the class for the 'tscatalog' endpoint returned json"""

from collections import defaultdict
from dataclasses import asdict, dataclass
from typing import Any, Dict, List

from novastar_client.models.meta import ApiVersion, AttributionAndUsage, ResponseInfo
from novastar_client.models.normalize_payload import normalize_payload_with_sequence
from novastar_client.models.tscatalog import TsCatalogItem


@dataclass
class TsCatalogResponse:
    """TsCatalogResponse dataclass handling multiple parts of the NovaStar
    Time Series Catalog (tscatalog) returned payload.  Differences returned
    when 'jsonFormat' query parameter set to 'bare' or 'named'.
    """

    api_version: ApiVersion
    attribution_and_usage: AttributionAndUsage
    response_info: ResponseInfo
    tscatalog: List[TsCatalogItem]
    sequence_key: str = "tscatalog"

    @classmethod
    def from_api(cls, data: Dict) -> "TsCatalogResponse":
        """from_api convert json to class

        Parameters
        ----------
        data : Dict
            NovaStar json payload described by tscatalog endpoint (see NovaStar API Schemas).

        Returns
        -------
        TsCatalogResponse
            ApiVersion, AttributionAndUsage, ResponseInfo, and TsCatalogItem dataclasses.
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

    def get_tsids(self) -> List[str]:
        """get_tsids class method

        Returns
        -------
        List[str]
            List of Time Series IDs.
        """
        return [item.time_series_identifier for item in self.tscatalog]

    def get_catalog_by_id(self) -> List[List[TsCatalogItem]]:
        """get_catalog_by_id class method

        Returns
        -------
        List[List[TsCatalogItem]]
            List of Time Series Catalogs grouped by station.
        """
        groups: dict[str, List[TsCatalogItem]] = defaultdict(list)

        for cat in self.tscatalog:
            groups[cat.loc_id].append(cat)

        return [groups[k] for k in sorted(groups)]

    def get_catalog_by_name(self) -> dict[str, list[dict[str, Any]]]:
        """get_catalog_by_name method returns a dictionary with station names
        as the key and a list of catalog dictionaries as the value.


        Returns
        -------
        dict[str, list[dict[str,Any]]]
            List of catalogs grouped by station name.
        """
        groups = defaultdict(list)

        for cat in self.tscatalog:
            groups[cat.station_name].append(asdict(cat))

        return dict(sorted(groups.items()))
