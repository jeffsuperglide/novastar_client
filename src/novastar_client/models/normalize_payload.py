"""Normalize the payload dealing with {} or []

Returns
-------
tuple[dict,list]
    returning a tuple with a dictionary and list
"""

from typing import Any, Tuple, Dict, List


def normalize_payload_with_sequence(
    data: Any,
    sequence_key: str,
) -> Tuple[Dict, List]:
    """normalize_payload_with_sequence returning (meta_dict, sequence_list)

    Parameters
    ----------
    data : Any
        json payload from NovaStar
    sequence_key : str
        NovaStar endpoint

    Returns
    -------
    meta_dict : Dict
        Metadata extracted from the payload.
    sequence_list : List
        Sequence entries extracted from the payload.
    """
    if isinstance(data, Dict):
        return data, data.get(sequence_key, [])
    if isinstance(data, List):
        return {}, data

    return {}, []
