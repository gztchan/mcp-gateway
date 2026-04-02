```bash
npx mcporter call 'http://192.168.5.192:9091/mcp.hackernews_get_listing_stories(
  cdp_url: "http://providence-edge.service.local/browser?browser_id=7d1a3171-06c6-4818-b504-907cee91ce28",
  type: "ask",
  limit: 50
)' --allow-http

npx mcporter call 'http://192.168.5.192:9091/mcp.hackernews_read_story(
  cdp_url: "http://providence-edge.service.local/browser?browser_id=7d1a3171-06c6-4818-b504-907cee91ce28",
  hackernews_story_url: "https://news.ycombinator.com/item?id=48100192"
)' --allow-http
```