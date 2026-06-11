# Parking API Reference

## Decision

**Winner: Google Maps Places API — Nearby Search (type=parking)**

- Already authorized via `GOOGLE_MAPS_API_KEY` in `.env` — no new credential needed
- Returns named lots with street addresses and coordinates
- 20 results per query, ranked by proximity
- Free tier: $200/month credit (~40,000 searches)
- Overpass API tested as fallback; results were unnamed/unlabeled lots without addresses — not usable for navigation links

## Endpoint

```
GET https://maps.googleapis.com/maps/api/place/nearbysearch/json
  ?location={lat},{lng}
  &radius={meters}          # 400–800 for urban, 1000–1500 for rural
  &type=parking
  &key=$GOOGLE_MAPS_API_KEY
```

Filter strategy: skip results with "bicycle" in the name; take `results[0]` (closest).

## Fields Available Per Result

| Field | Path in response |
|-------|-----------------|
| Lot name | `results[].name` |
| Street address | `results[].vicinity` |
| Latitude | `results[].geometry.location.lat` |
| Longitude | `results[].geometry.location.lng` |
| Ratings | `results[].rating` (not used) |
| Pricing | **Not returned** — dollar amounts not in Places API |

> Dollar pricing not available; navigation link to the lot is the primary use case.

---

## Parking Coordinates — All Drive-To Stops

### Day 1 — SF (Transit / Rideshare Day — no personal vehicle)

| Stop | Lot Name | Address | lat | lng |
|------|----------|---------|-----|-----|
| Embarcadero / Ferry Building | Four Embarcadero Center Lot #77 | 4 Embarcadero Center, SF | 37.7951 | -122.3963 |
| Palace of Fine Arts | Parking Lot for Palace of Fine Arts Theatre | 3399 Lyon St, SF | 37.8023 | -122.4493 |
| Russian Hill / Lombard St | Public Parking Garage | 721 Filbert St, SF | 37.8008 | -122.4116 |
| Alamo Square | Impark — Fillmore Heritage Garage | 1310 Fillmore St, SF | 37.7817 | -122.4320 |
| Golden Gate Park / Tea Garden | Music Concourse Underground Garage | 55 Hagiwara Tea Garden Dr, SF | 37.7728 | -122.4682 |
| Twin Peaks | Twin Peaks Parking | Twin Peaks Blvd, SF | 37.7546 | -122.4463 |

### Day 2 — SF Day Trips (Rental Car)

| Stop | Lot Name | Address | lat | lng |
|------|----------|---------|-----|-----|
| Pier 33 / Alcatraz Ferry | Impark — C Garage Lot 20 | 2210 Stockton St, SF | 37.8064 | -122.4103 |
| Fort Point / Golden Gate Bridge | Battery Cranston Rd Parking | Battery Cranston Rd, Presidio | 37.8063 | -122.4760 |
| UC Berkeley | Wellman Courtyard Parking | Berkeley | 37.8734 | -122.2629 |
| Muir Woods | Muir Woods Overflow Parking Lot | Muir Woods Rd, Mill Valley | 37.8913 | -122.5688 |

### Day 3 — Wine Country

| Stop | Lot Name | Address | lat | lng |
|------|----------|---------|-----|-----|
| Yountville / Bouchon Bakery | Public Parking Lot | Yount Street, Yountville | 38.4035 | -122.3616 |
| Calistoga / Sterling Vineyards | Winery Parking | 1111 Dunaweal Lane, Calistoga | 38.5697 | -122.5472 |
| Napa / Oxbow Public Market | Park and Ride Lot | 1215 4th Street, Napa | 38.2964 | -122.2857 |

### Day 4 — Big Sur (Coastal Drive)

| Stop | Lot Name | Address | lat | lng |
|------|----------|---------|-----|-----|
| 17-Mile Drive | Pebble Beach Toll Gate (fee included in entry) | Del Monte Forest, CA | 36.5728 | -121.9487 |
| Carmel-by-the-Sea | Pine Inn Private Parking / AirGarage | 61 Lincoln St, Carmel | 36.5558 | -121.9243 |
| Point Lobos State Reserve | Point Lobos Parking Lot | Point Lobos, Carmel | 36.5155 | -121.9478 |
| Bixby Bridge | North Turnout (roadside) | CA-1, Big Sur | 36.3715 | -121.9019 |
| Pfeiffer Beach | Sycamore Canyon Rd Lot ($12 cash) | 9101 Sycamore Canyon Rd, Big Sur | 36.2381 | -121.8162 |
| McWay Falls | McWay Beach Parking Lot | Julia Pfeiffer Burns SP, Big Sur | 36.1589 | -121.6692 |
| Ragged Point | Ragged Point Inn Lot | 19019 CA-1, Ragged Point | 35.7806 | -121.3300 |
| Elephant Seals — Piedras Blancas | Roadside vista pullout | CA-1, San Simeon | 35.665 | -121.254 |

### Day 5 — Central Coast

| Stop | Lot Name | Address | lat | lng |
|------|----------|---------|-----|-----|
| Hearst Castle | Visitor Center Parking | 700 Hearst Castle Rd, San Simeon | 35.6505 | -121.1863 |
| Solvang | Municipal Parking | Solvang, CA | 34.5958 | -120.1376 |
| Santa Barbara | Lot 11 | 523 Anacapa St, Santa Barbara | 34.4176 | -119.6948 |

### Day 6 — Coastal Drive to San Diego

| Stop | Lot Name | Address | lat | lng |
|------|----------|---------|-----|-----|
| El Matador Beach (Malibu) | State Beach Parking Lot | 32350 PCH, Malibu | 34.0380 | -118.8747 |
| Newport Beach | Newport Visitor Parking | 3142 Villa Way, Newport Beach | 33.6158 | -117.9284 |
| Laguna Beach | Mermaid Lot | 348 Glenneyre St, Laguna Beach | 33.5427 | -117.7822 |
| La Jolla Cove | La Jolla Cove Lot | La Jolla, San Diego | 32.8504 | -117.2729 |
| Coronado Beach | Strand Way Parking | 1631 Strand Way, Coronado | 32.6788 | -117.1744 |

### Days 8–10 — Los Angeles

| Stop | Lot Name | Address | lat | lng |
|------|----------|---------|-----|-----|
| Beverly Hills / Rodeo Drive | Drivester / Public Lot | 9454 Wilshire Blvd, Beverly Hills | 34.0667 | -118.3985 |
| Hollywood / Walk of Fame | Hollywood & Vine Parking Lot | 1721 Vine St, Los Angeles | 34.1021 | -118.3270 |
| Downtown LA / Disney Concert Hall | Joe's Auto Parks | 215 S Broadway, Los Angeles | 34.0521 | -118.2476 |
| Griffith Observatory | Greek Theater Parking F | 2700 N Vermont Ave, Los Angeles | 34.1210 | -118.2965 |
| Venice Boardwalk | Venice Beach Lot | N Venice Blvd, Venice | 33.9857 | -118.4691 |
| Santa Monica Farmers Market | SP+ Parking | 1401 Ocean Ave, Santa Monica | 34.0141 | -118.4974 |
| Getty Center | Getty Center Parking Structure ($20/car) | 1200 Getty Center Dr, Los Angeles | 34.0878 | -118.4757 |

---

## Cost Estimation

~30 Nearby Search calls × $0.032/call = ~$0.96 total (well within $200 free tier)

## Notes

- Dollar pricing requires a separate data source (Parkopedia, SpotHero) — not implemented
- Lot links open `maps.google.com/search/?api=1&query={lat},{lng}` in new tab
- For roadside pullouts (Bixby Bridge, Elephant Seals) the "parking" coordinate IS the turnout
- Getty Center ($20/car flat rate) and Hearst Castle (included with tour) are the only known pricing
