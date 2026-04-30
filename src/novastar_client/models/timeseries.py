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
            point_compress_interval=payload["pointCompressInterval"],
            point_description=payload.get("pointDescription", ""),
            point_id=payload["pointId"],
            point_line=payload["pointLine"],
            point_name=payload["pointName"],
            point_no_report_interval=payload["pointNoReportInterval"],
            point_num_id=payload["pointNumId"],
            point_out_of_service=payload["pointOutOfService"],
            point_plot_lower_limit=payload["pointPlotLowerLimit"],
            point_plot_upper_limit=payload["pointPlotUpperLimit"],
            point_point_type_id=payload["pointPointTypeId"],
            point_rated=payload["pointRated"],
            point_remote_id=payload["pointRemoteId"],
            point_sensor_id=payload["pointSensorId"],
            point_tag_name=payload["pointTagName"],
            point_type_id=payload["pointTypeId"],
            point_type_name=payload["pointTypeName"],
            point_type_shef_parameter_code=payload["pointTypeShefParameterCode"],
            station_num_id=payload["stationNumId"],
            station_id=payload["stationId"],
            station_name=payload["stationName"],
            station_description=payload.get("stationDescription", ""),
            station_tag_name=payload["stationTagName"],
            station_remote_tag=payload["stationRemoteTag"],
            station_out_of_service=payload["stationOutOfService"],
            station_latitude=payload["stationLatitude"],
            station_longitude=payload["stationLongitude"],
            station_elevation=payload["stationElevation"],
            station_type_description=payload.get("stationTypeDescription", ""),
            station_type_id=payload["stationTypeId"],
            station_type_line=payload["stationTypeLine"],
            station_type_name=payload["stationTypeName"],
            station_type_protocol=payload["stationTypeProtocol"],
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
    description: Optional[str]
    units: Optional[str]
    value_digits: Optional[int]

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
            format=payload["format"],
            loc_id=payload["locId"],
            data_type=payload["dataType"],
            data_interval=payload["dataInterval"],
            description=payload.get("description"),
            units=payload.get("units"),
            value_digits=payload.get("valueDigits"),
            properties=TimeSeriesProperties.from_api(payload.get("properties", {})),
            data=[TimeSeriesPoint.from_api(d) for d in payload.get("data", [])],
        )
