from typing import Any

import httpx


async def call_remote_api(
    url: str,
    method: str = "POST",
    headers: dict[str, str] | None = None,
    params: dict[str, Any] | None = None,
    json_data: dict[str, Any] | None = None,
    timeout: float = 30.0,
) -> dict[str, Any]:
    """
    Call a remote REST API endpoint asynchronously using httpx.

    Args:
        url: The remote API endpoint URL
        method: HTTP method (GET, POST, PUT, DELETE, etc.)
        headers: Optional HTTP headers
        params: Optional query parameters
        json_data: Optional JSON request body
        timeout: Request timeout in seconds (default: 30)

    Returns:
        Dictionary containing the response data

    Raises:
        httpx.HTTPError: If the request fails
        httpx.TimeoutException: If the request times out
    """
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.request(
            method=method.upper(),
            url=url,
            headers=headers,
            params=params,
            json=json_data,
        )
        response.raise_for_status()
        return response.json()
