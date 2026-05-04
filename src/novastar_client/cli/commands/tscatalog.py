"""NovaStar Client command line interface subcommand, tscatalog"""

from __future__ import annotations

import logging
from typing import Tuple

import click

import pprint

from novastar_client.cli.settings import CONTEXT_SETTINGS
from novastar_client.cli.context import AppContext
from novastar_client.client import NovaStarClient
from novastar_client.config import NovaStarConfig

logger = logging.getLogger(__name__)

pass_app = click.make_pass_decorator(AppContext)


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
)
@click.option(
    "--pretty-print",
    is_flag=True,
)
@pass_app
def tscatalog(
    app: AppContext,
    station_numid: Tuple,
    group_name: bool,
    pretty_print: bool,
) -> None:
    """Subcommand returning a list of station TSIDs.


    Parameters
    ----------
    app : AppContext
        Application context passed to subcommands.
    station_numid : Tuple
        Tuple of station number IDs.
    group_id : bool
        Boolean to determine if output should be grouped by id.

    Returns
    -------
    List
        List of time series IDS.
    """
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

    pp = pprint.PrettyPrinter(indent=4, width=80, compact=False)
    if group_name:
        cat_by_name = resp.get_catalog_by_name()
        if pretty_print:
            click.echo(pp.pformat(cat_by_name))
        else:
            click.echo(cat_by_name)
    else:
        tsids = resp.get_tsids()
        if pretty_print:
            click.echo(pp.pformat((tsids)))
        else:
            click.echo(resp.get_tsids())
