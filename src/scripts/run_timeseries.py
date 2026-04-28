#!/usr/bin/env python
"""Manually test script: call the Time Series endpoint with jsonFormat=bare
and print the basic information"""

import os

from novastar_client import NovaStarClient, NovaStarConfig
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

    resp: TimeSeriesResponse = client.timeseries.get(tsid="54-5400.NovaStar5.WaterLevelRiver-Mean.1Hour")

    # props = resp.get_properties()

    # print(props)

    # get as a dictionary
    # print(resp.get_data("dt"))

    # get the field in a list
    # print(resp.get_field("dt"))

    # get the fields in a list
    # print(resp.get_fields("dt", "value"))

if __name__ == "__main__" or __name__ == "main":
    main()
