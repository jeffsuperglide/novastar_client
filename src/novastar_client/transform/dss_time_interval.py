"""Transform lookup module for DSS time intervals"""

from difflib import get_close_matches
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DssTimeInterval:
    seconds: int
    name: str

    time_sec = [
        31536000,
        2592000,
        1296000,
        864000,
        604800,
        86400,
        43200,
        28800,
        21600,
        14400,
        10800,
        7200,
        3600,
        1800,
        1200,
        900,
        720,
        600,
        360,
        300,
        240,
        180,
        120,
        60,
        30,
        20,
        15,
        10,
        6,
        5,
        4,
        3,
        2,
        1,
        0,
    ]

    time_string = [
        "1Year",
        "1Month",
        "Semi-Month",
        "Tri-Month",
        "1Week",
        "1Day",
        "12Hour",
        "8Hour",
        "6Hour",
        "4Hour",
        "3Hour",
        "2Hour",
        "1Hour",
        "30Minute",
        "20Minute",
        "15Minute",
        "12Minute",
        "10Minute",
        "6Minute",
        "5Minute",
        "4Minute",
        "3Minute",
        "2Minute",
        "1Minute",
        "30Second",
        "20Second",
        "15Second",
        "10Second",
        "6Second",
        "5Second",
        "4Second",
        "3Second",
        "2Second",
        "1Second",
        "0Second",
    ]

    @classmethod
    def all(cls) -> list["DssTimeInterval"]:
        return [cls(seconds=s, name=n) for s, n in zip(cls.time_sec, cls.time_string)]

    @classmethod
    def from_seconds(cls, seconds: int) -> "DssTimeInterval":
        for s, n in zip(cls.time_sec, cls.time_string):
            if s == seconds:
                return cls(seconds=s, name=n)
        raise ValueError(f"Unknown interval seconds: {seconds}")

    @classmethod
    def from_name(cls, name: str) -> "DssTimeInterval":
        for s, n in zip(cls.time_sec, cls.time_string):
            if n == name:
                return cls(seconds=s, name=n)
        raise ValueError(f"Unknown interval name: {name}")

    @classmethod
    def validate_time_string(cls, input_str: str) -> str | None:
        """
        Validates if input_str is in allowed list or finds closest match.
        Returns the matched string or None if no close match found.
        """
        # Exact match
        if input_str in cls.time_string:
            return input_str

        # Find close matches (cutoff=0.6 means 60% similarity threshold)
        matches = get_close_matches(input_str, cls.time_string, n=1, cutoff=0.6)
        return matches[0] if matches else None
