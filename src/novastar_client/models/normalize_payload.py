"""Normalize the payload dealing with {} or []"""

from typing import Any, Dict, List, Tuple


def normalize_payload_with_sequence(
    data: Any,
    sequence_key: str,
) -> Tuple[Dict, List]:
    """normalize_payload_with_sequence Normalize the payload dealing
    with {} or [] (meta_dict, sequence_list)

    Parameters
    ----------
    data : Any
        NovaStar json payload that may return a dictionary or list.
    sequence_key : str
        NovaStar endpoint (e.g., ts, tscatalog, stations)

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
