"""CLI logging"""

from __future__ import annotations

import logging
from typing import Callable, TypeVar

import click

F = TypeVar("F", bound=Callable[..., object])


def logging_options(func: F) -> F:
    """logging_options method defining logging options.

    Parameters
    ----------
    func : F
        Generic type variable that represents some callable type.

    Returns
    -------
    F
        A function of some signature returned.
    """
    func = click.option(
        "-q",
        "--quiet",
        count=True,
        help="Reduce logging output; repeat for less output.",
    )(func)
    func = click.option(
        "-v",
        "--verbose",
        count=True,
        help="Increase logging output; repeat for more detail.",
    )(func)
    return func


def _resolve_log_level(verbose: int, quiet: int) -> int:
    delta = verbose - quiet

    if delta <= -1:
        return logging.ERROR
    if delta == 0:
        return logging.WARNING
    if delta == 1:
        return logging.INFO
    return logging.DEBUG


def configure_cli_logging(verbose: int, quiet: int) -> None:
    """configure_cli_logging logging configuration method.

    The default logging level is logging.WARNING only showing warning
    and errors.  There is a delta determined between the verbose count (int)
    and the quiet count (int) that determines the logging level.  Adding
    a verbose flag raises the count therefore raising the

    Parameters
    ----------
    verbose : int
        Setting the level of verbosity.
    quiet : int
        Setting the level of who quiet the logging should be.
    """

    level = _resolve_log_level(verbose, quiet)

    root = logging.getLogger()
    root.handlers.clear()

    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
    )

    root.setLevel(level)
    root.addHandler(handler)
