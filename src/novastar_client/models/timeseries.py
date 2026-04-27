"""TimeSeries dataclass

Returns
-------
TimeSeries
    dataclass for the NovaStar time series endpoint return json payload
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any


@dataclass
class TimeSeriesPoint:
    """Single data point in a NovaStar time series.

    Returns
    -------
    TimeSeriesPoint
        Time Series Point dataclass
    """

    dt: str  # e.g. "2026-03-28T11:00:00-05:00"
    flag: str  # 'f' in payload
    duration: int  # 'd' in payload (seconds)
    status: int  # 's' in payload
    value: float  # 'v' in payload

    @classmethod
    def from_api(cls, data: Dict[str, Any]) -> "TimeSeriesPoint":
        return cls(
            dt=data["dt"],
            flag=data["f"],
            duration=data["d"],
            status=data["s"],
            value=data["v"],
        )


@dataclass
class TimeSeries:
    """TimeSeries dataclass for the NovaStar ts endpoint JSON payload.

    Represents the 'ts' object (metadata + list of data points).

    Returns
    -------
    TimeSeries
        Time Series dataclass
    """

    format: str
    loc_id: str
    data_type: str
    data_interval: str
    description: Optional[str]
    units: Optional[str]
    value_digits: Optional[int]

    # All point and station metadata live under 'properties' in the payload.
    properties: Dict[str, Any]

    # The actual series of measurements.
    data: List[TimeSeriesPoint]

    @classmethod
    def from_api(cls, payload: Dict[str, Any]) -> "TimeSeries":
        """Build a TimeSeries from the 'ts' section of the API response.

        Expects to receive data = response_json["ts"].
        """

        return cls(
            format=payload["format"],
            loc_id=payload["locId"],
            data_type=payload["dataType"],
            data_interval=payload["dataInterval"],
            description=payload.get("description"),
            units=payload.get("units"),
            value_digits=payload.get("valueDigits"),
            properties=payload.get("properties", {}),
            data=[TimeSeriesPoint.from_api(d) for d in payload.get("data", [])],
        )
