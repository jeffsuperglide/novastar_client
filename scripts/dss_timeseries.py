"""Read time series data from the NovaStar API and load the data into DSS"""

# imports

import pandas as pd

from hecdss.hecdss import HecDss, RegularTimeSeries
from novastar_client import NovaStarClient
from novastar_client.transform.dss_data_type import ns5_type_to_dss
from novastar_client.transform.dss_time_interval import DssTimeInterval
from novastar_client.transform.shef_lookup import ShefCodeInfo, get_shef_info

# establish a client and query the NovaStar API
client = NovaStarClient()
# periodStart="2026-04-27T13:00:00-05:00",
# periodEnd="2026-04-28T13:00:00-05:00",
resp = client.timeseries.get(
    tsid="54-5400.NovaStar5.WaterLevelRiver-Mean.1Hour",
    periodStart="now_minus_1Day",
    periodEnd="now",
)

# get the station information to populate the path and units
timeseries = resp.timeseries
props = resp.get_properties()

time_interval = timeseries.data_interval
time_interval_match = DssTimeInterval.validate_time_string(time_interval)

data_type, stat_type = timeseries.data_type.split("-")
shef_code = props.point_type_shef_parameter_code
shef_code_ns5 = (
    client.datatypes.get(name=data_type)
    .filter_shef_only()
    .datatypes[0]
    .shef_physical_element
)

shef_code_resolved = shef_code if shef_code else shef_code_ns5

# use the shef code to get its info
shef_info = get_shef_info(shef_code_resolved) if shef_code_resolved else ShefCodeInfo()

# DSS Data Type e.g., INST-VAL
stat_type_ns5 = ns5_type_to_dss(stat_type)

# check the units
if timeseries.units == "pies":
    timeseries.units = "ft"

PATH: str = (
    f"/{timeseries.loc_id}/{props.station_name}/{shef_info.parameter}//{time_interval_match}/{timeseries.data_type}/"
)
print(PATH)

# OR get the dt and value in a list of Dict
dt_value = resp.get_data_fields("dt", "value")

# load the DataFrame
df = pd.DataFrame(dt_value)
# convert dt to datetime
df["dt"] = pd.to_datetime(df["dt"])
# convert datetime to UTC
df["dt"] = df["dt"].dt.tz_convert("UTC")


# open the dss file, make a regular time series and put the data
dss: HecDss = HecDss("timeseries.dss")
tsc = RegularTimeSeries()
tsc.id = PATH
tsc.values = df["value"].to_list()  # type: ignore
tsc.times = df["dt"].to_list()
tsc.units = "ft"
tsc.data_type = stat_type_ns5

dss.put(tsc)
dss.close()
