#!/usr/bin/env python
"""Manually test script: call the Time Series Catalog endpoint with jsonFormat=bare
and print the basic information"""

import os

from novastar_client import NovaStarClient, NovaStarConfig


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

    # resp = client.stations.get(stationNumId="1")
    resp = client.tscatalog.get(jsonFormat="bare", stationNumId="54")
    # resp = client.tscatalog.get(
    #     jsonFormat="bare", dataType="Precip*", stationName="AAA ESTACION DE PRUEBA"
    # )
    # get the TSIDs
    for tsid in resp.get_tsids():
        print(tsid)


if __name__ == "__main__" or __name__ == "main":
    main()
