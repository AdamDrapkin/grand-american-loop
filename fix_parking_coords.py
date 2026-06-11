#!/usr/bin/env python3
"""Geocode correct parking addresses to get accurate lat/lng for fixes."""

import os, urllib.request, urllib.parse, json

API_KEY = open(".env").read().split("GOOGLE_MAPS_API_KEY=")[1].split("\n")[0].strip()

FIXES = [
    # (day, attraction, correct_address_to_geocode)
    ("Day 1", "Ferry Building parking",         "Embarcadero Center Garage, 250 Clay St, San Francisco, CA"),
    ("Day 1", "Russian Hill / Cable Car",        "Fisherman's Wharf Garage, 350 Beach St, San Francisco, CA"),
    ("Day 1", "Painted Ladies / Alamo Square",   "Hayes St & Steiner St, San Francisco, CA 94117"),
    ("Day 2", "Pier 33 / Alcatraz Ferry",        "Pier 33 Embarcadero, San Francisco, CA 94111"),
    ("Day 2", "UC Berkeley",                     "UC Berkeley Parking Structure 4, 2727 Durant Ave, Berkeley, CA"),
    ("Day 2", "Muir Woods parking",              "Muir Woods National Monument, 1 Muir Woods Rd, Mill Valley, CA"),
    ("Day 3", "Bouchon Bakery Yountville",       "Washington St & Humboldt St, Yountville, CA 94599"),
    ("Day 3", "Oxbow Public Market Napa",        "610 1st St, Napa, CA 94559"),
    ("Day 8", "Walt Disney Concert Hall",        "Walt Disney Concert Hall Parking, 101 S Grand Ave, Los Angeles, CA"),
    ("Day 10","Santa Monica Farmers Market",     "Santa Monica Civic Center Parking, 333 Civic Center Dr, Santa Monica, CA"),
]

def geocode(address):
    url = (
        "https://maps.googleapis.com/maps/api/geocode/json"
        f"?address={urllib.parse.quote(address)}&key={API_KEY}"
    )
    with urllib.request.urlopen(url) as r:
        data = json.loads(r.read())
    if data["status"] == "OK" and data["results"]:
        loc = data["results"][0]["geometry"]["location"]
        fmt = data["results"][0]["formatted_address"]
        return loc["lat"], loc["lng"], fmt
    return None, None, f"NO RESULT ({data['status']})"

print(f"{'Day':<6} {'Attraction':<35} {'New coords':<30} {'Verified address'}")
print("-" * 120)
for day, name, address in FIXES:
    lat, lng, fmt = geocode(address)
    if lat:
        print(f"{day:<6} {name:<35} p:[{lat:.4f},{lng:.4f}]         {fmt}")
    else:
        print(f"{day:<6} {name:<35} ERROR: {fmt}")
