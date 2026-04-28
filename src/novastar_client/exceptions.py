"""NovaStar API Exception"""

from typing import Dict


class NovaStarAPIError(Exception):
    """Raised when the NovaStar API returns an error response."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        url: str | None = None,
        response_body: str | None = None,
        parsed_body: dict | None = None,
        retryable: bool | None = None,
    ):
        # Final message that Exception.__str__ will show
        details = []

        if status_code is not None:
            details.append(f"status={status_code}")
        if url is not None:
            details.append(f"url={url}")
        if retryable is not None:
            details.append(f"retryable={retryable}")

        suffix = f" ({', '.join(details)})" if details else ""
        full_message = f"{message}{suffix}"

        super().__init__(full_message)

        self.message = message
        self.status_code = status_code
        self.url = url
        self.response_body = response_body
        self.parsed_body = parsed_body
        self.retryable = retryable

    def to_dict(self) -> Dict:
        """to_dict convert to dict

        Returns
        -------
        Dict
            Dictionary representation of the Exception.
        """
        return {
            "message": self.message,
            "status_code": self.status_code,
            "url": self.url,
            "response_body": self.response_body,
            "parsed_body": self.parsed_body,
            "retryable": self.retryable,
        }
