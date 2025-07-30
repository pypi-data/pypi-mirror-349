"""
Core client functionality for the BotRun Hatch Client.
"""

import json
import asyncio
from typing import Dict, Any, Optional
import aiohttp


class HatchClient:
    """Client for interacting with the BotRun Hatch API using aiohttp."""

    def __init__(self, api_key: str, base_url: str = "https://api.botrun.io"):
        """
        Initialize the Hatch Client.

        Args:
            api_key: The API key for authentication
            base_url: The base URL for the API (default: https://api.botrun.io)
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self._session = None

    async def _get_session(self) -> aiohttp.ClientSession:
        """
        Get or create an aiohttp ClientSession.

        Returns:
            An aiohttp ClientSession
        """
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
        return self._session

    async def close(self):
        """Close the aiohttp session."""
        if self._session and not self._session.closed:
            await self._session.close()

    def format_payload(self, data: Dict[str, Any]) -> str:
        """
        Format a dictionary payload as a JSON string.

        Args:
            data: Dictionary containing the payload data

        Returns:
            Formatted JSON string
        """
        return json.dumps(data, indent=2, sort_keys=True)

    async def validate_connection(self) -> Dict[str, Any]:
        """
        Validate the connection to the BotRun API asynchronously.

        This is a simple validation function that would normally make an API call,
        but for this example it just returns a status response.

        Returns:
            A dictionary with connection status information
        """
        # In a real implementation, this would make an API request with aiohttp
        # For demonstration purposes, we just return a mock response
        # await asyncio.sleep(0.1)  # Simulate network delay
        return {
            "status": "connected",
            "api_version": "1.0",
            "endpoint": self.base_url,
            "authenticated": True,
        }

    async def make_request(
        self,
        endpoint: str,
        method: str = "GET",
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make an HTTP request to the API asynchronously.

        Args:
            endpoint: API endpoint to call (will be appended to base_url)
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            data: Optional data to send in the request body
            params: Optional query parameters

        Returns:
            JSON response from the API as a dictionary
        """
        session = await self._get_session()
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        method = method.upper()
        kwargs = {}

        if params:
            kwargs["params"] = params
        if data:
            kwargs["json"] = data

        async with session.request(method, url, **kwargs) as response:
            response.raise_for_status()
            return await response.json()
