from fastmcp import FastMCP

from .base import PolymarketBase
from .gamma_comments import GammaCommentsTools
from .clob_market_data import ClobMarketDataTools
from .clob_trading import ClobTradingTools
from .data_market_analytics import DataMarketAnalyticsTools
from .data_trades import DataTradesTools
from .data_user_analytics import DataUserAnalyticsTools
from .gamma_events import GammaEventsTools
from .gamma_markets import GammaMarketsTools
from .gamma_profiles import GammaProfilesTools
from .gamma_search import GammaSearchTools
from .gamma_status import GammaStatusTools
from .gamma_taxonomy import GammaTaxonomyTools


class Polymarket(
    PolymarketBase,
    GammaStatusTools,
    GammaEventsTools,
    GammaMarketsTools,
    GammaSearchTools,
    GammaTaxonomyTools,
    GammaCommentsTools,
    GammaProfilesTools,
    DataTradesTools,
    DataMarketAnalyticsTools,
    DataUserAnalyticsTools,
    ClobMarketDataTools,
    ClobTradingTools,
):
    pass


polymarket_mcp = FastMCP("Polymarket")
polymarket = Polymarket()

for tool_fn in [
    polymarket.get_gamma_status,
    polymarket.list_events,
    polymarket.list_events_keyset,
    polymarket.list_events_pagination,
    polymarket.list_events_results,
    polymarket.get_event_by_id,
    polymarket.get_event_by_slug,
    polymarket.get_event_details,
    polymarket.get_event_tweet_count,
    polymarket.get_event_comments_count,
    polymarket.get_event_tags,
    polymarket.list_event_creators,
    polymarket.get_event_creator,
    polymarket.list_markets,
    polymarket.list_markets_keyset,
    polymarket.get_market_by_id,
    polymarket.get_market_by_slug,
    polymarket.get_market_details,
    polymarket.get_market_description,
    polymarket.get_market_tags,
    polymarket.get_markets_information,
    polymarket.get_abridged_markets,
    polymarket.search_public,
    polymarket.search,
    polymarket.list_tags,
    polymarket.get_tag_by_id,
    polymarket.get_tag_by_slug,
    polymarket.get_related_tags_by_id,
    polymarket.get_related_tags_by_slug,
    polymarket.get_tags_related_to_tag_by_id,
    polymarket.get_tags_related_to_tag_by_slug,
    polymarket.list_series,
    polymarket.get_series_by_id,
    polymarket.get_series_comments_count,
    polymarket.get_series_summary_by_id,
    polymarket.get_series_summary_by_slug,
    polymarket.list_sports,
    polymarket.list_sports_market_types,
    polymarket.list_teams,
    polymarket.get_team_by_id,
    polymarket.list_comments,
    polymarket.get_comments_by_id,
    polymarket.get_comments_by_user_address,
    polymarket.get_public_profile,
    polymarket.get_public_profile_by_user_address,
    polymarket.list_trades,
    polymarket.get_holders,
    polymarket.get_open_interest,
    polymarket.get_positions,
    polymarket.get_closed_positions,
    polymarket.get_activity,
    polymarket.get_value,
    polymarket.get_book,
    polymarket.get_books,
    polymarket.get_price,
    polymarket.get_prices,
    polymarket.get_midpoint,
    polymarket.get_midpoints,
    polymarket.get_spread,
    polymarket.get_spreads,
    polymarket.get_price_history,
    polymarket.get_market_by_token,
    polymarket.get_clob_market_info,
    polymarket.get_simplified_markets,
    polymarket.get_market_orderbook,
    polymarket.create_or_derive_api_credentials,
    polymarket.create_readonly_api_key,
    polymarket.list_api_keys,
    polymarket.place_order,
    polymarket.place_market_order,
    polymarket.list_open_orders,
    polymarket.get_order,
    polymarket.list_trades_private,
    polymarket.cancel_order,
    polymarket.cancel_orders,
    polymarket.cancel_all_orders,
    polymarket.cancel_orders_for_market,
    polymarket.post_heartbeat,
]:
    polymarket_mcp.add_tool(tool_fn)