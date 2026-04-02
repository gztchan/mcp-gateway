from __future__ import annotations

from .utils.clob_public_client import ClobPublicClient
from .utils.clob_trading_client import ClobTradingClient
from .utils.data_client import DataClient
from .utils.gamma_client import GammaClient

class PolymarketClobBase:
    def __init__(self) -> None:
        self.clob_public_client = ClobPublicClient()
        self.clob_trading_client = ClobTradingClient()

class PolymarketDataBase:
    def __init__(self) -> None:
        self.data_client = DataClient()

class PolymarketGammaBase:
    def __init__(self) -> None:
        self.gamma_client = GammaClient()
