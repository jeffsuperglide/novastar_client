"""TimeSeries dataclass"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any


from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class TimeSeriesProperties:
    """Time Series properties in a NovaStar time series schema."""

    point_compress_interval: int
    point_description: str
    point_id: int
    point_line: int
    point_name: str
    point_no_report_interval: int
    point_num_id: int
    point_out_of_service: bool
    point_plot_lower_limit: float
    point_plot_upper_limit: float
    point_point_type_id: int
    point_rated: bool
    point_remote_id: int
    point_sensor_id: int
    point_tag_name: str
    point_type_id: int
    point_type_name: str
    point_type_shef_parameter_code: str

    station_num_id: int
    station_id: int
    station_name: str
    station_description: str
    station_tag_name: str
    station_remote_tag: str
    station_out_of_service: bool
    station_latitude: float
    station_longitude: float
    station_elevation: float
    station_type_description: str
    station_type_id: int
    station_type_line: int
    station_type_name: str
    station_type_protocol: str

    @classmethod
    def from_api(cls, payload: Dict[str, Any]) -> "TimeSeriesProperties":
        """from_api Build TimeSeriesProperties dataclass from the properties field

        Parameters
        ----------
        payload : Dict[str, Any]
            The dictionary payload from the properties part.

        Returns
        -------
        TimeSeriesProperties
            Time Series properties dataclass
        """
        return cls(
            point_compress_interval=payload.get("pointCompressInterval", 0),
            point_description=payload.get("pointDescription", ""),
            point_id=payload.get("pointId", 0),
            point_line=payload.get("pointLine", 0),
            point_name=payload.get("pointName", ""),
            point_no_report_interval=payload.get("pointNoReportInterval", 0),
            point_num_id=payload.get("pointNumId", 0),
            point_out_of_service=payload.get("pointOutOfService", True),
            point_plot_lower_limit=payload.get("pointPlotLowerLimit", 0.0),
            point_plot_upper_limit=payload.get("pointPlotUpperLimit", 0.0),
            point_point_type_id=payload.get("pointPointTypeId", 0),
            point_rated=payload.get("pointRated", False),
            point_remote_id=payload.get("pointRemoteId", 0),
            point_sensor_id=payload.get("pointSensorId", 0),
            point_tag_name=payload.get("pointTagName", ""),
            point_type_id=payload.get("pointTypeId", 0),
            point_type_name=payload.get("pointTypeName", ""),
            point_type_shef_parameter_code=payload.get(
                "pointTypeShefParameterCode", ""
            ),
            station_num_id=payload.get("stationNumId", 0),
            station_id=payload.get("stationId", 0),
            station_name=payload.get("stationName", ""),
            station_description=payload.get("stationDescription", ""),
            station_tag_name=payload.get("stationTagName", ""),
            station_remote_tag=payload.get("stationRemoteTag", ""),
            station_out_of_service=payload.get("stationOutOfService", True),
            station_latitude=payload.get("stationLatitude", 0.0),
            station_longitude=payload.get("stationLongitude", 0.0),
            station_elevation=payload.get("stationElevation", 0.0),
            station_type_description=payload.get("stationTypeDescription", ""),
            station_type_id=payload.get("stationTypeId", 0),
            station_type_line=payload.get("stationTypeLine", 0),
            station_type_name=payload.get("stationTypeName", ""),
            station_type_protocol=payload.get("stationTypeProtocol", ""),
        )


@dataclass
class TimeSeriesPoint:
    """Single data point (TSData) in a NovaStar time series."""

    dt: str  # e.g. "2026-03-28T11:00:00-05:00"
    flag: str  # 'f' in payload
    duration: int  # 'd' in payload (seconds)
    status: int  # 's' in payload
    value: float  # 'v' in payload

    @classmethod
    def from_api(cls, data: Dict[str, Any]) -> "TimeSeriesPoint":
        """from_api classmethod parsing json to this dataclass

        Parameters
        ----------
        data : Dict[str, Any]
            NovaStar json payload described by TSData (see NovaStar API Schemas).

        Returns
        -------
        TimeSeriesPoint
            dataclass for the NovaStar TSData.
        """
        return cls(
            dt=data["dt"],
            flag=data["f"],
            duration=data["d"],
            status=data["s"],
            value=data["v"],
        )


@dataclass
class TimeSeries:
    """TimeSeries dataclass for the NovaStar Time Series (ts) endpoint JSON payload.

    Represents the 'ts' object (metadata + list of data points).

    """

    format: str
    loc_id: str
    data_type: str
    data_interval: str
    description: str
    units: str
    value_digits: int

    # All point and station metadata live under 'properties' in the payload.
    properties: TimeSeriesProperties

    # The actual series of measurements.
    data: List[TimeSeriesPoint]

    @classmethod
    def from_api(cls, payload: Dict[str, Any]) -> "TimeSeries":
        """Build a TimeSeries from the 'ts' section of the API response.

        Returns
        -------
        TimeSeries
            dataclass for the NovaStar Time Series (ts) endpoint returned json payload
        """

        return cls(
            format=payload.get("format", ""),
            loc_id=payload.get("locId", ""),
            data_type=payload.get("dataType", ""),
            data_interval=payload.get("dataInterval", ""),
            description=payload.get("description", ""),
            units=payload.get("units", ""),
            value_digits=payload.get("valueDigits", 0),
            properties=TimeSeriesProperties.from_api(payload.get("properties", {})),
            data=[TimeSeriesPoint.from_api(d) for d in payload.get("data", [])],
        )
