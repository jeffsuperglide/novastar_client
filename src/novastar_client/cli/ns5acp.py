"""NovaStar Client command line interface"""

from __future__ import annotations

import click

from novastar_client import __version__

from .commands.stations import stations
from .commands.ts import ts

from .commands.tscatalog import tscatalog
from .context import AppContext
from .logging import configure_cli_logging, logging_options
from .settings import CONTEXT_SETTINGS


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(__version__)
@click.option(
    "--api-url",
    default="https://panama-cloud-ns5.trilynx-novastar.systems",
    show_default=True,
)
@click.option(
    "--api-version",
    default="v1",
    show_default=True,
)
@click.option(
    "--api-root",
    default="/novastar/data/api",
    show_default=True,
)
@click.option(
    "--verify-ssl",
    default=True,
    show_default=True,
)
@click.option(
    "--api-timeout",
    default=30,
    show_default=True,
)
@logging_options
@click.pass_context
def cli(
    ctx: click.Context,
    api_url: str,
    api_version: str,
    api_root: str,
    verify_ssl: bool,
    api_timeout: int,
    verbose: int,
    quiet: int,
) -> None:
    """cli interface for the novastar_client

    Parameters
    ----------
    verbose : int, optional
        Verbose count, by default 0
    quiet : int, optional
        Quiet count, by default 0
    """
    configure_cli_logging(verbose=verbose, quiet=quiet)

    ctx.obj = AppContext(
        api_url=api_url,
        api_version=api_version,
        api_root=api_root,
        verify_ssl=verify_ssl,
        timeout=api_timeout,
        verbose=verbose,
        quiet=quiet,
    )


cli.add_command(ts)
cli.add_command(stations)
cli.add_command(tscatalog)
