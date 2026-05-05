"""NovaStar Client command line interface subcommand, stations"""

from __future__ import annotations

import logging
import typing
import pprint

import click

from ..context import AppContext
from ..settings import CONTEXT_SETTINGS
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
    "--pretty-print",
    is_flag=True,
)
@pass_app
def stations(app: AppContext, station_numid: typing.Tuple, pretty_print: bool) -> None:
    """Subcommand returning a list of station metadata."""

    config = NovaStarConfig(base_url=app.api_url, api_version=app.api_version)
    client = NovaStarClient(config=config)

    station_numbers = (
        ",".join(station_numid) if len(station_numid) > 1 else "".join(station_numid)
    )

    resp = client.stations.get(stationNumId=station_numbers)

    if resp is None:
        logger.warning("Stations command line interface returned %s", resp)
        return None

    resp_as_dict = resp.to_dict()  # type: ignore

    if pretty_print:
        click.echo(pp.pformat(resp_as_dict))
    else:
        click.echo(resp_as_dict)
