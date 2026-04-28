"""NovaStarConfig Class"""

from dataclasses import dataclass


@dataclass(frozen=True)
class NovaStarConfig:
    """NovaStar configuration setup"""

    base_url: str = "https://panama-cloud-ns5.trilynx-novastar.systems"
    api_root: str = "/novastar/data/api"
    api_version: str = "v1"
    timeout: int = 30
    verify_ssl: bool = True
