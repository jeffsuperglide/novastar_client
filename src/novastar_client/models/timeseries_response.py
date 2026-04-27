"""TimeSeriesResponse class defining the class for the 'tscatalog' endpoint returned json

Returns
-------
TimeSeriesResponse
    json to class return
"""

from dataclasses import asdict, dataclass, fields
from typing import List, Dict, Any, Tuple

from novastar_client.models.meta import ApiVersion, AttributionAndUsage, ResponseInfo
from novastar_client.models.timeseries import TimeSeries


@dataclass
class TimeSeriesResponse:
    """TimeSeriesResponse class

    Returns
    -------
    StationsRespnse class
        dataclass with meta plus timeseries attributes
    """

    api_version: ApiVersion
    attribution_and_usage: AttributionAndUsage
    response_info: ResponseInfo
    timeseries: TimeSeries

    @classmethod
    def from_api(cls, data: dict) -> "TimeSeriesResponse":
        """from_api convert json to class

        Parameters
        ----------
        data : dict
            input json as a dict

        Returns
        -------
        TimeSeriesResponse
            class with attributes meta plus timeseries
        """

        return cls(
            api_version=ApiVersion.from_api(data.get("apiVersion", {})),
            attribution_and_usage=AttributionAndUsage.from_api(
                data.get("attributionAndUsage", {})
            ),
            response_info=ResponseInfo.from_api(data.get("responseInfo", {})),
            timeseries=TimeSeries.from_api(data.get("ts", {})),
        )

    def get_properties(self):
        return {
            f.name: getattr(self.timeseries, f.name)
            for f in fields(self.timeseries)
            if f.name != "data"
        }

    def get_data(self) -> list:
        return [asdict(item) for item in self.timeseries.data]

    def get_field(self, field_name: str) -> list:
        return [getattr(item, field_name) for item in self.timeseries.data]

    def get_fields(self, *field_names) -> List[Tuple[Any]]:
        return [
            tuple(getattr(item, name) for name in field_names)
            for item in self.timeseries.data
        ]
