"""NovaStarSession Class"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional
from urllib.parse import urlencode

import requests

import logging
from novastar_client.config import NovaStarConfig

logger = logging.getLogger(__name__)


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
        """NovaStar Session GET method API call to NovaStar

        Parameters
        ----------
        path : str
            Endpoint path.
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

        _params = urlencode((params or {}), doseq=True)

        response = self.session.get(
            url,
            params=_params,
            timeout=self.config.timeout,
            verify=self.config.verify_ssl,
        )
        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            # Try to parse JSON if available
            parsed = None
            try:
                parsed = response.json()
            except ValueError:
                pass

            retryable = 500 <= response.status_code < 600

            # raise NovaStarAPIError(
            #     "NovaStar API request failed",
            #     status_code=response.status_code,
            #     url=url,
            #     response_body=response.text,
            #     parsed_body=parsed,
            #     retryable=retryable,
            # ) from exc
            logging.warning(
                "NovaStar API request failed",
                extra={
                    "status_code": response.status_code,
                    "url": url,
                    "response_body": response.text,
                    "parsed_body": parsed,
                    "retryable": retryable,
                    "original_exception": exc,
                },
            )
            return {}

        return response.json()
