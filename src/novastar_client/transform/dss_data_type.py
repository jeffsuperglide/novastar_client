"""Transform module lookup for DSS data types"""

from enum import Enum
from typing import Final


class DssDataType(str, Enum):
    """DSS data type enumerations"""
    PER_AVER = "PER-AVER"
    PER_CUM = "PER-CUM"
    INST_VAL = "INST-VAL"
    INST_CUM = "INST-CUM"
    FREQ = "FREQ"
    PER_MAX = "PER-MAX"
    PER_MIN = "PER-MIN"
    CONST = "CONST"


class NovaStarStatisticType(str, Enum):
    """NovaStar statistic type enumerations"""
    MEAN = "Mean"
    MAX = "Max"
    MIN = "Min"
    COUNT = "Count"
    LAST = "Last"
    NEAR = "Near"
    TOTAL = "Total"
    TIME_WEIGHTED_MEAN = "TimeWeightedMean"


NOVASTAR_TO_DSS_TYPE: Final[dict[NovaStarStatisticType, DssDataType]] = {
    NovaStarStatisticType.MEAN: DssDataType.PER_AVER,
    NovaStarStatisticType.TIME_WEIGHTED_MEAN: DssDataType.PER_AVER,
    NovaStarStatisticType.MAX: DssDataType.PER_MAX,
    NovaStarStatisticType.MIN: DssDataType.PER_MIN,
    NovaStarStatisticType.COUNT: DssDataType.FREQ,
    NovaStarStatisticType.TOTAL: DssDataType.PER_CUM,
    NovaStarStatisticType.LAST: DssDataType.INST_VAL,
    NovaStarStatisticType.NEAR: DssDataType.INST_VAL,
}


def ns5_type_to_dss(api_type: str) -> DssDataType:
    """ns5_type_to_dss translates NovaStar statistic types to DSS data types

    Parameters
    ----------
    api_type : str
        The NovaStar statistic type input.

    Returns
    -------
    DssDataType
        The DSS data type returned.
    """
    if not api_type:
        return DssDataType.INST_VAL

    try:
        api_enum = NovaStarStatisticType(api_type)
    except ValueError:
        return DssDataType.INST_VAL

    return NOVASTAR_TO_DSS_TYPE.get(api_enum, DssDataType.INST_VAL)
