#!/usr/bin/env python3
"""
build_california.py — California Road Trip HTML Viewer Builder
Builds docs/california-viewer.html from the 6 California guide HTML files.

Google Maps API key is read from .env and injected into all {{GMAPS_KEY}}
placeholders in the HTML files before bundling. NEVER hardcode the key.

Run: python3 build_california.py
"""

import os
import sys
import pathlib
from datetime import datetime

# Add current directory to path so we can import shared functions from build.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import shared builder functions from build.py (does NOT execute build() —
# that is guarded by if __name__ == '__main__')
from build import build_viewer_html, build_translate_html

# ════════════════════════════════════════════════════════════════
#  CALIFORNIA CONFIGURATION
# ════════════════════════════════════════════════════════════════

MANUAL_FILES = [
    "./california/california-routes.html",
    "./california/sf-guide.html",
    "./california/bigsur-guide.html",
    "./california/centralcoast-guide.html",
    "./california/sandiego-guide.html",
    "./california/la-guide.html",
]

OUTPUT_FILE  = "./docs/california-viewer.html"

VIEWER_TITLE = "California Road Trip · San Francisco → Los Angeles · July 2026"

INLINE_ASSETS    = False   # All California guides are self-contained (CDN links, inline styles)
ENABLE_TRANSLATE = True    # Keep the 12-language translate widget

TRANSLATE_LANGUAGES = [
    ("English",    "en"),
    ("Spanish",    "es"),
    ("French",     "fr"),
    ("German",     "de"),
    ("Portuguese", "pt"),
    ("Italian",    "it"),
    ("Japanese",   "ja"),
    ("Korean",     "ko"),
    ("Chinese",    "zh-CN"),
    ("Arabic",     "ar"),
    ("Hindi",      "hi"),
    ("Russian",    "ru"),
]

# ════════════════════════════════════════════════════════════════
#  GOOGLE MAPS KEY READER
# Key is stored in .env as GOOGLE_MAPS_API_KEY — never hardcoded here
# ════════════════════════════════════════════════════════════════

def read_gmaps_key():
    """Read GOOGLE_MAPS_API_KEY from .env file. Returns empty string if not found."""
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    if not os.path.exists(env_path):
        return ""
    with open(env_path) as f:
        for line in f:
            stripped = line.strip()
            if stripped.startswith('GOOGLE_MAPS_API_KEY='):
                return stripped.split('=', 1)[1].strip()
    return ""


# ════════════════════════════════════════════════════════════════
#  BUILD
# ════════════════════════════════════════════════════════════════

def build():
    print()
    print("═" * 60)
    print("  California Road Trip — HTML Viewer Builder")
    print(f"  Output: {OUTPUT_FILE}")
    print("═" * 60)
    print()

    # ── Load Google Maps API key from .env ────────────────────────
    gmaps_key = read_gmaps_key()
    if gmaps_key:
        print("  ✓ GOOGLE_MAPS_API_KEY loaded from .env")
    else:
        print("  ⚠  GOOGLE_MAPS_API_KEY not found in .env")
        print("     Google Maps iframes will show an API error until the key is set.")
    print()

    # ── Verify all source files exist ─────────────────────────────
    files = []
    for entry in MANUAL_FILES:
        p = pathlib.Path(entry)
        if not p.exists():
            print(f"  ✗ Missing file: {entry}")
            print("    Run from the project root directory (same folder as build.py).")
            sys.exit(1)
        files.append(str(p))

    print(f"  Processing {len(files)} HTML files:")
    for i, f in enumerate(files):
        print(f"    [{i+1:02d}] {f}")
    print()

    # ── Read and pre-process each file ────────────────────────────
    pages  = []
    labels = []

    for i, filepath in enumerate(files):
        label = pathlib.Path(filepath).stem
        labels.append(label)
        print(f"  Reading [{i+1}/{len(files)}]: {label}", end="", flush=True)

        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()

        # Inject Google Maps API key — replace every {{GMAPS_KEY}} placeholder
        # These appear in iframe src="https://www.google.com/maps/embed/v1/...?key={{GMAPS_KEY}}&..."
        replaced = content.count("{{GMAPS_KEY}}")
        if replaced > 0 and gmaps_key:
            content = content.replace("{{GMAPS_KEY}}", gmaps_key)
            print(f"  (+{replaced} map embed{'s' if replaced != 1 else ''} keyed)")
        elif replaced > 0 and not gmaps_key:
            print(f"  (⚠ {replaced} map embed{'s' if replaced != 1 else ''} have no key)")
        else:
            print()

        pages.append(content)

    # ── Build translate HTML components ───────────────────────────
    translate_button, translate_css, translate_js = build_translate_html(
        TRANSLATE_LANGUAGES, ENABLE_TRANSLATE
    )

    # ── Build the viewer HTML ─────────────────────────────────────
    print()
    print("  Building viewer HTML (this may take a few seconds for large bundles)...")
    output = build_viewer_html(
        pages, labels, VIEWER_TITLE,
        translate_button, translate_css, translate_js,
        ENABLE_TRANSLATE
    )

    # ── Write output ──────────────────────────────────────────────
    out_path = pathlib.Path(OUTPUT_FILE)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(output, encoding="utf-8")

    size_kb   = out_path.stat().st_size / 1024
    size_label = f"{size_kb:.1f} KB" if size_kb < 1024 else f"{size_kb / 1024:.2f} MB"

    print()
    print("─" * 60)
    print(f"  ✓  Built successfully!")
    print(f"  Output     : {out_path.resolve()}")
    print(f"  Size       : {size_label}")
    print(f"  Slides     : {len(pages)}")
    print(f"  Translate  : {len(TRANSLATE_LANGUAGES)} languages")
    print(f"  Time       : {datetime.now().strftime('%H:%M:%S')}")
    print("─" * 60)
    print()
    print("  Next steps:")
    print("  1. Open docs/california-viewer.html in your browser to verify")
    print("  2. Check all 6 slides, all Google Maps iframes, all booking banners")
    print("  3. Push to GitHub:")
    print("     git add california-routes.html sf-guide.html bigsur-guide.html \\")
    print("            centralcoast-guide.html sandiego-guide.html la-guide.html \\")
    print("            build_california.py docs/california-viewer.html")
    print("     git commit -m 'Add California Road Trip guide'")
    print("     git push")
    print()
    print("  GitHub Pages URL (after push):")
    print("  https://AdamDrapkin.github.io/grand-american-loop/docs/california-viewer.html")
    print()


if __name__ == "__main__":
    build()
