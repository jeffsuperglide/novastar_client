#!/usr/bin/env python
"""Manually test script: call the Time Series endpoint with jsonFormat=bare
and print the basic information"""

from dataclasses import asdict
import os
from typing import Dict, List

from novastar_client import NovaStarClient, NovaStarConfig
from novastar_client.models.timeseries import TimeSeries, TimeSeriesPoint
from novastar_client.models.timeseries_response import TimeSeriesResponse


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

    resp: TimeSeriesResponse = client.timeseries.get(
        tsid="54-5400.NovaStar5.WaterLevelRiver-Mean.1Hour",
        periodStart="2026-04-27T13:00:00-05:00",
        periodEnd="2026-04-28T13:00:00-05:00"
    )

    # TimeSeries
    ts: TimeSeries = resp.timeseries
    print(type(ts))

    # TimeSeries Data: a list of TimeSeriesPoint
    ts_data: List = ts.data
    print(type(ts_data), len(ts_data))

    ts_data_point: TimeSeriesPoint = ts.data[0]
    print(type(ts_data_point))

    ts_point_asdict: Dict = asdict(ts_data_point)
    print(ts_point_asdict)


if __name__ in ("__main__", "main"):
    main()
