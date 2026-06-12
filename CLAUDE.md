# CLAUDE.md

## Project
Grand American Loop — two active family road trips planned simultaneously:
- **Pre-California**: Huntingdon Valley PA → Kansas City → Glacier → Yellowstone → San Francisco (multi-segment truck drive, pets on board)
- **California**: San Francisco → Los Angeles, 10 days

## Viewers (GitHub Pages — live after every push)
- Pre-California: https://adamdrapkin.github.io/grand-american-loop/ (`docs/index.html`)
- California: https://adamdrapkin.github.io/grand-american-loop/california-viewer.html (`docs/california-viewer.html`)

After editing any HTML source file: rebuild the relevant viewer → commit → push to GitHub. A successful push is confirmation the viewer is live. No verification step needed.

## Stack & When to Use Each Tool

**Web Search / Web Fetch** — Default for all research. Use these first for any fact-finding: hours, pricing, reviews, road conditions, attraction info. No approval needed.

**Google Maps API** — NOT an MCP. Activated by `GOOGLE_MAPS_API_KEY` from `.env` and called via Python scripts. Has 33 tools: Routes API (drive times), Places API (location lookups), Geocoding API (coordinate verification), Directions Matrix, and more. Every drive time must come from a live API call and be shown as "X hrs Y mins." Always use Google Maps when the user requests it — never substitute another tool.

**Playwright MCP** — Use ONLY when Web Search and Web Fetch cannot retrieve the needed information AND the user explicitly approves it. Never launch Playwright on your own initiative.

**Scrape Creators** — Three identities: (1) REST API accessed directly via `x-api-key` header, (2) MCP server, (3) agent skill at `.claude/skills/scrapecreators-api/`. Connects to 33+ platforms — not Instagram only. Use ONLY when the user explicitly requests it. Read `references/instagram-endpoints.md` before any Instagram-specific call.

**Open B&B MCP** — Airbnb catalog integration for accommodations and restaurants. Use ONLY with explicit user approval. Never use Open B&B tools in response to a Google Maps request — always use the tool the user names. Do not confuse Open B&B tools with Google Maps API calls.

## Commands
- Build pre-california viewer (full manual):
  `cd pre-california && python3 ../build.py && cp docs/index.html ../docs/index.html && rm -rf docs && cd ..`
- Build pre-california viewer (push-only shortcut):
  Commit and push source changes in `pre-california/` — GitHub Action auto-builds and commits `docs/index.html`
- Build california viewer (always manual — no Action):
  `python3 build_california.py` (run from project root)
- Add Playwright MCP: `claude mcp add playwright npx @playwright/mcp@latest`
- Verify .env: `cat .env` (both keys must be non-empty)
- Cloud bootstrap (if .env missing): `echo "GOOGLE_MAPS_API_KEY=$GOOGLE_MAPS_API_KEY" > .env && echo "SCRAPE_CREATORS_API_KEY=$SCRAPE_CREATORS_API_KEY" >> .env`

## Architecture
- `pre-california/` → segment HTML guides + Leaflet maps + logistics strips (source files)
- `california/` → California HTML source files (california-routes, sf-guide, bigsur-guide, centralcoast-guide, sandiego-guide, la-guide, logistics-guide, itinerary-v2)
- `docs/index.html` → pre-California viewer (auto-built by GitHub Actions on push to main)
- `docs/california-viewer.html` → California viewer (built manually — GitHub Action does NOT auto-build this)
- `build.py` → builds pre-california viewer; outputs to `pre-california/docs/index.html` when run from `pre-california/`; copy step required to reach `docs/index.html`
- `build_california.py` → builds california viewer; run from project root; outputs directly to `docs/california-viewer.html`
- `.claude/skills/california-html-builder/` → invoke when building California HTML source files
- `.claude/skills/scrapecreators-api/` → invoke for any Scrape Creators task
- `.env` → GOOGLE_MAPS_API_KEY, SCRAPE_CREATORS_API_KEY (never hardcode; cloud: written from env vars via bootstrap)
- `references/` → instagram-endpoints.md, mcp-status.md, parking-api.md, route-analysis.md
- Root utility scripts: fix_maps_coords.py, fix_parking_coords.py, inject_photos.py, verify_parking.py — maintenance tools, not part of the build pipeline

## Rules
- NEVER guess driving times — call Google Maps Routes API via Python; show "X hrs Y mins"
- NEVER hardcode API keys — always load from `.env`
- NEVER commit `.env` — keys in Codespaces Secrets (cloud) or local `.env` only
- NEVER re-run full MCP setup mid-session — tools are installed; just verify responsiveness
- NEVER add more than 3 activities per day — comfort over coverage
- NEVER edit viewer files directly — build via the correct build script, then push
- NEVER use Playwright without explicit user approval
- NEVER use Open B&B without explicit user approval
- NEVER substitute one tool for another when the user names a specific tool
- IMPORTANT: Scrape Creators auth header is `x-api-key`, not `Authorization`
- IMPORTANT: Read `references/instagram-endpoints.md` before every Scrape Creators Instagram call
- IMPORTANT: If `.env` is missing at session start, run cloud bootstrap before doing anything else

## Workflow
- Session start: verify `.env` → confirm tools → read project files → produce Session State Report
- One clarifying question per turn, never a list
- After any HTML edit: rebuild the relevant viewer using the correct command → commit → push → done
- Every drive time: call Google Maps via Python script, show result explicitly

## Out of scope
- Do not produce final itinerary until user explicitly signals intake complete
- Do not plan the return trip (post-July 12, California → Huntingdon Valley PA) — determined after California
- Do not modify `.env` without prompting the user
