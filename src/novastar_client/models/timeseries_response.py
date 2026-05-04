"""TimeSeriesResponse"""

import logging
from dataclasses import asdict, dataclass
from typing import List, Dict, Any

from novastar_client.models.meta import ApiVersion, AttributionAndUsage, ResponseInfo
from novastar_client.models.timeseries import TimeSeries, TimeSeriesProperties

logger = logging.getLogger(__name__)


@dataclass
class TimeSeriesResponse:
    """TimeSeriesResponse dataclass handling multiple parts of the NovaStar
    Time Series (ts) returned payload.  Differences returned when 'jsonFormat' query parameter
    set to 'bare' or 'named'.
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
    def from_api(cls, data: Dict) -> "TimeSeriesResponse":
        """from_api convert json to class

        Parameters
        ----------
        data : Dict
            NovaStar json payload described by Time Series (TS) (see NovaStar API Schemas).

        Returns
        -------
        TimeSeriesResponse class
            ApiVersion, AttributionAndUsage, ResponseInfo, and TimeSeries dataclasses.
        """

        return cls(
            api_version=ApiVersion.from_api(data.get("apiVersion", {})),
            attribution_and_usage=AttributionAndUsage.from_api(
                data.get("attributionAndUsage", {})
            ),
            response_info=ResponseInfo.from_api(data.get("responseInfo", {})),
            timeseries=TimeSeries.from_api(data.get("ts", {})),
        )

    def get_properties(self) -> TimeSeriesProperties:
        """get_properties TimeSeries dataclass properties

        Returns
        -------
        TimeSeriesProperties
            TimeSeriesProperties dataclass
        """

        return self.timeseries.properties

    def get_properties_asdict(self) -> Dict[str, Any]:
        """get_properties TimeSeries dataclass properties

        Returns
        -------
        Dict
            Dictionary of TimeSeries dataclass properties
        """
        return asdict(self.timeseries.properties)

    def get_data(self) -> list:
        """get_data TimeSeriesResponse data

        Returns
        -------
        list
            TimeSeries data
        """
        return [asdict(item) for item in self.timeseries.data]

    def get_data_field(self, field_name: str) -> List | None:
        """get_data_field getting a specific field from the TimeSeries data field

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
            logger.warning("Field name '%s' not valid.", field_name)
            return None

        default_value = self.default_values[field_name]

        return [
            getattr(item, field_name, default_value) for item in self.timeseries.data
        ]

    def get_data_fields(self, *field_names) -> List[Dict[str, Any]]:
        """get_data_fields getting a specific set of fields from the TimeSeries data field

        Returns
        -------
        List[Dict[str,Any]]
            The return is a list of dictionary objects defined by the input field names.
        """

        # get field names if None.
        if not field_names:
            field_names = self.default_values

        # Determine if there are any invalid field names.
        invalid_fields = [
            name for name in field_names if name not in self.default_values
        ]
        # Get only the valid field names
        valid_names = [name for name in field_names if name in self.default_values]

        if invalid_fields:
            logger.warning(
                "Field name(s) are not valid", extra={"invalid": invalid_fields}
            )

        return [
            {
                name: getattr(item, name, self.default_values[name])
                for name in valid_names
            }
            for item in self.timeseries.data
        ]
