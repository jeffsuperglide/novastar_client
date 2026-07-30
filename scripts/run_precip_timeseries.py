#!/usr/bin/env python
"""Manually test script: call the Time Series endpoint with jsonFormat=bare
and print the basic information"""

from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt

import pandas as pd
from dataclasses import asdict
import os
from typing import Dict, List

from novastar_client import NovaStarClient, NovaStarConfig
from novastar_client.models.timeseries import TimeSeries, TimeSeriesPoint
from novastar_client.models.timeseries_response import TimeSeriesResponse
from novastar_client.transform import timeseries


def main():
    base_url = os.getenv(
        "NOVASTAR_BASE_URL", "https://panama-cloud-ns5.trilynx-novastar.systems"
    )

    api_version = os.getenv("NOVASTAR_API_VERSION", "v1")

    # auth_token = os.getenv(
    #     "NOVASTAR_AUTH_TOKEN"
    # )  # not needed but here for example if needed

    config = NovaStarConfig(base_url=base_url, api_version=api_version, timeout=60)

    client = NovaStarClient(config=config)

    # resp: TimeSeriesResponse = client.timeseries.get(
    #     tsid="71.NovaStar5.PrecipAccum.IrregSecond",
    #     periodStart="now_minus_2Days",
    #     periodEnd="now",
    # )  # type: ignore

    # TimeSeriesResponse properties
    # start_time = datetime.fromisoformat(resp.response_info.period_start)  # type: ignore
    # end_time = datetime.fromisoformat(resp.response_info.period_end)  # type: ignore
    # print(start_time, " | ", end_time)

    # TimeSeries
    # ts: TimeSeries = resp.timeseries
    # print(type(ts))

    # TimeSeries Data: a list of TimeSeriesPoint
    # ts_data: List = ts.data
    # print(type(ts_data), len(ts_data))

    # time series to panda dataframe
    ts_data = {
        "dt": [
            "2026-07-15T01:34:59-05:00",
            "2026-07-15T07:31:10-05:00",
            "2026-07-15T13:34:59-05:00",
            "2026-07-16T01:34:59-05:00",
            "2026-07-16T05:06:25-05:00",
            "2026-07-16T07:26:55-05:00",
            "2026-07-16T13:34:59-05:00",
            "2026-07-16T15:19:13-05:00",
            "2026-07-16T17:19:13-05:00",
            "2026-07-17T01:19:13-05:00",
            "2026-07-17T10:19:13-05:00",
            "2026-07-18T03:19:13-05:00",
            "2026-07-18T12:19:13-05:00",
        ],
        "flag": ["10092V"] * 13,
        "duration": [-1] * 13,
        "status": [1] * 13,
        "value": [750, 751, 751, 751, 752, 753, 753, 754, 0, 1, 2, 3, 8],
    }

    df = pd.DataFrame(ts_data)

    df["dt"] = pd.to_datetime(df["dt"])

    df = df.set_index("dt").sort_index()

    idx_1min = pd.date_range(
        start=df.index.min().floor("min"), end=df.index.max().ceil("min"), freq="1min"
    )

    # df_1min = df.resample("1min").ffill()
    df_1min = df.reindex(idx_1min).bfill()

    print(df)

    for idx, row in df_1min[:20].iterrows():
        print(idx, row["value"])

    # add the difference in the irregular values
    # df["dt"] = pd.to_datetime(df["dt"])
    # df["diff_value"] = df["value"].diff().fillna(0)

    # diff_df = df[["dt", "diff_value"]].sort_values("dt")

    # get first time and snap to freq
    # first_dt = df["dt"].iloc[0]
    # first_dt_freq = first_dt.round("15min")

    # last_dt = df["dt"].iloc[-1]
    # last_dt_freq = last_dt.round("15min")

    # start = first_dt_freq
    # end = last_dt_freq

    # dt_grid = pd.date_range(start=start, end=end, freq="15min")

    # grid_df = pd.DataFrame({"dt": dt_grid})
    # grid_df = grid_df.sort_values("dt")

    # out_df = pd.merge_asof(grid_df, diff_df, on="dt", direction="backward")
    # out_df = out_df.fillna(diff_df["diff_value"].iloc[0])
    # out_df = out_df.set_index("dt")

    # print(diff_df)

    # for idx, row in out_df.iterrows():
    # print(idx, row["diff_value"])

    # ax = out_df['diff_value'].plot(kind='line')  # or out.plot(y='value')
    # ax.set_ylabel('value')
    # ax.set_xlabel('datetime')
    # plt.tight_layout()
    # plt.show()

    # elapsed in minutes
    # t0 = df["dt"].iloc[0]
    # print(t0)
    # df["elapsed_min"] = (df["dt"] - t0).dt.total_seconds() / 60

    # t_end = df['elapsed_min'].iloc[-1]
    # grid = np.arange(0, t_end + 15, 15)  # every 15 minutes
    # grid_df = pd.DataFrame({'elapsed_min': grid})
    # print(grid_df)

    # print(df)
    # print(df_15min)

    # print(df)
    # for idx, row in df.iterrows():
    #     print(idx, row["dt"], row["value"])

    # irregular to regular
    # reg = timeseries.irregular_to_regular(
    #     df,
    #     start_time=start_time,  # type: ignore
    #     end_time=end_time,  # type: ignore
    #     freq="15min",
    #     fill_method="constant",
    #     value_cols=["value"],
    # )

    # for idx, row in reg.iterrows():
    #     print(idx, row["value"])

    # ts_point_asdict: Dict = asdict(ts_data_point)
    # print(ts_point_asdict)


if __name__ in ("__main__", "main"):
    main()
