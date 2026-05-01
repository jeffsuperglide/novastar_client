"""DataType dataclass"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class DataType:
    """DataType dataclass representing the NovaStar DataType"""

    name: str
    is_valid: bool
    include_in_operator_station_summary: bool
    display_name: Optional[str] = None
    description: Optional[str] = None
    data_type_source_type: Optional[str] = None
    is_valid_error: Optional[str] = None
    shef_physical_element: Optional[str] = None

    @classmethod
    def from_api(cls, data: dict) -> "DataType":
        """from_api classmethod parsing json to this dataclass

        Parameters
        ----------
        data : dict
            NovaStar json payload described by DataType (see NovaStar API Schemas).

        Returns
        -------
        DataType
            dataclass for the NovaStar returned payload describing the API DataType section.
        """

        return cls(
            name=data["name"],
            display_name=data["displayName"],
            description=data["description"],
            data_type_source_type=data["dataTypeSourceType"],
            include_in_operator_station_summary=data["includeInOperatorStationSummary"],
            is_valid=data["isValid"],
            is_valid_error=data.get("isValidError"),
            shef_physical_element=data["shefPhysicalElement"],
        )
