# src/novastar_client/session.py
from __future__ import annotations
from typing import Any, Dict, Optional
import requests

from .config import NovaStarConfig
from .exceptions import NovaStarAPIError


class NovaStarSession:
    def __init__(self, config: NovaStarConfig, auth_token: Optional[str] = None):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/json",
                "User-Agent": f"novastar-client/{config.api_version}",
            }
        )
        if auth_token:
            self.session.headers["Authorization"] = f"Bearer {auth_token}"

    @property
    def api_root(self) -> str:
        return (
            f"{self.config.base_url.rstrip('/')}"
            f"/novastar/data/api/{self.config.api_version}"
        )

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        url = f"{self.api_root}/{path.lstrip('/')}"
        response = self.session.get(
            url,
            params=params,
            timeout=self.config.timeout,
            verify=self.config.verify_ssl,
        )
        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise NovaStarAPIError(
                f"{response.status_code} error for {url}: {response.text}"
            ) from exc
        return response.json()
