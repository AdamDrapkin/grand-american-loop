#!/usr/bin/env python3
"""Reverse-geocode every parking coord in the guide files via Google Maps API."""

import os, urllib.request, urllib.parse, json

API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY") or open(".env").read().split("GOOGLE_MAPS_API_KEY=")[1].split("\n")[0].strip()

PARKING = [
    # Day 1 — SF
    ("Day 1", "Ferry Building",             37.7951, -122.3963),
    ("Day 1", "Palace of Fine Arts",        37.8023, -122.4493),
    ("Day 1", "Russian Hill / Cable Car",   37.8008, -122.4116),
    ("Day 1", "Painted Ladies / Alamo Sq",  37.7817, -122.4320),
    ("Day 1", "Golden Gate Park Garage",    37.7700, -122.4683),
    ("Day 1", "Twin Peaks",                 37.7546, -122.4463),
    # Day 2 — SF day trips
    ("Day 2", "Pier 33 / Alcatraz Ferry",   37.8064, -122.4103),
    ("Day 2", "Fort Point NHS",             37.8063, -122.4760),
    ("Day 2", "UC Berkeley",                37.8734, -122.2629),
    ("Day 2", "Muir Woods",                 37.8913, -122.5688),
    # Day 3 — Napa
    ("Day 3", "Bouchon Bakery Yountville",  38.4035, -122.3616),
    ("Day 3", "Sterling Vineyards",         38.5697, -122.5472),
    ("Day 3", "Oxbow Public Market Napa",   38.2964, -122.2857),
    # Day 4 — Big Sur / Carmel
    ("Day 4", "17-Mile Drive",              36.5728, -121.9487),
    ("Day 4", "Carmel-by-the-Sea",          36.5558, -121.9243),
    ("Day 4", "Point Lobos State Reserve",  36.5155, -121.9478),
    ("Day 4", "Bixby Creek Bridge",         36.3715, -121.9019),
    ("Day 4", "Pfeiffer Beach",             36.2381, -121.8162),
    ("Day 4", "McWay Falls / JPBSP",        36.1589, -121.6692),
    ("Day 4", "Ragged Point",               35.7806, -121.3300),
    ("Day 4", "Elephant Seals Piedras",     35.6650, -121.2540),
    # Day 5 — Central Coast
    ("Day 5", "Hearst Castle Visitor Ctr",  35.6556, -121.1663),
    ("Day 5", "Solvang",                    34.5958, -120.1376),
    # Day 6 — Coastal drive
    ("Day 6", "El Matador State Beach",     34.0380, -118.8747),
    ("Day 6", "Newport Beach / Balboa Is",  33.6158, -117.9284),
    ("Day 6", "Laguna Beach Heisler Park",  33.5427, -117.7822),
    ("Day 6", "La Jolla Cove",              32.8504, -117.2729),
    # Day 8 — LA Beverly Hills / Hollywood
    ("Day 8", "Rodeo Drive",                34.0667, -118.3985),
    ("Day 8", "Hollywood Walk of Fame",     34.1021, -118.3270),
    ("Day 8", "Walt Disney Concert Hall",   34.0521, -118.2476),
    # Day 9 — LA Griffith / Venice
    ("Day 9", "Griffith Observatory",       34.1210, -118.2965),
    ("Day 9", "Venice Boardwalk",           33.9857, -118.4691),
    # Day 10 — Santa Monica / Getty
    ("Day 10", "Santa Monica Farmers Mkt",  34.0141, -118.4974),
    ("Day 10", "Getty Center",              34.0878, -118.4757),
]

def reverse_geocode(lat, lng):
    url = (
        "https://maps.googleapis.com/maps/api/geocode/json"
        f"?latlng={lat},{lng}&key={API_KEY}"
    )
    with urllib.request.urlopen(url) as r:
        data = json.loads(r.read())
    if data["status"] == "OK" and data["results"]:
        return data["results"][0]["formatted_address"]
    return f"NO RESULT ({data['status']})"

print(f"{'Day':<6} {'Attraction':<35} {'Coords':<26} {'Google Maps Address'}")
print("-" * 120)
for day, name, lat, lng, in PARKING:
    addr = reverse_geocode(lat, lng)
    print(f"{day:<6} {name:<35} {lat},{lng:<20} {addr}")
