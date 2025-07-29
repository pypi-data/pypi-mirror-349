# SPDX-FileCopyrightText: 2025-present Shane Rogers <shane@teer.ai>
#
# SPDX-License-Identifier: MIT

from typing import Dict, Any, Optional, TYPE_CHECKING
import logging
import requests

if TYPE_CHECKING:
    from .. import TeerClient

logger = logging.getLogger("teer")


class BaseResource:
    """Base class for all Teer API resources."""

    def __init__(
        self,
        client: "TeerClient",
        resource_path: str,
        resource_base_url: Optional[str] = None,
    ):
        """
        Initialize the base resource.

        Args:
            client: The Teer client instance.
            resource_path: The path to the resource, e.g., "ingest".
            resource_base_url: Optional base URL for this resource. If not provided,
                              defaults to the client's api_base.
        """
        self.client = client
        base_url = resource_base_url or client.api_base
        self.base_url = f"{base_url}/{resource_path}"

    def _request(
        self,
        method: str,
        path: str = "",
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 10,
    ) -> Dict[str, Any]:
        """
        Make a request to the Teer API using the shared HTTP client.

        Args:
            method: The HTTP method to use (GET, POST, etc.).
            path: The path to append to the base URL.
            params: Query parameters for the request.
            data: JSON data for the request body.
            headers: Additional headers to include in the request.
            timeout: Request timeout in seconds.

        Returns:
            The response from the Teer API.

        Raises:
            Exception: If the request fails.
        """
        # Calculate the full path relative to the resource base URL
        resource_path = path.lstrip("/") if path else ""

        # Construct the full URL for the request using the resource's base URL
        # This ensures we use the correct base URL (api or track) for each resource
        full_url = f"{self.base_url}/{resource_path}".rstrip("/")
        if resource_path:
            full_url = f"{self.base_url}/{resource_path}"
        else:
            full_url = self.base_url

        logger.debug(f"Making {method} request to {full_url}")
        if data:
            logger.debug(f"Request data: {data}")

        # Make the request directly using the requests library
        # This bypasses the HTTP client's base URL and uses the resource's base URL
        try:
            # Ensure we always have the Authorization and Content-Type headers
            request_headers = {
                "Authorization": f"Bearer {self.client.api_key}",
                "Content-Type": "application/json",
            }

            # Add any additional headers
            if headers:
                request_headers.update(headers)

            response = requests.request(
                method=method,
                url=full_url,
                params=params,
                json=data,
                headers=request_headers,
                timeout=timeout,
            )
            response.raise_for_status()

            # Try to parse the response as JSON
            try:
                return response.json()
            except ValueError:
                # If the response is not JSON, return the text
                return {"text": response.text}

        except Exception as e:
            logger.error(f"Error making request to {full_url}: {str(e)}")
            # Re-raise the exception for the caller to handle
            raise
