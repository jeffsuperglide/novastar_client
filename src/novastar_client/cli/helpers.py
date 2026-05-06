"""Helper module with shared methods"""

import json

import click


def output_pretty_json(data, indent: int = 4, sort_keys: bool = True) -> None:
    """output_pretty_json helper method pretty printing json output.

    Parameters
    ----------
    data : Any
        Input data.
    indent : int, optional
        Indention, by default 4
    sort_keys: bool, optional
        Sort the keys, by default True
    """
    json_str = json.dumps(
        data,
        indent=indent,
        sort_keys=sort_keys,
    )

    click.echo(json_str)
