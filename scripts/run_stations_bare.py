#!/usr/bin/env python
"""Manually test script: call the Stations endpoint with jsonFormat=full
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

    config = NovaStarConfig(base_url=base_url, api_version=api_version)

    client = NovaStarClient(config=config)

    resp = client.stations.get(stationNumId="54")
    # resp = client.stations.get(jsonFormat="bare", name="AAA ESTACION DE PRUEBA")
    print(resp.stations)


if __name__ == "__main__" or __name__ == "main":
    main()
