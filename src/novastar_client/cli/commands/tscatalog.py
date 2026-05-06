"""NovaStar Client command line interface subcommand, tscatalog"""

from __future__ import annotations

import json
import logging
from typing import Tuple

import click

import pprint

from novastar_client.cli.helpers import output_pretty_json

from ..settings import CONTEXT_SETTINGS
from ..context import AppContext
from ...client import NovaStarClient
from ...config import NovaStarConfig

logger = logging.getLogger(__name__)

pass_app = click.make_pass_decorator(AppContext)

pp = pprint.PrettyPrinter(indent=4, width=80, compact=False)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option(
    "--station-numid",
    multiple=True,
    help="Station numerical ID filter, using public identifiers, single "
    "number or comma-separated list, can be repeated.",
)
@click.option(
    "--group-name",
    is_flag=True,
    help="Group the output by station name returning a list of "
    "each time series catalog description.",
)
@click.option("--pretty-print", is_flag=True, help="Pretty print the json response.")
@pass_app
def tscatalog(
    app: AppContext,
    station_numid: Tuple,
    group_name: bool,
    pretty_print: bool,
) -> None:
    """Subcommand returning a list of station TSIDs."""
    config = NovaStarConfig(
        base_url=app.api_url,
        api_version=app.api_version,
        timeout=app.timeout,
    )
    client = NovaStarClient(config=config)

    station_numbers = (
        ",".join(station_numid) if len(station_numid) > 1 else "".join(station_numid)
    )

    resp = client.tscatalog.get(stationNumId=station_numbers)

    if resp is None:
        logger.warning("Timeseries command line interface returned %s", resp)
        return None

    if group_name:
        cat_by_name = resp.get_catalog_by_name()
        if pretty_print:
            output_pretty_json(cat_by_name)
        else:
            click.echo(json.dumps(cat_by_name))
    else:
        tsids = resp.get_tsids()
        if pretty_print:
            output_pretty_json(tsids)
        else:
            click.echo(json.dumps(tsids))
