# MCP & API Status — Verification Log

Last verified: Session startup

## Playwright / WebFetch (Browser Research)
- **Status**: VERIFIED ✓
- **Test**: Fetched visitcalifornia.com — returned page title "Visit California - Official Travel & Tourism Website"
- **Note**: NPS Big Sur URL (nps.gov/bisu) appears to have been restructured; browser tool confirmed live via visitcalifornia.com

## Google Maps Directions API
- **Status**: VERIFIED ✓
- **Test**: SF → Carmel-by-the-Sea
- **Result**: 2 hrs 2 mins / 122 mi
- **Key**: GOOGLE_MAPS_API_KEY in .env
- **APIs enabled**: Places API, Distance Matrix API, Directions API, Routes API

## Scrape Creators Instagram API
- **Status**: VERIFIED ✓
- **Test**: GET /v1/instagram/profile?handle=natgeo
- **Result**: @natgeo / National Geographic / 269,466,062 followers
- **Auth header**: x-api-key
- **Key**: SCRAPE_CREATORS_API_KEY in .env

## Reference Files
- `references/instagram-endpoints.md` — all 10 endpoints documented ✓
- `references/mcp-status.md` — this file ✓

## .env
- GOOGLE_MAPS_API_KEY — set ✓
- SCRAPE_CREATORS_API_KEY — set ✓
