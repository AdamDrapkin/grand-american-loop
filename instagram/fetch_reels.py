#!/usr/bin/env python3
"""Fetch Instagram reels for Yellowstone and Glacier NP queries."""

import urllib.request
import urllib.parse
import json
import re
import os
import time

API_KEY = "oH0cojFTtKhM5tqC7908PIA5XUz2"
BASE_URL = "https://api.scrapecreators.com/v2/instagram/reels/search"

# Constraint keywords that should flag a reel
CONSTRAINT_PATTERNS = [
    r'\b(?:permit|permits|required permit|reservation required)\b',
    r'\b(?:\d+(?:\.\d+)?\s*(?:mile|miles|mi)\b)',  # any mileage mention
    r'\bpaid\b.*\bactivity\b',
    r'\bentry fee\b',
    r'\bticketed\b',
    r'\breservation\b',
]

HIKE_OVER_4MI = re.compile(r'\b([4-9]\d*(?:\.\d+)?|[1-9]\d+(?:\.\d+)?)\s*(?:mile|miles|mi)\b', re.IGNORECASE)
PERMIT_RE = re.compile(r'\b(?:permit|permits|permit required|timed entry|reservation required)\b', re.IGNORECASE)
PAID_RE = re.compile(r'\b(?:paid tour|guided tour|costs?|fee beyond|additional fee)\b', re.IGNORECASE)


def check_constraints(caption: str) -> str:
    """Return a comma-separated string of triggered constraints, or empty string."""
    flags = []
    if caption:
        hike_matches = HIKE_OVER_4MI.findall(caption)
        if hike_matches:
            flags.append(f"hike_distance_mentioned:{','.join(hike_matches[:3])}mi")
        if PERMIT_RE.search(caption):
            flags.append("permit_required_mentioned")
        if PAID_RE.search(caption):
            flags.append("paid_activity_mentioned")
    return "; ".join(flags)


def fetch_query(query: str) -> list:
    """Fetch reels for a query and return cleaned reel objects."""
    encoded = urllib.parse.quote(query, safe='')
    url = f"{BASE_URL}?query={encoded}"
    req = urllib.request.Request(url, headers={"x-api-key": API_KEY})

    with urllib.request.urlopen(req, timeout=30) as resp:
        raw = resp.read()

    # Fix control characters in JSON (common in captions with newlines)
    data = json.loads(raw)

    reels = data.get("reels", [])
    results = []
    for r in reels:
        caption_full = r.get("caption") or ""
        caption_short = caption_full[:200]
        owner = r.get("owner") or {}
        views = r.get("video_view_count") or r.get("video_play_count") or 0

        entry = {
            "query": query,
            "platform": "instagram",
            "url": r.get("url", ""),
            "caption": caption_short,
            "views": views,
            "likes": r.get("like_count", 0),
            "creator": owner.get("username", ""),
            "followers": owner.get("follower_count", 0),
            "flagged_constraint": check_constraints(caption_full),
        }
        results.append(entry)

    return results, data.get("credits_remaining", "?")


YELLOWSTONE_QUERIES = [
    "Yellowstone National Park",
    "Yellowstone tips 2024",
    "Grand Prismatic Spring",
    "Old Faithful Yellowstone",
    "Lamar Valley Yellowstone",
    "Yellowstone hidden gems",
    "Yellowstone avoid crowds",
    "Yellowstone bison",
    "Yellowstone grizzly",
    "Yellowstone morning tips",
    "Yellowstone easy hike",
    "Yellowstone boardwalk",
    "Canyon Village Yellowstone",
    "Artist Point Yellowstone",
    "Yellowstone summer",
]

GLACIER_QUERIES = [
    "Glacier National Park",
    "Going to the Sun Road",
    "Logan Pass Glacier",
    "Many Glacier",
    "Glacier NP tips",
    "Lake McDonald Glacier",
    "Glacier mountain goats",
    "Glacier NP June",
    "St Mary Lake Glacier",
    "Glacier hidden gems",
    "Swiftcurrent Lake",
    "Glacier NP morning",
    "Hidden Lake Glacier",
    "Glacier NP avoid crowds",
    "Glacier NP 2024",
]


def run_all(queries: list, label: str) -> list:
    all_reels = []
    for i, q in enumerate(queries):
        print(f"  [{i+1}/{len(queries)}] {q}...", end=" ", flush=True)
        try:
            reels, credits = fetch_query(q)
            all_reels.extend(reels)
            print(f"{len(reels)} reels | credits left: {credits}")
        except Exception as e:
            print(f"ERROR: {e}")
        if i < len(queries) - 1:
            time.sleep(0.3)  # small polite delay
    return all_reels


print("=== YELLOWSTONE ===")
y_reels = run_all(YELLOWSTONE_QUERIES, "Yellowstone")

print("\n=== GLACIER ===")
g_reels = run_all(GLACIER_QUERIES, "Glacier")

# Deduplicate by URL (same reel can appear in multiple query results)
def dedup(reels):
    seen = {}
    for r in reels:
        url = r["url"]
        if url not in seen or r["views"] > seen[url]["views"]:
            seen[url] = r
    return list(seen.values())

y_reels_dedup = dedup(y_reels)
g_reels_dedup = dedup(g_reels)

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

y_path = os.path.join(OUT_DIR, "yellowstone-reels.json")
g_path = os.path.join(OUT_DIR, "glacier-reels.json")

with open(y_path, "w") as f:
    json.dump(y_reels_dedup, f, indent=2, ensure_ascii=False)

with open(g_path, "w") as f:
    json.dump(g_reels_dedup, f, indent=2, ensure_ascii=False)

print(f"\nSaved {len(y_reels_dedup)} unique Yellowstone reels → {y_path}")
print(f"Saved {len(g_reels_dedup)} unique Glacier reels → {g_path}")

# Print top 5 by views for each park
def top5(reels, label):
    sorted_r = sorted(reels, key=lambda x: x["views"], reverse=True)[:5]
    print(f"\n--- TOP 5 {label} BY VIEWS ---")
    for i, r in enumerate(sorted_r, 1):
        print(f"{i}. @{r['creator']} ({r['followers']:,} followers)")
        print(f"   Views: {r['views']:,} | Likes: {r['likes']:,}")
        print(f"   URL: {r['url']}")
        print(f"   Caption: {r['caption'][:100]}...")
        if r['flagged_constraint']:
            print(f"   FLAGS: {r['flagged_constraint']}")

top5(y_reels_dedup, "YELLOWSTONE")
top5(g_reels_dedup, "GLACIER")
