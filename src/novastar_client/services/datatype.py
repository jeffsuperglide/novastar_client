"""Stations Service API"""

import logging
import dataclasses
from typing import Any, ClassVar, Dict

from novastar_client.models import DataTypeResponse
from novastar_client.session import NovaStarSession

logger = logging.getLogger(__name__)


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
        """validate_sort checks the dataType sorting options.

        Parameters
        ----------
        sort_value : str | None
            The value to sort by.

        Returns
        -------
        str
            The provided sort value or the default sort value.
        """
        sort_value = sort_value or cls.DEFAULT_SORT
        if sort_value not in cls.ALLOWED_SORTS:
            sort_value = cls.DEFAULT_SORT
            logger.warning(
                "Invalid sort '%s'. Allowed values are: %s",
                sort_value,
                sorted(cls.ALLOWED_SORTS),
            )
            logger.warning("Default sort value will be used: %s", cls.DEFAULT_SORT)

        return sort_value

    def get(self, **kwargs) -> DataTypeResponse | None:
        """NovaStarSession GET method providing DataTypeResponse

        Returns
        -------
        DataTypeResponse
            DataTypeResponse dataclass defined in the models module.
        """

        params: Dict[str, Any] = {**self.default_params, **kwargs}
        data: Any = self.session.get(self.path, params=params)

        if data is None:
            return None

        return DataTypeResponse.from_api(data)
