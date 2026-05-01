"""DataTypeResponse"""

from dataclasses import asdict, dataclass
from typing import Any, Dict, List

from novastar_client.models.meta import ApiVersion, AttributionAndUsage, ResponseInfo
from novastar_client.models.datatype import DataType


@dataclass
class DataTypeResponse:
    """DataTypeResponse dataclass handling multiple parts of the NovaStar
    DataType returned payload.  Differences returned when 'jsonFormat' query parameter
    set to 'bare' or 'named'.
    """

    api_version: ApiVersion
    attribution_and_usage: AttributionAndUsage
    response_info: ResponseInfo
    datatypes: List[DataType]

    @classmethod
    def from_api(cls, data: Dict) -> "DataTypeResponse":
        """from_api classmethod parsing json to this dataclass

        Parameters
        ----------
        data : Dict
            NovaStar json payload described by DataType (see NovaStar API Schemas).

        Returns
        -------
        DataTypeResponse
            ApiVersion, AttributionAndUsage, ResponseInfo, and DataType dataclasses.
        """

        return cls(
            api_version=ApiVersion.from_api(data.get("apiVersion", {})),
            attribution_and_usage=AttributionAndUsage.from_api(
                data.get("attributionAndUsage", {})
            ),
            response_info=ResponseInfo.from_api(data.get("responseInfo", {})),
            datatypes=[DataType.from_api(item) for item in data.get("dataTypes", [])],
        )

    def to_dict(self) -> List[Dict[str, Any]]:
        """to_dict converts the DataTypes dataclass to a dictionary

        Returns
        -------
        List[Dict[str,Any]]
            DataTypes dataclass converted to a dictionary and returned
            in a list.
        """
        return [asdict(datatype) for datatype in self.datatypes]

    def filter_shef_only(self):
        for i in range(len(self.datatypes) - 1, -1, -1):
            if self.datatypes[i].data_type_source_type != "SHEF":
                self.datatypes.pop(i)
        return self
