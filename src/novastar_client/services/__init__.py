"""services init"""

from novastar_client.services.station import StationsAPI
from novastar_client.services.tscatalog import TimeSeriesCatalogAPI
from novastar_client.services.timeseries import TimeSeriesAPI
from novastar_client.services.datatype import DataTypeResponse

__all__ = [
    "StationsAPI",
    "TimeSeriesCatalogAPI",
    "TimeSeriesAPI",
    "DataTypeResponse",
]
