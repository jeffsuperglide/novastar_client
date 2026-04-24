"""services init"""

from novastar_client.services.station import StationsAPI
from novastar_client.services.tscatalog import TimeSeriesCatalogAPI

__all__ = ["StationsAPI", "TimeSeriesCatalogAPI"]
