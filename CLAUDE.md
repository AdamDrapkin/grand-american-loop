# CLAUDE.md

## Project
10-day California family road trip planner (SF to LA). Builds an unhurried, research-backed itinerary through interactive intake of images, text, and Instagram content from the user.

## Stack
Claude Code, Playwright MCP (browser automation + research), Google Maps MCP (live routing), Scrape Creators REST API (Instagram data), Node.js 18+

## Commands
- Add Playwright: `claude mcp add playwright npx @playwright/mcp@latest`
- Test Playwright: navigate to https://www.nps.gov/bisu/index.htm, return page title
- Test Google Maps: get directions from San Francisco to Carmel-by-the-Sea
- Test Scrape Creators: GET Instagram profile for `natgeo` (public account)
- Check .env is populated: `cat .env` (both keys must be present)

## Architecture
- `.env` → GOOGLE_MAPS_API_KEY, SCRAPE_CREATORS_API_KEY (never hardcode either)
- `references/instagram-endpoints.md` → all 10 Scrape Creators Instagram endpoint specs
- `references/mcp-status.md` → verification results written during setup
- System prompt → travel planning agent instructions (read-only, never modify)

## Rules
- NEVER begin travel planning until all three tools pass the Step 0D system check
- NEVER guess driving times — call Google Maps for every route, show the result explicitly
- NEVER recommend any destination, hotel, or restaurant without a Playwright research pass first
- NEVER hardcode API keys — always load from `.env`
- IMPORTANT: Scrape Creators authentication header is `x-api-key`, not `Authorization`
- IMPORTANT: All Instagram API calls must reference `references/instagram-endpoints.md` for correct paths and params
- All `.env` writes prompt the user — Claude does not silently overwrite existing keys

## Workflow
- On activation: read official docs → install tools → verify each → build reference files → signal ready
- During planning intake: one clarifying question per turn, never a list of questions
- Every new destination gets a Playwright research pass before being added to the candidate list
- Every driving time is pulled from Google Maps and shown as "X hrs Y mins" in the plan
- Instagram Reels and posts submitted by the user are processed via Scrape Creators transcript + comments endpoints

## Out of scope
- Do not modify `.env` without prompting the user
- Do not produce the final itinerary until the user explicitly signals intake is complete
- Do not re-run the full setup sequence mid-session unless a tool fails verification
- Do not add more than 3 activities per day — comfort over coverage
