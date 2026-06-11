#!/usr/bin/env python3
"""
inject_photos.py — Injects photo carousels into California guide HTML files.

Photos are pulled from Wikipedia article media lists (Wikipedia REST API,
no key required, images are curated and always on-topic).

Run from project root: python3 inject_photos.py

Rules:
  - Activities (booked or planned) get 3 photos.
  - Confirmed hotels get 3 photos.
  - Unconfirmed restaurants are excluded (never in the target list).
  - la-guide.html is excluded (pending revamp).
"""

import urllib.request
import urllib.parse
import json
import re
import time
import os

# ── CAROUSEL CSS ─────────────────────────────────────────────────────────────
CAROUSEL_CSS = """\
/* ── photo carousels ── */
.photo-carousel{position:relative;width:100%;height:220px;overflow:hidden;border-radius:8px;margin:10px 0 12px;background:#ccc}
.pc-track{display:flex;height:100%;transition:transform .35s ease}
.pc-track img{min-width:100%;height:220px;object-fit:cover;flex-shrink:0;user-select:none;pointer-events:none}
.pc-btn{position:absolute;top:50%;transform:translateY(-50%);background:rgba(0,0,0,.4);color:#fff;border:none;width:32px;height:32px;border-radius:50%;font-size:22px;line-height:1;cursor:pointer;z-index:2;display:flex;align-items:center;justify-content:center;padding:0}
.pc-btn:hover{background:rgba(0,0,0,.72)}
.pc-prev{left:7px}.pc-next{right:7px}
.pc-dots{position:absolute;bottom:7px;left:50%;transform:translateX(-50%);display:flex;gap:5px;z-index:2}
.pc-dot{width:7px;height:7px;border-radius:50%;background:rgba(255,255,255,.5);cursor:pointer;transition:background .2s}
.pc-dot.on{background:#fff}
"""

# ── CAROUSEL JS ───────────────────────────────────────────────────────────────
CAROUSEL_JS = """\
function pcStep(id,d){var e=document.getElementById(id),n=e.querySelectorAll('.pc-track img').length,c=+(e.dataset.c||0);pcGo(id,(c+d+n)%n)}
function pcGo(id,n){var e=document.getElementById(id);e.querySelector('.pc-track').style.transform='translateX(-'+n+'00%)';e.querySelectorAll('.pc-dot').forEach(function(d,i){d.classList.toggle('on',i===n)});e.dataset.c=n}
"""

# ── SKIP WORDS (for image file names) ─────────────────────────────────────────
SKIP = [
    "logo", "icon", "seal", "map", "flag", "coat", "shield", "badge",
    "symbol", "diagram", "chart", "graph", "portrait", "headshot",
    "emblem", "crest", "signature", "plaque", "stamp", "postcard",
    "plan", "layout", "aerial_view_map",
]

# ── TARGET LOCATIONS ──────────────────────────────────────────────────────────
# Key:      unique substring of the Google Maps href for that stop.
# "article" Wikipedia article name (used with the media-list REST endpoint).
# "fb"      Fallback article if primary has < 2 gallery images.
# "label"   Human-readable name (for progress output).

SF_TARGETS = {
    "Palace+of+Fine+Arts+San+Francisco": {
        "article": "Palace_of_Fine_Arts,_San_Francisco",
        "fb":      "Palace_of_Fine_Arts",
        "label":   "Palace of Fine Arts",
    },
    "Powell+and+Market+Cable+Car+Turnaround": {
        "article": "San_Francisco_cable_car_system",
        "fb":      "Powell-Hyde_Street_cable_car_line",
        "label":   "Powell-Hyde Cable Car",
    },
    "Twin+Peaks+San+Francisco+CA": {
        "article": "Twin_Peaks_(San_Francisco)",
        "fb":      "San_Francisco",
        "label":   "Twin Peaks",
    },
    "Pier+33+Alcatraz+Landing+San+Francisco": {
        "article": "Alcatraz_Island",
        "fb":      None,
        "label":   "Alcatraz",
    },
    "Fort+Point+National+Historic+Site+San+Francisco": {
        "article": "Fort_Point_National_Historic_Site",
        "fb":      "Fort_Point,_San_Francisco",
        "label":   "Fort Point NHS",
    },
    "Sather+Tower+UC+Berkeley+CA": {
        "article": "Sather_Tower",
        "fb":      "University_of_California,_Berkeley",
        "label":   "UC Berkeley / Campanile",
    },
    "Muir+Woods+National+Monument+Mill+Valley": {
        "article": "Muir_Woods_National_Monument",
        "fb":      None,
        "label":   "Muir Woods",
    },
    "1111+Dunaweal+Ln+Calistoga": {
        "article": "Sterling_Vineyards",
        "fb":      "Napa_Valley_wine_region",
        "label":   "Sterling Vineyards",
    },
    "50+Third+St+San+Francisco+CA+94103": {
        "article": "Hyatt_Regency_San_Francisco",
        "fb":      "Embarcadero_Center",
        "label":   "Hyatt Regency SF",
    },
}

BIGSUR_TARGETS = {
    "17+Mile+Drive+Pacific+Grove+CA": {
        "article": "17-Mile_Drive",
        "fb":      "Pebble_Beach,_California",
        "label":   "17-Mile Drive",
    },
    "Ocean+Avenue+Carmel+by+the+Sea+CA": {
        "article": "Carmel-by-the-Sea,_California",
        "fb":      None,
        "label":   "Carmel-by-the-Sea",
    },
    "Point+Lobos+State+Natural+Reserve+Carmel": {
        "article": "Point_Lobos_State_Natural_Reserve",
        "fb":      "Point_Lobos",
        "label":   "Point Lobos",
    },
    "Bixby+Creek+Bridge+Big+Sur+CA": {
        "article": "Bixby_Creek_Bridge",
        "fb":      "Big_Sur",
        "label":   "Bixby Creek Bridge",
    },
    "Hurricane+Point+Big+Sur+CA": {
        "article": "Big_Sur",    # No Wikipedia article for Hurricane Point itself
        "fb":      "California_State_Route_1",
        "label":   "Hurricane Point (Big Sur)",
    },
    "Pfeiffer+Beach+Big+Sur+CA": {
        "article": "Pfeiffer_Beach",
        "fb":      "Big_Sur",
        "label":   "Pfeiffer Beach",
    },
    "McWay+Falls+Julia+Pfeiffer+Burns+State+Park+Big+Sur": {
        "article": "McWay_Falls",
        "fb":      "Julia_Pfeiffer_Burns_State_Park",
        "label":   "McWay Falls",
    },
    "Piedras+Blancas+Elephant+Seal+Vista+Point+San+Simeon": {
        "article": "Northern_elephant_seal",
        "fb":      "Elephant_seal",
        "label":   "Elephant Seals",
    },
    "6620+Moonstone+Beach+Dr+Cambria+CA": {
        "article": "Cambria,_California",
        "fb":      "San_Luis_Obispo_County,_California",
        "label":   "Castle Inn / Moonstone Beach",
    },
}

CENTRALCOAST_TARGETS = {
    "750+Hearst+Castle+Rd+San+Simeon": {
        "article": "Hearst_Castle",
        "fb":      None,
        "label":   "Hearst Castle",
    },
    "Ostrichland+USA+610+E+Hwy+246+Solvang": {
        "article": "Solvang,_California",
        "fb":      None,
        "label":   "Solvang",
    },
    "Santa+Barbara+County+Courthouse+1100+Anacapa": {
        "article": "Santa_Barbara_County_Courthouse",
        "fb":      "Santa_Barbara,_California",
        "label":   "Santa Barbara Courthouse",
    },
    "Old+Mission+Santa+Barbara+2201+Laguna": {
        "article": "Mission_Santa_Barbara",
        "fb":      "Santa_Barbara,_California",
        "label":   "Old Mission Santa Barbara",
    },
    "El+Presidio+Santa+Barbara+123+E+Canon+Perdido": {
        "article": "Santa_Barbara_Presidio",
        "fb":      "Santa_Barbara,_California",
        "label":   "El Presidio",
    },
    "336+W+Cabrillo+Blvd+Santa+Barbara+CA+93101": {
        "article": "Santa_Barbara,_California",
        "fb":      None,
        "label":   "Beachside Inn / Santa Barbara",
    },
}

SANDIEGO_TARGETS = {
    "32215+Pacific+Coast+Hwy+Malibu+CA": {
        "article": "El_Matador_State_Beach",
        "fb":      "Malibu,_California",
        "label":   "El Matador Beach",
    },
    "Marine+Avenue+Balboa+Island+Newport+Beach": {
        "article": "Balboa_Island,_Newport_Beach",
        "fb":      "Newport_Beach,_California",
        "label":   "Balboa Island / Newport Beach",
    },
    "Heisler+Park+Laguna+Beach+CA": {
        "article": "Laguna_Beach,_California",
        "fb":      None,
        "label":   "Laguna Beach",
    },
    "275+Orange+Ave+Coronado+San+Diego+CA": {
        "article": "Coronado,_California",
        "fb":      "Hotel_del_Coronado",
        "label":   "Coronado Island",
    },
}

GUIDE_TARGETS = {
    "california/sf-guide.html":           SF_TARGETS,
    "california/bigsur-guide.html":       BIGSUR_TARGETS,
    "california/centralcoast-guide.html": CENTRALCOAST_TARGETS,
    "california/sandiego-guide.html":     SANDIEGO_TARGETS,
}


# ── PHOTO FETCHING ─────────────────────────────────────────────────────────────

def fetch_article_images(article, count=3):
    """
    Fetch up to `count` gallery images from a Wikipedia article's media list.
    Returns list of https:// URLs (largest srcset version).
    """
    url = f"https://en.wikipedia.org/api/rest_v1/page/media-list/{urllib.parse.quote(article)}"
    req = urllib.request.Request(url, headers={"User-Agent": "CaliforniaTripGuide/1.0 (personal travel guide)"})
    try:
        with urllib.request.urlopen(req, timeout=12) as r:
            data = json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None   # Article not found — caller should try fallback
        raise             # Re-raise 429 or other errors so caller can retry
    except Exception:
        return []

    items = data.get("items", [])
    photos = []
    for item in items:
        if item.get("type") != "image":
            continue
        if not item.get("showInGallery"):
            continue
        srcset = item.get("srcset")
        if not srcset:
            continue

        title_lower = item.get("title", "").lower()
        if any(s in title_lower for s in SKIP):
            continue

        # Pick largest available version from srcset
        src = srcset[-1]["src"]
        if src.startswith("//"):
            src = "https:" + src

        # Try to infer width from URL (e.g. "1280px-") and skip tiny images
        m = re.search(r"/(\d+)px-", src)
        if m and int(m.group(1)) < 400:
            continue

        photos.append(src)
        if len(photos) >= count:
            break

    return photos


def get_photos(article, fallback, count=3):
    """
    Try `article` first; fall back to `fallback` if primary has < 2 images.
    Returns a list of exactly `count` URLs (last URL repeated if needed).
    On 429, waits 90 s and retries once.
    """
    for attempt in (1, 2):
        try:
            photos = fetch_article_images(article, count)
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt == 1:
                print(" [rate-limited, waiting 90 s]", end="", flush=True)
                time.sleep(90)
                continue
            return []
        break

    # Try fallback if primary is None (404) or too few images
    if (photos is None or len(photos) < 2) and fallback:
        time.sleep(1.0)
        try:
            fb_photos = fetch_article_images(fallback, count)
            if fb_photos is not None and len(fb_photos) > len(photos or []):
                photos = fb_photos
        except Exception:
            pass

    if not photos:
        return []

    # Pad to count if fewer found
    while len(photos) < count:
        photos.append(photos[-1])
    return photos[:count]


# ── CAROUSEL BUILDER ──────────────────────────────────────────────────────────

_ctr = 0

def build_carousel(photos):
    global _ctr
    _ctr += 1
    cid   = f"pc{_ctr}"
    imgs  = "\n    ".join(f'<img src="{u}" loading="lazy" alt="photo {i+1}">' for i, u in enumerate(photos))
    dots  = "\n    ".join(f'<span class="pc-dot{" on" if i==0 else ""}" onclick="pcGo(\'{cid}\',{i})"></span>' for i in range(len(photos)))
    return (
        f'<div class="photo-carousel" id="{cid}" data-c="0">\n'
        f'  <div class="pc-track">\n'
        f'    {imgs}\n'
        f'  </div>\n'
        f'  <button class="pc-btn pc-prev" onclick="pcStep(\'{cid}\',-1)">&#8249;</button>\n'
        f'  <button class="pc-btn pc-next" onclick="pcStep(\'{cid}\',1)">&#8250;</button>\n'
        f'  <div class="pc-dots">\n'
        f'    {dots}\n'
        f'  </div>\n'
        f'</div>\n'
    )


# ── INJECTION ─────────────────────────────────────────────────────────────────

GUARD_WINDOW = 2000   # chars to look back for existing carousel

def already_injected(html, div_start):
    window = html[max(0, div_start - GUARD_WINDOW) : div_start]
    return "photo-carousel" in window


def inject_carousel(html, url_fragment, carousel_html):
    """
    Insert carousel_html immediately before the <div class="map-actions">
    that contains url_fragment. Returns (new_html, success).
    """
    pos = html.find(url_fragment)
    if pos == -1:
        return html, False

    marker    = '<div class="map-actions">'
    div_start = html.rfind(marker, 0, pos)
    if div_start == -1:
        return html, False

    if already_injected(html, div_start):
        return html, False   # already done — skip without counting as failure

    return html[:div_start] + carousel_html + html[div_start:], True


def process_guide(filepath, targets):
    print(f"\n  ── {filepath}")

    if not os.path.exists(filepath):
        print(f"     ✗ file not found")
        return

    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    injected = 0
    skipped  = 0

    for url_fragment, cfg in targets.items():
        label   = cfg["label"]
        article = cfg["article"]
        fb      = cfg["fb"]

        # Pre-check: skip API call if already injected
        pos = html.find(url_fragment)
        if pos != -1:
            marker    = '<div class="map-actions">'
            div_start = html.rfind(marker, 0, pos)
            if div_start != -1 and already_injected(html, div_start):
                print(f"     {label} … ⟳ already present")
                continue

        print(f"     {label} … ", end="", flush=True)
        photos = get_photos(article, fb, count=3)
        time.sleep(1.5)   # polite rate limiting

        if not photos:
            print("✗ no photos found")
            skipped += 1
            continue

        carousel_html      = build_carousel(photos)
        html, ok           = inject_carousel(html, url_fragment, carousel_html)

        if ok:
            print(f"✓")
            injected += 1
        else:
            print(f"⚠ anchor not found")
            skipped += 1

    if injected == 0:
        print(f"     (no new carousels written)")
        return

    # Add CSS once (guard against double-add)
    if "photo-carousel" not in (html[:html.index("</style>")] if "</style>" in html else ""):
        html = html.replace("</style>", CAROUSEL_CSS + "</style>", 1)

    # Add JS once
    if "function pcStep" not in html:
        html = html.replace("</body>", f"<script>\n{CAROUSEL_JS}</script>\n</body>", 1)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"     ✓ {injected} new carousels written ({skipped} skipped)")


# ── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    print()
    print("═" * 62)
    print("  California Trip — Photo Carousel Injector")
    print("  Source: Wikipedia article media lists (no API key)")
    print("═" * 62)

    for filepath, targets in GUIDE_TARGETS.items():
        process_guide(filepath, targets)

    print()
    print("─" * 62)
    print("  Done. Run:  python3 build_california.py  to rebuild viewer.")
    print("─" * 62)
    print()


if __name__ == "__main__":
    main()
