"""Transform lookup module for SHEF codes"""

from __future__ import annotations

import logging

from csv import DictReader
from dataclasses import dataclass
from functools import lru_cache
from importlib.resources import files
from typing import IO, Any, Iterator

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ShefCodeInfo:
    """Shef code info dataclass"""

    parameter: str = ""
    unit: str = ""
    data_type: str = ""
    conversion: Any = ""


def _data_lines(f: IO, skip: int) -> Iterator[str]:
    for _ in range(skip):
        next(f, None)

    # Yield only non-blank lines
    for line in f:
        if line.strip():  # ignore completely blank/whitespace lines
            yield line


@lru_cache(maxsize=1)
def load_shef_map() -> dict[str, ShefCodeInfo]:
    """load_shef_map method loading the shef_parameters data file.

    Returns
    -------
    dict[str, ShefCodeInfo]
        Dictionary of shef code to ShefCodeInfo dataclass relation.
    """
    fieldnames: list[str] = [
        "code",
        "parameter",
        "unit",
        "data_type",
        "conversion",
    ]

    resource = files("novastar_client.data").joinpath("shef_parameters.csv")

    # Data starts on line 14 -> skip=13
    with resource.open(mode="r", encoding="utf-8") as f:
        reader = DictReader(_data_lines(f, skip=13), fieldnames=fieldnames)
        return {
            row["code"]: ShefCodeInfo(
                parameter=row["parameter"].strip(),
                unit=row["unit"].strip(),
                data_type=row["data_type"].strip(),
                conversion=(
                    row["conversion"].strip()
                    if isinstance(row["conversion"], str)
                    else row["conversion"]
                ),
            )
            for row in reader
        }


def get_shef_info(code: str) -> ShefCodeInfo:
    """get_shef_info method using the load_shef_map() method.


    Parameters
    ----------
    code : str
        The shef code to lookup.

    Returns
    -------
    ShefCodeInfo
        The shef code information dataclass.

    Raises
    ------
    KeyError
            Raises error for unknown shef code.
    """
    try:
        return load_shef_map()[code]
    except KeyError:
        logger.warning("Unknown shef code: %s", code)
        return ShefCodeInfo()
