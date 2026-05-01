"""Transform module lookup for DSS data types"""

from enum import Enum
from typing import Final


class DssDataType(str, Enum):
    PER_AVER = "PER-AVER"
    PER_CUM = "PER-CUM"
    INST_VAL = "INST-VAL"
    INST_CUM = "INST-CUM"
    FREQ = "FREQ"
    PER_MAX = "PER-MAX"
    PER_MIN = "PER-MIN"
    CONST = "CONST"


class NovaStarDataType(str, Enum):
    MEAN = "Mean"
    MAX = "Max"
    MIN = "Min"
    COUNT = "Count"
    LAST = "Last"
    NEAR = "Near"
    TOTAL = "Total"
    TIME_WEIGHTED_MEAN = "TimeWeightedMean"


NOVASTAR_TO_DSS_TYPE: Final[dict[NovaStarDataType, DssDataType]] = {
    NovaStarDataType.MEAN: DssDataType.PER_AVER,
    NovaStarDataType.TIME_WEIGHTED_MEAN: DssDataType.PER_AVER,
    NovaStarDataType.MAX: DssDataType.PER_MAX,
    NovaStarDataType.MIN: DssDataType.PER_MIN,
    NovaStarDataType.COUNT: DssDataType.FREQ,
    NovaStarDataType.TOTAL: DssDataType.PER_CUM,
    NovaStarDataType.LAST: DssDataType.INST_VAL,
    NovaStarDataType.NEAR: DssDataType.INST_VAL,
}


def ns5_type_to_dss(api_type: str) -> DssDataType:
    if not api_type:
        return DssDataType.INST_VAL

    try:
        api_enum = NovaStarDataType(api_type)
    except ValueError:
        return DssDataType.INST_VAL

    return NOVASTAR_TO_DSS_TYPE.get(api_enum, DssDataType.INST_VAL)
