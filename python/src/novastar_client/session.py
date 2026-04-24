"""
NovaStarSession Class
"""

from __future__ import annotations

from typing import Any, Dict, Optional

import requests
from novastar_client.config import NovaStarConfig
from novastar_client.exceptions import NovaStarAPIError


class NovaStarSession:
    """NovaStar Session defines API root path and get() method"""

    def __init__(
        self,
        config: NovaStarConfig,
        auth_token: Optional[str] = None,
    ):
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
        """api_root path creation

        Returns
        -------
        str
            api root path
        """
        return (
            f"{self.config.base_url.rstrip('/')}/"
            f"{self.config.api_root.strip("/")}/"
            f"{self.config.api_version.strip("/")}"
        )

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """get API call to NovaStar

        Parameters
        ----------
        path : str
            endpoint path
        params : Optional[Dict[str, Any]], optional
            API call query parameters, by default None

        Returns
        -------
        Any
            json

        Raises
        ------
        NovaStarAPIError
            NovaStar Error
        """
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
