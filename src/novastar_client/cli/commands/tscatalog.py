# src/project/bin/commands/sync.py
from __future__ import annotations

import logging

import click

from novastar_client.cli.settings import CONTEXT_SETTINGS
from novastar_client.cli.context import AppContext


logger = logging.getLogger(__name__)

pass_app = click.make_pass_decorator(AppContext)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option(
    "--full",
    is_flag=True,
    help="Run a full sync instead of an incremental sync.",
)
@click.option(
    "--profile",
    default="default",
    show_default=True,
    help="Execution profile to use.",
)
@pass_app
def tscatalog(app: AppContext, full: bool, profile: str) -> None:
    logger.info("Starting sync")
    logger.debug("sync arguments full=%s profile=%s", full, profile)
    click.echo(f"sync full={full} profile={profile}")
