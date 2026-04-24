"""Helpers utility"""

from urllib.parse import quote_plus


def with_urlencoded_kwargs(base: dict | None = None, **kwargs) -> dict:
    base = dict(base or {})
    encoded = {k: quote_plus(str(v)) for k, v in kwargs.items()}
    return {**base, **encoded}
