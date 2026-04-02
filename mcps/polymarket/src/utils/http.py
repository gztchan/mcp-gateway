from __future__ import annotations

from collections.abc import Iterable
from typing import Any

import requests

from .errors import PolymarketError


def _normalize_path(path: str) -> str:
    return path.lstrip("/")


def clean_params(params: dict[str, Any] | None) -> dict[str, Any]:
    cleaned: dict[str, Any] = {}
    for key, value in (params or {}).items():
        if value is None:
            continue
        if isinstance(value, tuple):
            value = list(value)
        if isinstance(value, list):
            cleaned[key] = ",".join(str(item) for item in value)
            continue
        if isinstance(value, Iterable) and not isinstance(value, (str, bytes, dict)):
            cleaned[key] = ",".join(str(item) for item in value)
            continue
        cleaned[key] = value
    return cleaned


def request_json(
    *,
    base_url: str,
    path: str,
    method: str = "GET",
    params: dict[str, Any] | None = None,
    json: Any | None = None,
    headers: dict[str, str] | None = None,
    timeout: int = 30,
) -> Any:
    url = f"{base_url.rstrip('/')}/{_normalize_path(path)}"
    response = requests.request(
        method=method,
        url=url,
        params=clean_params(params),
        json=json,
        headers=headers,
        timeout=timeout,
    )

    try:
        payload = response.json()
    except ValueError as exc:
        raise PolymarketError(
            f"Non-JSON response from Polymarket endpoint {method} {url}"
        ) from exc

    if response.ok:
        return payload

    if isinstance(payload, dict) and payload.get("error"):
        raise PolymarketError(payload["error"])

    raise PolymarketError(
        f"Polymarket request failed ({response.status_code}) for {method} {url}"
    )


def request_text(
    *,
    base_url: str,
    path: str,
    method: str = "GET",
    params: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
    timeout: int = 30,
) -> str:
    url = f"{base_url.rstrip('/')}/{_normalize_path(path)}"
    response = requests.request(
        method=method,
        url=url,
        params=clean_params(params),
        headers=headers,
        timeout=timeout,
    )

    if response.ok:
        return response.text

    raise PolymarketError(
        f"Polymarket request failed ({response.status_code}) for {method} {url}"
    )
