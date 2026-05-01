"""NovaStar Client command line interface"""

from __future__ import annotations

import click

from novastar_client.cli.commands.stations import stations
from novastar_client.cli.commands.ts import ts

from novastar_client.cli.commands.tscatalog import tscatalog
from novastar_client.cli.context import AppContext
from novastar_client.cli.logging import configure_logging, logging_options
from novastar_client.cli.settings import CONTEXT_SETTINGS
from novastar_client.config import NovaStarConfig


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option(
    "--api-url",
    default=NovaStarConfig.base_url,
    show_default=True,
)
@click.option(
    "--api-version",
    default=NovaStarConfig.api_version,
    show_default=True,
)
@click.option(
    "--api-root",
    default=NovaStarConfig.api_root,
    show_default=True,
)
@click.option(
    "--verify-ssl",
    default=NovaStarConfig.verify_ssl,
    show_default=True,
)
@click.option(
    "--api-timeout",
    default=NovaStarConfig.timeout,
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
    configure_logging(verbose=verbose, quiet=quiet)

    # resolve the NovaStar package configurations
    api_url_resolved = NovaStarConfig.base_url if api_url is None else api_url
    api_version_resolved = (
        NovaStarConfig.api_version if api_version is None else api_version
    )
    api_root_resolved = NovaStarConfig.api_root if api_root is None else api_root

    ctx.obj = AppContext(
        api_url=api_url_resolved,
        api_version=api_version_resolved,
        api_root=api_root_resolved,
        verify_ssl=verify_ssl,
        timeout=api_timeout,
        verbose=verbose,
        quiet=quiet,
    )


cli.add_command(ts)
cli.add_command(stations)
cli.add_command(tscatalog)
