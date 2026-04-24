"""Normalize the payload dealing with {} or []

Returns
-------
tuple[dict,list]
    returning a tuple with a dictionary and list
"""

from typing import Any


def normalize_payload_with_sequence(
    data: Any,
    sequence_key: str,
) -> tuple[dict, list]:
    """normalize_payload_with_sequence returning (meta_dict, sequence_list)

    Parameters
    ----------
    data : Any
        json payload from NovaStar
    sequence_key : str
        NovaStar endpoint

    Returns
    -------
    tuple[dict, list]
        tuple of dict and list with data or empty
    """
    if isinstance(data, dict):
        return data, data.get(sequence_key, [])
    if isinstance(data, list):
        return {}, data

    return {}, []
