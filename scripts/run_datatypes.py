#!/usr/bin/env python
"""Manually test script: call the Time Series endpoint with jsonFormat=bare
and print the basic information"""

import os

import pprint

from novastar_client import NovaStarClient, NovaStarConfig
from novastar_client.models.datatype_response import DataTypeResponse


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

    resp: DataTypeResponse = client.datatypes.get(
        sort="-name",
        shefPhysicalElement="H*",
    )

    # length of all datatypes
    print(len(resp.datatypes))

    # length of on SHEF datatypes
    print(len(resp.filter_shef_only().datatypes))

    pp = pprint.PrettyPrinter(indent=4)

    pp.pprint(resp.to_dict())


if __name__ in ("__main__", "main"):
    main()
