from __future__ import annotations

from fastmcp.tools import tool


class GammaStatusTools:
    @tool(description="Get Polymarket Gamma API health status")
    def get_gamma_status(self) -> str:
        return self.gamma_client.get_status()
