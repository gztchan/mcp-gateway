from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class PolymarketModel(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)


class ApiError(PolymarketModel):
    error: str = Field(description="Polymarket API error message")


class EventMarketRef(PolymarketModel):
    id: str | int | None = None
    slug: str | None = None
    question: str | None = None


class EventDetails(PolymarketModel):
    id: str | int | None = None
    title: str | None = None
    slug: str | None = None
    description: str | None = None
    active: bool | None = None
    closed: bool | None = None
    liquidity: float | None = None
    volume: float | None = None
    start_date: str | None = Field(default=None, alias="startDate")
    end_date: str | None = Field(default=None, alias="endDate")
    created_at: str | None = Field(default=None, alias="createdAt")
    markets: list[EventMarketRef] = Field(default_factory=list)


class MarketOutcomeToken(PolymarketModel):
    token_id: str | None = None
    outcome: str | None = None
    price: float | None = None
    winner: bool | None = None


class MarketDetails(PolymarketModel):
    id: str | int | None = None
    condition_id: str | None = Field(default=None, alias="conditionId")
    slug: str | None = None
    question: str | None = None
    active: bool | None = None
    closed: bool | None = None
    archived: bool | None = None
    volume: float | None = None
    liquidity: float | None = None
    yes_token: str | None = None
    no_token: str | None = None
    tokens: list[MarketOutcomeToken] = Field(default_factory=list)


class TagSummary(PolymarketModel):
    id: str | int | None = None
    label: str | None = None
    slug: str | None = None


class SeriesSummary(PolymarketModel):
    id: str | int | None = None
    slug: str | None = None
    title: str | None = None
    ticker: str | None = None


class SeriesDetails(PolymarketModel):
    id: str | int | None = None
    slug: str | None = None
    title: str | None = None
    ticker: str | None = None


class TagDetails(PolymarketModel):
    id: str | int | None = None
    label: str | None = None
    slug: str | None = None


class RelatedTag(PolymarketModel):
    pass


class TeamSummary(PolymarketModel):
    id: int | None = None
    name: str | None = None
    league: str | None = None
    abbreviation: str | None = None
    alias: str | None = None


class SportsMetadata(PolymarketModel):
    sport: str | None = None
    image: str | None = None
    resolution: str | None = None
    ordering: str | None = None
    tags: str | None = None
    series: str | None = None


class SearchPagination(PolymarketModel):
    page: int | None = None
    has_more: bool | None = None
    count: int | None = None


class ProfileSummary(PolymarketModel):
    name: str | None = None
    pseudonym: str | None = None
    bio: str | None = None
    profileImage: str | None = None
    wallet_address: str | None = Field(default=None, alias="walletAddress")


class SearchResults(PolymarketModel):
    events: list[EventDetails] = Field(default_factory=list)
    tags: list[TagSummary] = Field(default_factory=list)
    profiles: list[ProfileSummary] = Field(default_factory=list)
    pagination: SearchPagination | None = None


class PaginationInfo(PolymarketModel):
    has_more: bool | None = Field(default=None, alias="hasMore")
    total_results: int | None = Field(default=None, alias="totalResults")


class EventsPaginationResponse(PolymarketModel):
    data: list[EventDetails] = Field(default_factory=list)
    pagination: PaginationInfo | None = None


class CountResponse(PolymarketModel):
    count: int | None = None


class EventTweetCount(PolymarketModel):
    tweet_count: int | None = Field(default=None, alias="tweetCount")


class EventCreator(PolymarketModel):
    id: int | None = None
    name: str | None = None
    handle: str | None = None


class PriceLevel(PolymarketModel):
    price: float | None = None
    size: float | None = None


class Orderbook(PolymarketModel):
    market: str | None = None
    asset_id: str | None = None
    timestamp: str | None = None
    hash: str | None = None
    neg_risk: bool | None = None
    min_order_size: str | None = None
    tick_size: str | None = None
    last_trade_price: str | None = None
    bids: list[PriceLevel] = Field(default_factory=list)
    asks: list[PriceLevel] = Field(default_factory=list)


class PriceQuote(PolymarketModel):
    token_id: str | None = None
    side: Literal["BUY", "SELL"] | None = None
    price: float | None = None


class SpreadQuote(PolymarketModel):
    token_id: str | None = None
    spread: float | None = None


class MidpointQuote(PolymarketModel):
    token_id: str | None = None
    midpoint: float | None = None


class LastTradePrice(PolymarketModel):
    token_id: str | None = None
    price: float | None = None
    side: str | None = None


class PriceHistoryPoint(PolymarketModel):
    t: int | None = None
    p: float | None = None


class PriceHistoryResponse(PolymarketModel):
    history: list[PriceHistoryPoint] = Field(default_factory=list)


class ClobMarketByToken(PolymarketModel):
    condition_id: str | None = None
    primary_token_id: str | None = None
    secondary_token_id: str | None = None


class MarketDescription(PolymarketModel):
    description: str | None = None


class KeysetMarketsResponse(PolymarketModel):
    markets: list[MarketDetails] = Field(default_factory=list)
    next_cursor: str | None = None


class KeysetEventsResponse(PolymarketModel):
    events: list[EventDetails] = Field(default_factory=list)
    next_cursor: str | None = None


class SportsMarketTypesResponse(PolymarketModel):
    market_types: list[str] = Field(default_factory=list, alias="marketTypes")


class CommentRecord(PolymarketModel):
    id: int | None = None
    body: str | None = None


class ProfileRecord(PolymarketModel):
    name: str | None = None
    pseudonym: str | None = None
    bio: str | None = None
    profileImage: str | None = None
    wallet_address: str | None = Field(default=None, alias="walletAddress")


class PublicProfileResponse(PolymarketModel):
    profile: ProfileRecord | None = None


class CursorPage(PolymarketModel):
    limit: int | None = None
    next_cursor: str | None = None
    count: int | None = None
    data: list[Any] = Field(default_factory=list)


class TradeRecord(PolymarketModel):
    proxyWallet: str | None = None
    side: str | None = None
    asset: str | None = None
    conditionId: str | None = None
    size: float | None = None
    price: float | None = None
    timestamp: int | None = None
    title: str | None = None
    slug: str | None = None
    eventSlug: str | None = None
    outcome: str | None = None
    transactionHash: str | None = None


class HolderRecord(PolymarketModel):
    proxyWallet: str | None = None
    asset: str | None = None
    pseudonym: str | None = None
    amount: float | None = None
    outcomeIndex: int | None = None
    name: str | None = None


class MarketHolders(PolymarketModel):
    token: str | None = None
    holders: list[HolderRecord] = Field(default_factory=list)


class OpenInterestRecord(PolymarketModel):
    market: str | None = None
    value: float | None = None


class PositionRecord(PolymarketModel):
    proxyWallet: str | None = None
    asset: str | None = None
    conditionId: str | None = None
    size: float | None = None
    avgPrice: float | None = None
    initialValue: float | None = None
    currentValue: float | None = None
    cashPnl: float | None = None
    percentPnl: float | None = None
    title: str | None = None
    slug: str | None = None
    eventSlug: str | None = None
    outcome: str | None = None


class ClosedPositionRecord(PolymarketModel):
    proxyWallet: str | None = None
    asset: str | None = None
    conditionId: str | None = None
    realizedPnl: float | None = None
    avgPrice: float | None = None
    timestamp: int | None = None
    title: str | None = None
    slug: str | None = None
    eventSlug: str | None = None
    outcome: str | None = None


class ActivityRecord(PolymarketModel):
    proxyWallet: str | None = None
    timestamp: int | None = None
    conditionId: str | None = None
    type: str | None = None
    size: float | None = None
    usdcSize: float | None = None
    transactionHash: str | None = None
    price: float | None = None
    asset: str | None = None
    side: str | None = None
    title: str | None = None
    slug: str | None = None
    eventSlug: str | None = None
    outcome: str | None = None


class ValueRecord(PolymarketModel):
    user: str | None = None
    value: float | None = None


class ApiCredentials(PolymarketModel):
    api_key: str | None = None
    api_secret: str | None = None
    api_passphrase: str | None = None


class OrderPlacementResponse(PolymarketModel):
    success: bool | None = None
    orderID: str | None = None
    status: str | None = None
    makingAmount: str | None = None
    takingAmount: str | None = None
    transactionsHashes: list[str] = Field(default_factory=list)
    tradeIDs: list[str] = Field(default_factory=list)
    errorMsg: str | None = None


class OpenOrderRecord(PolymarketModel):
    id: str | None = None
    status: str | None = None
    owner: str | None = None
    maker_address: str | None = None
    market: str | None = None
    asset_id: str | None = None
    side: str | None = None
    original_size: str | None = None
    size_matched: str | None = None
    price: str | None = None
    outcome: str | None = None
    expiration: str | None = None
    order_type: str | None = None
    associate_trades: list[str] = Field(default_factory=list)
    created_at: int | None = None


class CancelOrdersResponse(PolymarketModel):
    canceled: list[str] = Field(default_factory=list)
    not_canceled: dict[str, str] = Field(default_factory=dict)
