# src/novastar_client/models/station.py
from dataclasses import dataclass
from typing import Optional


@dataclass
class Station:
    id: int
    num_id: int
    name: str

    description: Optional[str] = None
    description_text: Optional[str] = None
    dashboard_url: Optional[str] = None

    elevation: Optional[float] = None
    last_time_polled: Optional[str] = None

    latitude: Optional[float] = None
    longitude: Optional[float] = None

    out_of_service: Optional[bool] = None
    remote_tag: Optional[str] = None
    retired_station: Optional[bool] = None
    tag_name: Optional[str] = None
    test_station: Optional[bool] = None

    type_id: Optional[int] = None
    station_type_name: Optional[str] = None
    station_type_protocol: Optional[str] = None

    @classmethod
    def from_api(cls, data: dict) -> "Station":
        return cls(
            id=data["id"],
            num_id=data["numId"],
            name=data["name"],
            description=data.get("description"),
            description_text=data.get("descriptionText"),
            dashboard_url=data.get("dashboardUrl"),
            elevation=data.get("elevation"),
            last_time_polled=data.get("lastTimePolled"),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            out_of_service=data.get("outOfService"),
            remote_tag=data.get("remoteTag"),
            retired_station=data.get("retiredStation"),
            tag_name=data.get("tagName"),
            test_station=data.get("testStation"),
            type_id=data.get("typeId"),
            station_type_name=data.get("stationTypeName"),
            station_type_protocol=data.get("stationTypeProtocol"),
        )
