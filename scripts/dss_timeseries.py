"""Read time series data from the NovaStar API and load the data into DSS"""

# imports
from datetime import datetime
from typing import Any, Dict, List

import pandas as pd

from hecdss.hecdss import HecDss, RegularTimeSeries
from novastar_client import NovaStarClient

# from novastar_client.models.timeseries import TimeSeries, TimeSeriesPoint
from novastar_client.models.timeseries_response import TimeSeriesResponse

# establish a client and query the NovaStar API
client = NovaStarClient()
# periodStart="2026-04-27T13:00:00-05:00",
# periodEnd="2026-04-28T13:00:00-05:00",
resp: TimeSeriesResponse = client.timeseries.get(
    tsid="54-5400.NovaStar5.WaterLevelRiver-Mean.1Hour",
    periodStart="now_minus_1Day",
    periodEnd="now",
)

# get the station information to populate the path and units
props = resp.get_properties()

timeseries = resp.timeseries

PATH: str = (
    f"/{timeseries.loc_id}/{props.station_name}/Stage//{timeseries.data_interval}/{timeseries.data_type}/"
)
print(PATH)

# get the dt as a list, get the values as a list, and load in a numpy df
# dates = resp.get_data_field("dt")
# values = resp.get_data_field("value")

# OR get the dt and value in a list of Dict
dt_value = resp.get_data_fields("dt", "value")

# load the DataFrame
df = pd.DataFrame(dt_value)
# convert dt to datetime
df["dt"] = pd.to_datetime(df["dt"])
# convert datetime to UTC
df["dt"] = df["dt"].dt.tz_convert("UTC")

# print(df["dt"].to_list())
# print(df["value"].to_list())

# open the dss file, make a regular time series and put the data
dss: HecDss = HecDss("timeseries.dss")
tsc = RegularTimeSeries()
tsc.id = PATH
tsc.values = df["value"].to_list()  # type: ignore
tsc.times = df["dt"].to_list()
tsc.units = "ft"
tsc.data_type = "INST-VAL"

dss.put(tsc)
dss.close()
