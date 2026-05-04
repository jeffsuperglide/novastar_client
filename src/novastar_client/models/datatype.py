"""DataType dataclass"""

from dataclasses import dataclass


@dataclass
class DataType:
    """DataType dataclass representing the NovaStar DataType"""

    name: str
    is_valid: bool
    include_in_operator_station_summary: bool
    display_name: str = ""
    description: str = ""
    data_type_source_type: str = ""
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
            name=data["name"],
            display_name=data["displayName"],
            description=data["description"],
            data_type_source_type=data["dataTypeSourceType"],
            include_in_operator_station_summary=data["includeInOperatorStationSummary"],
            is_valid=data["isValid"],
            is_valid_error=data["isValidError"],
            shef_physical_element=data["shefPhysicalElement"],
        )
