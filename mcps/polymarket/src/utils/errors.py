from __future__ import annotations


class PolymarketError(RuntimeError):
    pass


def require_env(name: str) -> str:
    import os

    value = os.getenv(name)
    if not value:
        raise PolymarketError(f"Missing required environment variable: {name}")
    return value
