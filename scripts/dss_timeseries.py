"""Read time series data from the NovaStar API and load the data into DSS"""

# imports

import pandas as pd

import logging
from hecdss.hecdss import HecDss, RegularTimeSeries
from novastar_client.config import NovaStarConfig
from novastar_client.client import NovaStarClient
from novastar_client.logging_utils import configure_package_logging
from novastar_client.transform.dss_data_type import ns5_type_to_dss
from novastar_client.transform.dss_time_interval import DssTimeInterval
from novastar_client.transform.shef_lookup import get_shef_info

configure_package_logging(NovaStarConfig())
logger = logging.getLogger(__name__)

# establish a client and query the NovaStar API
client = NovaStarClient()


def main():
    # open the dss file, make a regular time series and put the data
    dss: HecDss = HecDss("timeseries.dss")

    catalog = client.tscatalog.get(stationNumId="2")

    if catalog is None:
        return None

    tsids = catalog.get_tsids()

    for tsid in tsids:
        logger.info("tscatalog returned TSID: %s", tsid)

        resp = client.timeseries.get(
            tsid=tsid,
            periodStart="now_minus_1Day",
            periodEnd="now",
        )

        if resp is None:
            logger.exception("timeseries response returned None: %s", tsid)
            continue

        # get the station information to populate the path and units
        timeseries = resp.timeseries
        props = resp.get_properties()

        time_interval = timeseries.data_interval
        time_interval_match = (
            "1Second"
            if time_interval.endswith("IrregSecond")
            else DssTimeInterval.validate_time_string(time_interval)
        )

        data_type_parts = timeseries.data_type.split("-")
        shef_code = props.point_type_shef_parameter_code

        shef_info = get_shef_info(shef_code)
        shef_info_parameter = shef_info.parameter

        # if shef_info.parameter is empty get it from the NovaStar name
        if shef_info_parameter == "":
            datatype = client.datatypes.get(name=data_type_parts[0])

            # filter on SHEF
            if datatype is not None:
                shef_code = datatype.datatypes[0].shef_physical_element
                shef_info = get_shef_info(shef_code)
                shef_info_parameter = shef_info.parameter

        # DSS Data Type e.g., INST-VAL
        stat_type_ns5 = ns5_type_to_dss(data_type_parts[-1])

        # check the units
        if timeseries.units == "pies":
            timeseries.units = "ft"

        path: str = (
            f"/{timeseries.loc_id}/{props.station_name}/{shef_info_parameter}//{time_interval_match}/{timeseries.data_type}/"
        )
        logger.info("DSS Pathname for tsid '%s': %s", tsid, path)

        if len(shef_info_parameter) > 0:
            # OR get the dt and value in a list of Dict
            dt_value = resp.get_data_fields("dt", "value")

            if len(dt_value) > 0:
                # load the DataFrame
                df = pd.DataFrame(dt_value)
                # convert dt to datetime
                df["dt"] = pd.to_datetime(df["dt"])
                # convert datetime to UTC
                df["dt"] = df["dt"].dt.tz_convert("UTC")

                tsc = RegularTimeSeries()
                tsc.id = path
                tsc.values = df["value"].to_list()  # type: ignore
                tsc.times = df["dt"].to_list()
                tsc.units = timeseries.units  # type: ignore
                tsc.data_type = stat_type_ns5

                dss.put(tsc)
    dss.close()


if __name__ == "__main__":
    main()
