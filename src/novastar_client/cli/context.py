"""Context setting for subcommands"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AppContext:
    """NovaStar command line interface context dataclass"""

    api_url: str
    api_version: str
    api_root: str
    verify_ssl: bool
    timeout: int = 30
    verbose: int = 0
    quiet: int = 0
