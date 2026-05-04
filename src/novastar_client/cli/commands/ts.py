"""NovaStar Client command line interface subcommand, ts"""

from __future__ import annotations

import logging
import pprint

import click

from ...client import NovaStarClient
from ...config import NovaStarConfig
from ..context import AppContext
from ..settings import CONTEXT_SETTINGS

logger = logging.getLogger(__name__)

pass_app = click.make_pass_decorator(AppContext)

pp = pprint.PrettyPrinter(indent=4, width=80, compact=False)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option(
    "--tsid",
    type=str,
    help="Time series identifier, for example: 100.NovaStar5.WaterLevelRiver.IrregSecond.",
)
@click.option(
    "--period-start",
    type=str,
    help="Period start date/time using format YYYY-MM-DDThh:mm:ss or "
    "YYYY-MM-DDThh:mm:ss-06:00 with time zone offset (default is 31 days prior to current time).",
)
@click.option(
    "--period-end",
    type=str,
    help="Period end date/time using format YYYY-MM-DDThh:mm:ss or "
    "YYYY-MM-DDThh:mm:ss-06:00 (default is the current time).",
)
@click.option("--pretty-print", is_flag=True, help="Pretty print the json response.")
@click.option("--stream", is_flag=True, help="Stream the json response per line.")
@pass_app
def ts(
    app: AppContext,
    tsid: str,
    period_start: str,
    period_end: str,
    pretty_print: bool,
    stream: bool,
) -> None:
    """Subcommand returning a list of timeseries data."""

    config = NovaStarConfig(base_url=app.api_url, api_version=app.api_version)
    client = NovaStarClient(config=config)

    if (period_start is None) != (period_end is None):
        raise click.UsageError(
            "--period-start and --period-end must be provided together"
        )

    args = {
        "raw": False,
        "tsid": tsid,
    }
    if period_start is not None:
        args["periodStart"] = period_start
    if period_end is not None:
        args["periodEnd"] = period_end

    resp = client.timeseries.get(**args)

    if resp is None:
        logger.warning("Timeseries command line interface returned %s", resp)
        return None

    dt_values = resp.get_data_fields("dt", "value")

    if stream:
        for item in dt_values:
            click.echo(item)
    elif pretty_print:
        click.echo(pp.pformat(dt_values))
    else:
        click.echo(dt_values)
