"""Run station IDs to see which TSID has data"""

from pathlib import Path
import logging
from novastar_client.config import NovaStarConfig
from novastar_client.client import NovaStarClient

logger = logging.getLogger(__name__)

output_file = Path("./stations_tsids.out")

intervals_allowed = (
    "Minute",
    "Hour",
    # "Day",
    # "Month",
    # "Year",
)
measure_allowed = (
    "Precip-Total",
    "WaterLevelRiver-Mean",
    "DischargeRiver-Mean",
)

# define the list of IDs
acp_ids = [
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    16,
    17,
    18,
    19,
    20,
    22,
    23,
    24,
    25,
    26,
    29,
    30,
    32,
    33,
    34,
    35,
    36,
    37,
    39,
    40,
    42,
    43,
    44,
    45,
    46,
    47,
    48,
    49,
    50,
    51,
    52,
    53,
    54,
    55,
    56,
    57,
    58,
    59,
    60,
    61,
    62,
    63,
    64,
    65,
    67,
    68,
    69,
    70,
    71,
    72,
    73,
    74,
    75,
    76,
    77,
    78,
    79,
    80,
    81,
    88,
    89,
    90,
    93,
    94,
    95,
    96,
    97,
    98,
    99,
    100,
    101,
    102,
    103,
    106,
    107,
    109,
    110,
    112,
    114,
    117,
    118,
    119,
    120,
    121,
    123,
    124,
    125,
    126,
    127,
    128,
    129,
    130,
    131,
    132,
    133,
    134,
    135,
    136,
    137,
    138,
    139,
    140,
    141,
    142,
    143,
    144,
    145,
    146,
    147,
    201,
    203,
    204,
    205,
    206,
    207,
    208,
    209,
    210,
    211,
    213,
    228,
    229,
    231,
    232,
    233,
    253,
    261,
    262,
    263,
    301,
    302,
    303,
    305,
    306,
    307,
    308,
    309,
    310,
    311,
    312,
    313,
    314,
    315,
    316,
    318,
    320,
    338,
    340,
    341,
    342,
    343,
    344,
    345,
    346,
    347,
    348,
    349,
    350,
    360,
    361,
    362,
    363,
    364,
    365,
    366,
    367,
    368,
    369,
    370,
    460,
    509,
    530,
    540,
    1609,
    3609,
    3809,
    4094,
    5000,
    5300,
    6000,
    8000,
    34090,
    99910,
    99920,
    99921,
    99927,
    99938,
    99941,
    99966,
    99991,
    99992,
]
# define the starting and ending date for the time window
START_PERIOD = "now_minus_1Day"
END_PERIOD = "now"

# setup the client
client = NovaStarClient(NovaStarConfig(log_level="INFO", timeout=60))


def main():
    # get a list of TSIDs from the current station ID
    with output_file.open(mode="w", encoding="utf-8") as fp:

        for acp_id in acp_ids:
            catalog = client.tscatalog.get(stationNumId=str(acp_id))
            if catalog is None:
                logger.info("Station number ID '%s' returned None", acp_id)
                continue

            # get the tsids and filter by allowed intervals
            tsids = catalog.get_tsids()
            tsids_resolved = [
                tsid
                for tsid in tsids
                if any(measure in tsid for measure in measure_allowed)
                and tsid.endswith(intervals_allowed)
            ]

            # loop through the TSIDs seeing if that ID has data
            for ts in tsids_resolved:
                response = client.timeseries.get(
                    tsid=ts,
                    periodStart=START_PERIOD,
                    periodEnd=END_PERIOD,
                )

                if response is not None:
                    # if that return is not empty or null, write that TSID out
                    data_list = response.get_data()
                    if len(data_list) > 0:
                        logger.info(ts)

                        fp.write(f"{ts}\n")
                else:
                    logger.exception("timeseries response returned None: %s", ts)
                    continue


if __name__ == "__main__":
    main()
