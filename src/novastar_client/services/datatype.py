"""Stations Service API"""

import dataclasses
from typing import Any, ClassVar, Dict

from novastar_client.exceptions import NovaStarAPIError
from novastar_client.models import DataTypeResponse
from novastar_client.session import NovaStarSession


@dataclasses.dataclass
class DataTypesAPI:
    """DataTypesAPI dataclass"""

    session: "NovaStarSession"

    ALLOWED_SORTS: ClassVar[set[str]] = {
        "name",
        "shefPhysicalElement",
        "-name",
        "-shefPhysicalElement",
    }

    DEFAULT_SORT: ClassVar[str] = "shefPhysicalElement"

    def __post_init__(self):
        self.path = "dataTypes"
        self.default_params: Dict[str, Any] = {
            "debug": str(False).lower(),
            "format": "json",
            "sort": self.DEFAULT_SORT,
        }

    @classmethod
    def validate_sort(cls, sort_value: str | None) -> str:
        sort_value = sort_value or cls.DEFAULT_SORT
        if sort_value not in cls.ALLOWED_SORTS:
            raise NovaStarAPIError(
                f"Invalid sort '{sort_value}'. Allowed values are: {sorted(cls.ALLOWED_SORTS)}"
            ) from Exception()
        return sort_value

    def get(self, **kwargs) -> DataTypeResponse:
        """NovaStarSession GET method providing DataTypeResponse

        Returns
        -------
        DataTypeResponse
            DataTypeResponse dataclass defined in the models module.
        """

        params: Dict[str, Any] = {**self.default_params, **kwargs}
        data: Any = self.session.get(self.path, params=params)

        return DataTypeResponse.from_api(data)
