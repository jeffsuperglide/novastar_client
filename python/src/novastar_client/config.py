"""
src/novastar_client/config.py
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class NovaStarConfig:
    base_url: str = "https://panama-cloud-ns5.trilynx-novastar.systems"
    api_version: str = "v1"
    timeout: int = 30
    verify_ssl: bool = True
