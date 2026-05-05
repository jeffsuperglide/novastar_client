"""DataType dataclass"""

from dataclasses import dataclass


@dataclass
class DataType:
    """DataType dataclass representing the NovaStar DataType"""

    name: str
    display_name: str = ""
    description: str = ""
    data_type_source_type: str = ""
    include_in_operator_station_summary: bool = False
    is_valid: bool = False
    is_valid_error: str = ""
    shef_physical_element: str = ""

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
            name=data.get("name", ""),
            display_name=data.get("displayName", ""),
            description=data.get("description", ""),
            data_type_source_type=data.get("dataTypeSourceType", ""),
            include_in_operator_station_summary=data.get(
                "includeInOperatorStationSummary", False
            ),
            is_valid=data.get("isValid", False),
            is_valid_error=data.get("isValidError", ""),
            shef_physical_element=data.get("shefPhysicalElement", ""),
        )
