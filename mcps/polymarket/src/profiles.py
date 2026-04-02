from __future__ import annotations

from fastmcp.tools import tool
from pydantic import Field

from .models import ProfileRecord, PublicProfileResponse


class GammaProfilesTools(GammaBase, ClobBase):
    @tool(description="Get Polymarket public profile by wallet address")
    def get_public_profile(
        self, address: str = Field(description="Wallet address")
    ) -> PublicProfileResponse:
        return PublicProfileResponse(**self.gamma_client.get_public_profile(address))

    @tool(description="Get Polymarket public profile by user address")
    def get_public_profile_by_user_address(
        self, user_address: str = Field(description="Wallet address")
    ) -> ProfileRecord:
        return ProfileRecord(**self.gamma_client.get_public_profile_by_user_address(user_address))
