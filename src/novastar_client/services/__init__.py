"""services init"""

from novastar_client.services.station import StationsAPI
from novastar_client.services.tscatalog import TimeSeriesCatalogAPI
from novastar_client.services.timeseries import TimeSeriesAPI

__all__ = ["StationsAPI", "TimeSeriesCatalogAPI", "TimeSeriesAPI"]
