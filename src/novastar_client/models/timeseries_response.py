"""TimeSeriesResponse class defining the class for the 'tscatalog' endpoint returned json

Returns
-------
TimeSeriesResponse
    json to class return
"""

from dataclasses import asdict, dataclass, fields
from typing import List, Dict, Any, Tuple

from novastar_client.exceptions import NovaStarAPIError
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

    default_values = {
        "dt": "",
        "flag": "",
        "duration": 0,
        "status": 0,
        "value": 0.0,
    }

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

    def get_properties(self) -> Dict:
        """get_properties TimeSeries dataclass properties

        Returns
        -------
        Dict
            dictionary of TimeSeries dataclass properties
        """
        return {
            f.name: getattr(self.timeseries, f.name)
            for f in fields(self.timeseries)
            if f.name != "data"
        }

    def get_data(self) -> list:
        """get_data TimeSeriesResponse data

        Returns
        -------
        list
            TimeSeries data
        """
        return [asdict(item) for item in self.timeseries.data]

    def get_field(self, field_name: str) -> list:
        """get_field getting a specific field from the TimeSeries data field

        Parameters
        ----------
        field_name : str
            The field name.  Options are dt, flag, duration, status, or value

        Returns
        -------
        list
            List of values from the field input name.
        """

        if field_name not in self.default_values:
            raise NovaStarAPIError(
                f"Invalid field_name: {field_name}.  "
                f"Expected one of: {', '.join(self.default_values)}"
            ) from Exception()

        default_value = self.default_values[field_name]

        return [
            getattr(item, field_name, default_value) for item in self.timeseries.data
        ]

    def get_fields(self, *field_names) -> List[Tuple[Any]]:
        """get_fields getting a specific set of fields from the TimeSeries data field

        Returns
        -------
        List[Tuple[Any]]
            _description_
        """

        if not field_names:
            field_names = self.default_values

        invalid_fields = [name for name in field_names if name not in self.default_values.keys()]
        if invalid_fields:
            raise NovaStarAPIError(
                f"Invalid field name(s): {invalid_fields}.  "
                f"Expected one or more of: {self.default_values.keys()}"
            ) from Exception()

        return [
            tuple(getattr(item, name) for name in field_names)
            for item in self.timeseries.data
        ]
