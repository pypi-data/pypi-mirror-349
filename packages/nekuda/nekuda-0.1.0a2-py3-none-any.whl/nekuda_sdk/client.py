"""
Main client for Nekuda SDK
"""

import httpx
from typing import Dict, Optional, Any
import time
import os

from .exceptions import NekudaApiError, NekudaConnectionError


class NekudaClient:
    """Client for Nekuda SDK to interact with payment API"""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.nekuda.ai",
        timeout: int = 30,
        *,
        max_retries: int = 3,
        backoff_factor: float = 0.5,
    ) -> None:
        """
        Initialize the Nekuda SDK client

        Args:
            api_key: Customer's API key
            base_url: Base URL for the Nekuda API
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for HTTP requests
            backoff_factor: Factor to increase wait time between retries
        """
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = timeout
        self.version = "0.1.0"  # SDK version

        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

        # Lazily initialised persistent HTTP client (to enable pickling / forking)
        self._session: httpx.Client | None = None

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, str]] = None,
        extra_headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """
        Make an HTTP request to the API gateway

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            data: Request payload
            params: Query parameters
            extra_headers: Optional dictionary of extra headers to include

        Returns:
            API response as dictionary
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        # Base headers
        headers = {
            "Content-Type": "application/json",
            "User-Agent": f"nekuda-sdk-python/{self.version}",
        }
        if extra_headers:
            headers.update(extra_headers)

        # Ensure we have a persistent session
        if self._session is None:
            self._session = httpx.Client(timeout=self.timeout)

        # Retry loop ----------------------------------------------------
        attempt = 0
        while True:
            try:
                response = self._session.request(
                    method=method,
                    url=url,
                    json=data,
                    params=params,
                    headers=headers,
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as exc:
                status = exc.response.status_code
                should_retry = status == 429 or status >= 500
                if should_retry and attempt < self.max_retries:
                    sleep_for = self.backoff_factor * 2**attempt
                    time.sleep(sleep_for)
                    attempt += 1
                    continue

                self._handle_error_response(exc.response)
            except httpx.RequestError as exc:
                if attempt < self.max_retries:
                    sleep_for = self.backoff_factor * 2**attempt
                    time.sleep(sleep_for)
                    attempt += 1
                    continue
                raise NekudaConnectionError(f"Connection error: {str(exc)}")

    def request_card_reveal_token(self, user_id: str, mandate_id: str) -> Dict[str, str]:
        """
        Request a one-time token to reveal card details for a user.

        Args:
            user_id: The identifier for the user.
            mandate_id: The identifier for the mandate to be used.

        Returns:
            Dictionary containing the reveal token ('reveal_token') and
            the API path ('reveal_path') for the next step.
        """
        endpoint = "/api/v1/wallet/request_card_reveal_token"
        headers = {
            "X-API-KEY": self.api_key,
            "x-user-id": user_id,
        }
        payload = {
            "mandate_id": mandate_id
        }
        response_data = self._request(method="POST", endpoint=endpoint, data=payload, extra_headers=headers)

        # As requested, return the token and the path for the reveal step
        return {
            "reveal_token": response_data["token"],
            "reveal_path": "/api/v1/wallet/reveal_card_details",
        }

    def reveal_card_details(self, user_id: str, reveal_token: str) -> Dict[str, str]:
        """
        Reveal card details using a previously obtained reveal token.

        Args:
            user_id: The identifier for the user.
            reveal_token: The one-time token obtained from request_card_reveal_token.

        Returns:
            Dictionary containing card details ('card_number', 'card_expiry_date', 'cardholder_name').
        """
        endpoint = "/api/v1/wallet/reveal_card_details"
        headers = {
            "Authorization": f"Bearer {reveal_token}",  # Add Bearer prefix
            "x-user-id": user_id,
        }
        # Card reveal uses GET method and headers for auth
        return self._request(method="GET", endpoint=endpoint, extra_headers=headers)

    def create_mandate(
        self, user_id: str, request_id: str, mandate_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Send mandate information to the backend before a purchase flow.

        Args:
            user_id: The identifier for the user associated with the mandate.
            request_id: A unique identifier for this mandate request.
            mandate_data: A dictionary containing the details of the mandate.
                          Expected keys include 'product', 'price', 'currency', etc.

        Returns:
            Dictionary representing the response from the backend, likely
            confirming mandate creation or returning the created mandate details.
        """
        # Assume a standard endpoint for mandate creation
        endpoint = "/api/v1/mandate/create"
        headers = {
            "X-API-KEY": self.api_key,
            "x-user-id": user_id,
            # Add request ID header if backend expects it
            "X-Request-ID": request_id,
        }
        # Mandate data is sent as the JSON payload
        payload = mandate_data

        # Send the POST request
        return self._request(
            method="POST", endpoint=endpoint, data=payload, extra_headers=headers
        )

    def _handle_error_response(self, response: httpx.Response) -> None:
        """Extract error details from response and raise appropriate exception"""
        try:
            error_data = response.json()
            error_message = error_data.get("message", "Unknown error")
            error_code = error_data.get("code", "unknown")
        except ValueError:
            error_message = response.text or f"HTTP Error: {response.status_code}"
            error_code = "http_error"

        status = response.status_code

        from .exceptions import (
            AuthenticationError,
            InvalidRequestError,
            RateLimitError,
            ServerError,
        )

        exc_cls = NekudaApiError
        if status == 401:
            exc_cls = AuthenticationError
        elif status == 429:
            exc_cls = RateLimitError
        elif status >= 500:
            exc_cls = ServerError
        elif 400 <= status < 500:
            exc_cls = InvalidRequestError

        raise exc_cls(message=error_message, code=error_code, status_code=status)

    def user(self, user_id: str):
        """Return a :class:`~nekuda_sdk.user.UserContext` bound to *user_id*.

        This is purely a convenience wrapper so callers do not need to repeat
        the ``user_id`` argument on every invocation.
        """
        # Local import to avoid circular dependency at import time.
        from .user import UserContext  # noqa: WPS433 – late import by design

        return UserContext(client=self, user_id=user_id)

    # ------------------------------------------------------------------
    # Lifecycle management ---------------------------------------------
    # ------------------------------------------------------------------
    def close(self) -> None:  # noqa: D401 – explicit close method
        if self._session is not None:
            self._session.close()

    def __del__(self):  # noqa: D401 – ensure resources freed
        try:
            self.close()
        except Exception:  # pragma: no cover – guard against destructor errors
            pass

    # ------------------------------------------------------------------
    # Convenience constructors -----------------------------------------
    # ------------------------------------------------------------------
    @classmethod
    def from_env(cls, *, api_key_var: str = "NEKUDA_API_KEY", base_url_var: str = "NEKUDA_BASE_URL", **kwargs):
        """Instantiate a client using environment variables.

        Parameters
        ----------
        api_key_var:
            Name of the environment variable holding the API key.
        base_url_var:
            Name of the environment variable holding the base URL (optional).
        **kwargs:
            Forwarded to :class:`~nekuda_sdk.client.NekudaClient` constructor
            (e.g. ``timeout``, ``max_retries``).
        """
        api_key = os.getenv(api_key_var)
        if not api_key:
            raise ValueError(f"Environment variable '{api_key_var}' is not set or empty")

        base_url = os.getenv(base_url_var, "https://api.nekuda.ai")

        return cls(api_key=api_key, base_url=base_url, **kwargs)
