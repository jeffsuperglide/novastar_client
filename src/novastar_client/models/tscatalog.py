"""TsCatalogItem dataclass"""

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class TsCatalogItem:
    """TsCatalogItem dataclass representing the NovaStar TimeSeriesCatalog"""

    loc_id: str
    data_type: str
    statistic_type: Optional[str]
    data_interval: str
    is_instantaneous: bool
    data_units: Optional[str]
    time_series_value_source_type: str
    time_series_value_source_is_equation: bool
    time_series_value_source_is_forecast: bool

    station_num_id: int
    station_name: str
    station_description: Optional[str]
    station_elevation: int
    station_id: int
    station_latitude: float
    station_longitude: float
    station_out_of_service: bool
    station_remote_tag: Optional[str]
    station_tag_name: Optional[str]
    station_type_description: Optional[str]
    station_type_name: Optional[str]
    station_type_protocol: Optional[str]

    point_id: int
    point_num_id: int
    point_name: str
    point_description: Optional[str]
    point_out_of_service: bool
    point_rated: bool
    point_tag_name: Optional[str]
    point_type_name: Optional[str]
    point_type_description: Optional[str]
    point_type_shef_parameter_code: Optional[str]
    point_type_short_name: Optional[str]
    point_type_units_abbreviated: Optional[str]
    point_class_description: Optional[str]
    point_class_name: Optional[str]

    rating_assign_shef_parameter_code: Optional[str]
    rating_table_out_units_abbrev: Optional[str]
    shef_parameter_code: Optional[str]
    shef_physical_element: Optional[str]
    shef_duration: Optional[str]
    shef_type: Optional[str]
    shef_source: Optional[str]
    shef_extremum: Optional[str]
    shef_probability: Optional[str]

    is_valid: bool
    problems: Optional[str]
    time_series_identifier: str

    @classmethod
    def from_api(cls, data: Dict[str, Any]) -> "TsCatalogItem":
        """from_api classmethod parsing json to this dataclass

        Parameters
        ----------
        data : Dict[str, Any]
            NovaStar json payload described by Time Series Catalog
            (tscatalog) (see NovaStar API Schemas).

        Returns
        -------
        TsCatalogItem
            dataclass for the NovaStar returned payload describing the TimeSeriesCatalog.
        """
        return cls(
            loc_id=data["locId"],
            data_type=data["dataType"],
            statistic_type=data.get("statisticType"),
            data_interval=data["dataInterval"],
            is_instantaneous=data["isInstantaneous"],
            data_units=data.get("dataUnits"),
            time_series_value_source_type=data["timeSeriesValueSourceType"],
            time_series_value_source_is_equation=data[
                "timeSeriesValueSourceIsEquation"
            ],
            time_series_value_source_is_forecast=data[
                "timeSeriesValueSourceIsForecast"
            ],
            station_num_id=data["stationNumId"],
            station_name=data["stationName"],
            station_description=data.get("stationDescription"),
            station_elevation=data["stationElevation"],
            station_id=data["stationId"],
            station_latitude=data["stationLatitude"],
            station_longitude=data["stationLongitude"],
            station_out_of_service=data["stationOutOfService"],
            station_remote_tag=data.get("stationRemoteTag"),
            station_tag_name=data.get("stationTagName"),
            station_type_description=data.get("stationTypeDescription"),
            station_type_name=data.get("stationTypeName"),
            station_type_protocol=data.get("stationTypeProtocol"),
            point_id=data["pointId"],
            point_num_id=data["pointNumId"],
            point_name=data["pointName"],
            point_description=data.get("pointDescription"),
            point_out_of_service=data["pointOutOfService"],
            point_rated=data["pointRated"],
            point_tag_name=data.get("pointTagName"),
            point_type_name=data.get("pointTypeName"),
            point_type_description=data.get("pointTypeDescription"),
            point_type_shef_parameter_code=data.get("pointTypeShefParameterCode"),
            point_type_short_name=data.get("pointTypeShortName"),
            point_type_units_abbreviated=data.get("pointTypeUnitsAbbreviated"),
            point_class_description=data.get("pointClassDescription"),
            point_class_name=data.get("pointClassName"),
            rating_assign_shef_parameter_code=data.get("ratingAssignShefParameterCode"),
            rating_table_out_units_abbrev=data.get("ratingTableOutUnitsAbbrev"),
            shef_parameter_code=data.get("shefParameterCode"),
            shef_physical_element=data.get("shefPhysicalElement"),
            shef_duration=data.get("shefDuration"),
            shef_type=data.get("shefType"),
            shef_source=data.get("shefSource"),
            shef_extremum=data.get("shefExtremum"),
            shef_probability=data.get("shefProbability"),
            is_valid=data["isValid"],
            problems=data.get("problems"),
            time_series_identifier=data["timeSeriesIdentifier"],
        )
