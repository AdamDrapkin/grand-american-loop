#!/usr/bin/env python3
"""
fix_maps_coords.py — Replace text-based Google Maps links with coordinate-based links.

Working formats (from pre-California guides):
  Individual pin:  https://www.google.com/maps/search/?api=1&query=LAT,LON
  Day route:       https://www.google.com/maps/dir/LAT1,LON1/LAT2,LON2/...

These open the Maps app on mobile and show the exact pin / navigation path.
Text-based links break inside the viewer iframe sandbox.

Run from project root: python3 fix_maps_coords.py
"""

import os
import re
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

GUIDES = [
    "./california/sf-guide.html",
    "./california/bigsur-guide.html",
    "./california/centralcoast-guide.html",
    "./california/sandiego-guide.html",
    "./california/la-guide.html",
]

GMAPS_PATTERN = re.compile(r'href="(https://(?:www\.)?google\.com/maps[^"]+)"')


def read_gmaps_key():
    env_path = Path(__file__).parent / ".env"
    for line in env_path.read_text().splitlines():
        if line.startswith("GOOGLE_MAPS_API_KEY="):
            return line.split("=", 1)[1].strip()
    raise ValueError("GOOGLE_MAPS_API_KEY not found in .env")


def geocode(address, api_key):
    """Return (lat, lng) rounded to 6 decimal places."""
    url = ("https://maps.googleapis.com/maps/api/geocode/json?"
           + urllib.parse.urlencode({"address": address, "key": api_key}))
    with urllib.request.urlopen(url, timeout=10) as r:
        data = json.loads(r.read())
    if data.get("status") == "OK" and data.get("results"):
        loc = data["results"][0]["geometry"]["location"]
        return (round(loc["lat"], 6), round(loc["lng"], 6))
    raise ValueError(f"status={data.get('status')} for '{address}'")


def decode_text(encoded):
    """URL-decode a Google Maps path/query segment."""
    return urllib.parse.unquote_plus(encoded).strip()


def coord_str(lat, lng):
    return f"{lat},{lng}"


def process_url(url, api_key, cache):
    """Return a coordinate-based Maps URL. Returns original if parsing fails."""

    # ── Individual location: /maps/search/TEXT  or  /maps/search/?api=1&query=TEXT ──
    search_m = re.match(
        r'https://(?:www\.)?google\.com/maps/search/([^?#]*?)/?(\?.*)?$', url
    )
    if search_m:
        path_part = (search_m.group(1) or "").strip("/")
        query_part = search_m.group(2) or ""

        if path_part:
            text = decode_text(path_part)
        elif "query=" in query_part:
            params = urllib.parse.parse_qs(query_part.lstrip("?"))
            text = params.get("query", [""])[0]
        else:
            return url

        if not text:
            return url

        try:
            if text not in cache:
                print(f"    geocode: {text}")
                cache[text] = geocode(text, api_key)
                time.sleep(0.15)
            lat, lng = cache[text]
            return f"https://www.google.com/maps/search/?api=1&query={coord_str(lat, lng)}"
        except Exception as e:
            print(f"    ⚠  FAILED '{text}': {e}")
            return url

    # ── Day route: /maps/dir/WAY1/WAY2/... ──────────────────────────────────────
    dir_m = re.match(r'https://(?:www\.)?google\.com/maps/dir/(.+?)/?$', url)
    if dir_m:
        raw_wps = [w for w in dir_m.group(1).split("/") if w]
        coords = []
        for wp in raw_wps:
            text = decode_text(wp)
            try:
                if text not in cache:
                    print(f"    geocode: {text}")
                    cache[text] = geocode(text, api_key)
                    time.sleep(0.15)
                lat, lng = cache[text]
                coords.append(coord_str(lat, lng))
            except Exception as e:
                print(f"    ⚠  FAILED waypoint '{text}': {e}")
                return url  # Keep original if any waypoint fails
        if coords:
            return "https://www.google.com/maps/dir/" + "/".join(coords)

    return url


def fix_file(filepath, api_key, cache):
    content = Path(filepath).read_text(encoding="utf-8")
    link_count = [0]

    def replace_match(m):
        original = m.group(1)
        new_url = process_url(original, api_key, cache)
        link_count[0] += 1
        return f'href="{new_url}"'

    new_content = GMAPS_PATTERN.sub(replace_match, content)

    if new_content != content:
        Path(filepath).write_text(new_content, encoding="utf-8")
        print(f"  ✓ {filepath}  ({link_count[0]} links rewritten)")
    else:
        print(f"  ✓ {filepath}  (no changes)")


def main():
    print()
    print("═" * 60)
    print("  fix_maps_coords.py — Coordinate Link Rebuilder")
    print("═" * 60)
    print()

    api_key = read_gmaps_key()
    print(f"  GOOGLE_MAPS_API_KEY loaded ✓")
    print()

    cache = {}

    for guide in GUIDES:
        print(f"  [{Path(guide).stem}]")
        fix_file(guide, api_key, cache)
        print()

    print(f"  Geocoded {len(cache)} unique locations.")
    print()
    print("  Next: python3 build_california.py")
    print()


if __name__ == "__main__":
    main()
