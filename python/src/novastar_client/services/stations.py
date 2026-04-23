# src/novastar_client/services/stations.py
from __future__ import annotations
from typing import Any, Iterable, Optional


class StationsAPI:
    def __init__(self, session):
        self.session = session

    def list(
        self,
        *,
        station_num_ids: Optional[Iterable[int]] = None,
        station_name: Optional[str] = None,
        include_retired_stations: bool = False,
        include_test_stations: bool = False,
        debug: bool = False,
        json_format: str = "full",
        xml_format: str = "full",
        format_pretty_print: bool = True,
    ) -> Any:
        params = {
            "debug": str(debug).lower(),
            "format": "json",
            "formatPrettyPrint": str(format_pretty_print).lower(),
            "includeRetiredStations": str(include_retired_stations).lower(),
            "includeTestStations": str(include_test_stations).lower(),
            "jsonFormat": json_format,
            "xmlFormat": xml_format,
        }
        if station_num_ids:
            params["stationNumId"] = ",".join(str(x) for x in station_num_ids)
        if station_name:
            params["stationName"] = station_name

        return self.session.get("stations", params=params)
