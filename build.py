#!/usr/bin/env python3
"""
build.py — HTML Viewer Bundle Builder
Combines multiple HTML files into a single self-contained viewer.html

Features in output viewer:
  - Horizontal slide navigation (swipe, drag, arrow keys, buttons)
  - Lazy loading (current + neighbors only)
  - Fullscreen mode (F key or button)
  - Dark/light theme toggle (T key or button)
  - Page counter (e.g. 3 / 12)
  - Thumbnail strip (G key or button)
  - Google Translate integration (language switcher)
  - Local asset inlining (images, fonts, CSS → base64)

Run: python3 build.py
"""

import os
import sys
import json
import glob
import base64
import re
import pathlib
from datetime import datetime

# ════════════════════════════════════════════════════════════════
#  CONFIGURATION — Edit this section before running
# ════════════════════════════════════════════════════════════════

# ── File Discovery ───────────────────────────────────────────────
# Option A: Auto-discover
# Set AUTO_DISCOVER = True and point SOURCE_DIR to your folder.
# All .html files in the folder are included, sorted alphabetically.
# Alphabetical sort = order by filename, so name files 01-, 02-, etc.
# to control sequence.
AUTO_DISCOVER = False
SOURCE_DIR    = "./pages"           # folder containing your HTML files

# Option B: Manual list
# Set AUTO_DISCOVER = False and list files in the exact order you want.
# Paths are relative to this script file.
MANUAL_FILES = [
    "./pre-california-routes.html",
    "./segment-hv-to-kc.html",
    "./segment-kc-to-glacier.html",
    "./glacier-guide.html",
    "./yellowstone-guide.html",
    "./segment-ys-to-sf.html",
    "./logistics-guide.html",
]

# ── Output ───────────────────────────────────────────────────────
OUTPUT_FILE  = "./docs/index.html"    # where the bundled file is written

# ── Viewer Title ─────────────────────────────────────────────────
# Shown in the browser tab and in the top-left of the viewer.
VIEWER_TITLE = "Grand American Loop"

# ── Asset Inlining ───────────────────────────────────────────────
# Set True  → scan each HTML file for local images, fonts, CSS, JS
#             and replace them with base64 data URIs.
#             Use this when your HTML files reference local files
#             like ./img/hero.png or ./fonts/custom.woff2
# Set False → skip inlining. Use this when your HTML files are
#             already self-contained (CDN links, inline styles,
#             base64 already embedded, no local asset references).
INLINE_ASSETS = False

# ── Google Translate ─────────────────────────────────────────────
# Set True  → adds a language selector in the top bar that uses
#             the Google Translate widget to translate all slide
#             content into the chosen language.
# Set False → no translation UI shown.
ENABLE_TRANSLATE = True

# Languages shown in the translate dropdown.
# Format: ("Language Label", "google-translate-code")
# Full list of codes: https://cloud.google.com/translate/docs/languages
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
#  END OF CONFIGURATION
# ════════════════════════════════════════════════════════════════


# ── MIME type map for asset inlining ────────────────────────────
MIME_TYPES = {
    ".png":  "image/png",
    ".jpg":  "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif":  "image/gif",
    ".webp": "image/webp",
    ".svg":  "image/svg+xml",
    ".ico":  "image/x-icon",
    ".avif": "image/avif",
    ".woff": "font/woff",
    ".woff2":"font/woff2",
    ".ttf":  "font/ttf",
    ".otf":  "font/otf",
    ".css":  "text/css",
    ".js":   "application/javascript",
}


def resolve_files():
    """Return ordered list of HTML file paths based on config."""
    if AUTO_DISCOVER:
        pattern = os.path.join(SOURCE_DIR, "*.html")
        found = sorted(glob.glob(pattern))
        if not found:
            print(f"\n  ERROR: No .html files found in '{SOURCE_DIR}'")
            print(f"         Check that SOURCE_DIR is correct and the folder exists.\n")
            sys.exit(1)
        return found
    else:
        if not MANUAL_FILES:
            print("\n  ERROR: MANUAL_FILES is empty and AUTO_DISCOVER is False.")
            print("         Either set AUTO_DISCOVER = True or add files to MANUAL_FILES.\n")
            sys.exit(1)
        missing = [f for f in MANUAL_FILES if not os.path.exists(f)]
        if missing:
            print("\n  ERROR: The following files were not found:")
            for m in missing:
                print(f"         - {m}")
            print()
            sys.exit(1)
        return MANUAL_FILES


def inline_assets_in_html(html_content, html_path):
    """
    Scan an HTML file for local asset references and replace them
    with base64 data URIs so the file is fully self-contained.
    Handles: src="...", href="..." (CSS/fonts), url('...') in CSS.
    Skips:   http/https URLs, data URIs, empty refs, # anchors.
    """
    base_dir = os.path.dirname(os.path.abspath(html_path))
    replacements = 0
    skipped = 0

    patterns = [
        # src="path" or src='path'
        r'(src=["\'])(?!data:|https?://|//|#)([^"\']+)(["\'])',
        # href="path" for CSS/fonts only
        r'(href=["\'])(?!data:|https?://|//|#)([^"\']+\.(?:css|woff2?|ttf|otf))(["\'])',
        # url('path') or url("path") in inline CSS
        r'(url\(["\']?)(?!data:|https?://|//|#)([^"\')\s]+)(["\']?\))',
    ]

    def replace_ref(match, base_dir):
        nonlocal replacements, skipped
        full    = match.group(0)
        prefix  = match.group(1)
        raw_path = match.group(2)
        suffix  = match.group(3)

        asset_path = os.path.normpath(os.path.join(base_dir, raw_path))
        ext = pathlib.Path(asset_path).suffix.lower()

        if ext not in MIME_TYPES:
            skipped += 1
            return full
        if not os.path.exists(asset_path):
            print(f"    WARN: Asset not found, skipping: {raw_path}")
            skipped += 1
            return full

        mime = MIME_TYPES[ext]
        try:
            with open(asset_path, "rb") as f:
                data = base64.b64encode(f.read()).decode("ascii")
            data_uri = f"data:{mime};base64,{data}"
            replacements += 1
            if full.startswith('url('):
                return f"url({data_uri})"
            else:
                return f"{prefix}{data_uri}{suffix}"
        except Exception as e:
            print(f"    WARN: Could not read asset '{raw_path}': {e}")
            skipped += 1
            return full

    result = html_content
    for pattern in patterns:
        result = re.sub(pattern, lambda m: replace_ref(m, base_dir), result)

    return result, replacements, skipped


def build_translate_html(languages, enabled):
    """Return the translate button + dropdown HTML, or empty string."""
    if not enabled:
        return "", "", ""

    # Build language options for the dropdown
    options_html = "\n".join(
        f'          <div class="lang-option" data-lang="{code}" role="option" tabindex="0">{label}</div>'
        for label, code in languages
    )

    button_html = f"""
    <div class="divider-v"></div>
    <div class="translate-wrap" id="translateWrap">
      <button class="btn-nav translate-btn" id="btnTranslate" aria-label="Translate" aria-haspopup="listbox" aria-expanded="false" title="Translate (L)">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="flex-shrink:0"><path d="M5 8l6 6"/><path d="M4 14l6-6 2-4"/><path d="M2 5h12"/><path d="M7 2h1"/><path d="M22 22l-5-10-5 10"/><path d="M14 18h6"/></svg>
        <span id="langLabel">Translate</span>
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="flex-shrink:0"><path d="M6 9l6 6 6-6"/></svg>
      </button>
      <div class="lang-dropdown" id="langDropdown" role="listbox" aria-label="Select language">
{options_html}
      </div>
    </div>"""

    dropdown_css = """
.translate-wrap { position: relative; flex-shrink: 0; }
.translate-btn { min-width: 100px; justify-content: space-between; gap: var(--space-2); }
.lang-dropdown {
  display: none;
  position: absolute;
  top: calc(100% + 6px);
  right: 0;
  min-width: 160px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  z-index: 999;
  padding: var(--space-1);
  max-height: 260px;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: var(--color-divider) transparent;
}
.lang-dropdown.open { display: block; }
.lang-option {
  padding: var(--space-2) var(--space-3);
  font-size: var(--text-xs);
  color: var(--color-text-muted);
  cursor: pointer;
  border-radius: var(--radius-md);
  transition: background var(--transition), color var(--transition);
  white-space: nowrap;
}
.lang-option:hover { background: var(--color-surface-offset); color: var(--color-text); }
.lang-option.active { color: var(--color-primary); font-weight: 600; }
/* Hide the Google Translate toolbar that appears at top of page */
.goog-te-banner-frame, #goog-te-banner-frame { display: none !important; }
body { top: 0 !important; }
.goog-te-gadget { display: none !important; }
.skiptranslate { display: none !important; }
"""

    translate_js = f"""
// ── Google Translate ──────────────────────────────────────────
const LANGUAGES = {json.dumps(languages)};
let currentLang = 'en';

function applyTranslation(langCode) {{
  document.querySelectorAll('.slide iframe').forEach(function(f) {{
    try {{ f.contentWindow.postMessage({{type:'translate', lang:langCode}}, '*'); }} catch(e) {{}}
  }});
}}

function setLanguage(code, label) {{
  currentLang = code;
  document.getElementById('langLabel').textContent = label;
  document.querySelectorAll('.lang-option').forEach(el => {{
    el.classList.toggle('active', el.dataset.lang === code);
  }});
  applyTranslation(code);
  closeLangDropdown();
}}

function closeLangDropdown() {{
  document.getElementById('langDropdown').classList.remove('open');
  document.getElementById('btnTranslate').setAttribute('aria-expanded', 'false');
}}

document.getElementById('btnTranslate').addEventListener('click', (e) => {{
  e.stopPropagation();
  const dd = document.getElementById('langDropdown');
  const isOpen = dd.classList.toggle('open');
  document.getElementById('btnTranslate').setAttribute('aria-expanded', isOpen);
}});

document.querySelectorAll('.lang-option').forEach(el => {{
  el.addEventListener('click', () => {{
    const code = el.dataset.lang;
    const label = el.textContent.trim();
    setLanguage(code, label);
  }});
  el.addEventListener('keydown', e => {{
    if (e.key === 'Enter' || e.key === ' ') {{ e.preventDefault(); el.click(); }}
  }});
}});

document.addEventListener('click', (e) => {{
  if (!document.getElementById('translateWrap').contains(e.target)) {{
    closeLangDropdown();
  }}
}});

// Keyboard shortcut L
document.addEventListener('keydown', e => {{
  if ((e.key === 'l' || e.key === 'L') && !e.target.matches('input,textarea')) {{
    const dd = document.getElementById('langDropdown');
    const isOpen = dd.classList.toggle('open');
    document.getElementById('btnTranslate').setAttribute('aria-expanded', isOpen);
  }}
}});
"""

    return button_html, dropdown_css, translate_js


# ── Viewer HTML Template ─────────────────────────────────────────
def build_viewer_html(pages, labels, title, translate_button, translate_css, translate_js, enable_translate):
    if enable_translate:
        _inject = (
            '<style>.goog-te-banner-frame,.skiptranslate{display:none!important}'
            'body{top:0!important}.goog-te-gadget{display:none!important}</style>'
            '<div id="google_translate_element" style="display:none"></div>'
            '<script>'
            'function googleTranslateElementInit(){'
            'new google.translate.TranslateElement({pageLanguage:"en",autoDisplay:false},"google_translate_element");}'
            'window.addEventListener("message",function(e){'
            'if(e&&e.data&&e.data.type==="translate"){'
            'var lang=e.data.lang,tries=0;'
            'var t=setInterval(function(){'
            'var s=document.querySelector(".goog-te-combo");'
            'if(s){clearInterval(t);s.value=lang;s.dispatchEvent(new Event("change"));}'
            'else if(++tries>40){clearInterval(t);}},150);}});'
            '</script>'
            '<script src="//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script>'
        )
        pages = [
            p.replace('</body>', _inject + '</body>') if '</body>' in p else p + _inject
            for p in pages
        ]
    pages_json  = json.dumps(pages, ensure_ascii=False).replace('</script>', r'<\/script>').replace('</style>', r'<\/style>')
    labels_json = json.dumps(labels, ensure_ascii=False)

    translate_script_tag = ""

    return f"""<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist+Mono:wght@400;500&family=Geist:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
/* ── Design Tokens ── */
:root,[data-theme="light"]{{
  --color-bg:#f7f6f2;--color-surface:#f9f8f5;--color-surface-2:#fbfbf9;
  --color-surface-offset:#f3f0ec;--color-surface-dynamic:#e6e4df;
  --color-border:color-mix(in oklch,#28251d 12%,transparent);
  --color-divider:#dcd9d5;--color-text:#28251d;--color-text-muted:#7a7974;
  --color-text-faint:#bab9b4;--color-primary:#01696f;
  --color-primary-hover:#0c4e54;--color-primary-highlight:#cedcd8;
  --font-body:'Geist','Helvetica Neue',sans-serif;
  --font-mono:'Geist Mono','Fira Code',monospace;
  --text-xs:clamp(0.75rem,0.7rem + 0.25vw,0.875rem);
  --text-sm:clamp(0.875rem,0.8rem + 0.35vw,1rem);
  --text-base:clamp(1rem,0.95rem + 0.25vw,1.125rem);
  --space-1:0.25rem;--space-2:0.5rem;--space-3:0.75rem;--space-4:1rem;
  --space-6:1.5rem;--space-8:2rem;
  --radius-sm:0.375rem;--radius-md:0.5rem;--radius-lg:0.75rem;--radius-full:9999px;
  --shadow-sm:0 1px 2px oklch(0.2 0.01 80/0.06);
  --shadow-md:0 4px 12px oklch(0.2 0.01 80/0.10);
  --transition:180ms cubic-bezier(0.16,1,0.3,1);
}}
[data-theme="dark"]{{
  --color-bg:#171614;--color-surface:#1c1b19;--color-surface-2:#201f1d;
  --color-surface-offset:#1d1c1a;--color-surface-dynamic:#2d2c2a;
  --color-border:color-mix(in oklch,#cdccca 10%,transparent);
  --color-divider:#262523;--color-text:#cdccca;--color-text-muted:#797876;
  --color-text-faint:#5a5957;--color-primary:#4f98a3;
  --color-primary-hover:#227f8b;--color-primary-highlight:#313b3b;
  --shadow-sm:0 1px 2px oklch(0 0 0/0.2);
  --shadow-md:0 4px 12px oklch(0 0 0/0.32);
}}
@media(prefers-color-scheme:dark){{
  :root:not([data-theme]){{
    --color-bg:#171614;--color-surface:#1c1b19;--color-surface-2:#201f1d;
    --color-surface-offset:#1d1c1a;--color-surface-dynamic:#2d2c2a;
    --color-border:color-mix(in oklch,#cdccca 10%,transparent);
    --color-divider:#262523;--color-text:#cdccca;--color-text-muted:#797876;
    --color-text-faint:#5a5957;--color-primary:#4f98a3;
    --color-primary-hover:#227f8b;--color-primary-highlight:#313b3b;
    --shadow-sm:0 1px 2px oklch(0 0 0/0.2);
    --shadow-md:0 4px 12px oklch(0 0 0/0.32);
  }}
}}
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
html{{height:100%;-webkit-font-smoothing:antialiased}}
body{{height:100dvh;font-family:var(--font-body);font-size:var(--text-sm);color:var(--color-text);background:var(--color-bg);display:flex;flex-direction:column;overflow:hidden;user-select:none}}
/* ── Top Bar ── */
.topbar{{display:flex;align-items:center;gap:var(--space-3);padding:var(--space-2) var(--space-4);background:var(--color-surface);border-bottom:1px solid var(--color-border);box-shadow:var(--shadow-sm);z-index:100;flex-shrink:0;height:48px}}
.logo{{display:flex;align-items:center;gap:var(--space-2);color:var(--color-primary);font-weight:600;font-size:var(--text-sm);letter-spacing:-0.01em;flex-shrink:0}}
.divider-v{{width:1px;height:20px;background:var(--color-border);flex-shrink:0}}
.page-title{{flex:1;font-size:var(--text-sm);font-weight:500;color:var(--color-text);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0}}
.controls{{display:flex;align-items:center;gap:var(--space-2);flex-shrink:0}}
.btn-icon{{display:flex;align-items:center;justify-content:center;width:32px;height:32px;background:none;border:1px solid var(--color-border);border-radius:var(--radius-md);color:var(--color-text-muted);cursor:pointer;transition:color var(--transition),background var(--transition),border-color var(--transition);flex-shrink:0}}
.btn-icon:hover{{color:var(--color-text);background:var(--color-surface-offset)}}
.btn-icon:active{{transform:scale(0.95)}}
.btn-icon:disabled{{opacity:.35;cursor:default;pointer-events:none}}
.btn-nav{{display:flex;align-items:center;gap:var(--space-1);padding:0 var(--space-3);height:32px;background:none;border:1px solid var(--color-border);border-radius:var(--radius-md);color:var(--color-text-muted);cursor:pointer;font-family:var(--font-body);font-size:var(--text-xs);font-weight:500;white-space:nowrap;transition:color var(--transition),background var(--transition),border-color var(--transition)}}
.btn-nav:hover{{color:var(--color-text);background:var(--color-surface-offset)}}
.btn-nav:active{{transform:scale(0.97)}}
.btn-nav:disabled{{opacity:.35;cursor:default;pointer-events:none}}
.page-counter{{font-size:var(--text-xs);font-family:var(--font-mono);color:var(--color-text-muted);background:var(--color-surface-offset);border:1px solid var(--color-border);border-radius:var(--radius-md);padding:0 var(--space-3);height:32px;display:flex;align-items:center;gap:.2em;flex-shrink:0}}
.page-counter .cur{{color:var(--color-text);font-weight:600}}
/* ── Thumbnail Strip ── */
.strip-wrapper{{flex-shrink:0;background:var(--color-surface);border-bottom:1px solid var(--color-border);overflow:hidden;transition:height 300ms cubic-bezier(0.16,1,0.3,1);height:0}}
.strip-wrapper.open{{height:100px}}
.strip{{display:flex;align-items:center;gap:var(--space-2);padding:var(--space-2) var(--space-4);overflow-x:auto;height:100%;scrollbar-width:thin;scrollbar-color:var(--color-divider) transparent}}
.thumb{{flex-shrink:0;width:64px;height:80px;border:2px solid var(--color-border);border-radius:var(--radius-md);background:var(--color-surface-offset);cursor:pointer;overflow:hidden;position:relative;transition:border-color var(--transition),box-shadow var(--transition),transform var(--transition);display:flex;flex-direction:column}}
.thumb:hover{{border-color:var(--color-primary);transform:translateY(-2px);box-shadow:var(--shadow-md)}}
.thumb.active{{border-color:var(--color-primary);box-shadow:0 0 0 3px var(--color-primary-highlight)}}
.thumb-label{{font-size:9px;font-family:var(--font-mono);color:var(--color-text-muted);padding:2px 4px;background:var(--color-surface);border-top:1px solid var(--color-border);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;flex-shrink:0;margin-top:auto}}
.thumb-num{{position:absolute;top:3px;left:4px;font-size:9px;font-family:var(--font-mono);font-weight:600;color:var(--color-text-faint)}}
.thumb-preview{{flex:1;background:var(--color-surface-2);display:flex;align-items:center;justify-content:center}}
.thumb-preview svg{{opacity:.3}}
/* ── Viewport ── */
.viewport{{flex:1;overflow:hidden;position:relative}}
.slides-track{{display:flex;height:100%;width:100%;transition:transform 380ms cubic-bezier(0.16,1,0.3,1);will-change:transform}}
.slide{{flex-shrink:0;width:100%;height:100%;position:relative}}
.slide iframe{{width:100%;height:100%;border:none;display:block;background:white}}
.slide-loader{{position:absolute;inset:0;background:var(--color-bg);display:flex;align-items:center;justify-content:center;flex-direction:column;gap:var(--space-4);color:var(--color-text-muted);font-size:var(--text-sm);transition:opacity 300ms ease,visibility 300ms ease;z-index:5}}
.slide-loader.hidden{{opacity:0;visibility:hidden}}
.spinner{{width:28px;height:28px;border:2px solid var(--color-border);border-top-color:var(--color-primary);border-radius:50%;animation:spin .7s linear infinite}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
/* ── Swipe Hint ── */
.swipe-hint{{position:absolute;bottom:var(--space-6);left:50%;transform:translateX(-50%);background:color-mix(in oklch,var(--color-surface) 90%,transparent);backdrop-filter:blur(8px);border:1px solid var(--color-border);border-radius:var(--radius-full);padding:var(--space-2) var(--space-4);font-size:var(--text-xs);color:var(--color-text-muted);display:flex;align-items:center;gap:var(--space-2);pointer-events:none;animation:hint-fade 3s 1.5s both;z-index:10}}
@keyframes hint-fade{{0%{{opacity:0;transform:translateX(-50%) translateY(8px)}}20%{{opacity:1;transform:translateX(-50%) translateY(0)}}70%{{opacity:1}}100%{{opacity:0}}}}
/* ── Keyboard Shortcuts ── */
.shortcuts{{position:absolute;bottom:var(--space-4);right:var(--space-4);display:flex;align-items:center;gap:var(--space-2);opacity:0;pointer-events:none;transition:opacity var(--transition);z-index:10}}
.viewport:hover .shortcuts{{opacity:1}}
.key{{background:var(--color-surface);border:1px solid var(--color-border);border-radius:var(--radius-sm);padding:2px 6px;font-family:var(--font-mono);font-size:11px;color:var(--color-text-muted);box-shadow:0 1px 0 var(--color-border)}}
{translate_css}
/* ── Mobile ── */
@media(max-width:640px){{
  .topbar{{padding:var(--space-2) var(--space-3);gap:var(--space-2);height:52px;flex-wrap:nowrap}}
  .logo span{{display:none}}
  .page-title{{display:none}}
  .divider-v{{display:none}}
  .btn-icon{{width:40px;height:40px;border-radius:var(--radius-md)}}
  .btn-nav{{height:40px;padding:0 var(--space-2);font-size:.7rem}}
  .page-counter{{height:40px;padding:0 var(--space-2);font-size:.7rem}}
  .controls{{gap:var(--space-1)}}
  .lang-dropdown{{right:0;left:auto;min-width:150px}}
  .translate-btn span#langLabel{{display:none}}
  .translate-btn{{min-width:unset;padding:0 var(--space-2)}}
  .strip-wrapper.open{{height:88px}}
  .thumb{{width:56px;height:72px}}
  .shortcuts{{display:none}}
}}
</style>
</head>
<body>
<header class="topbar">
  <div class="logo">
    <svg width="20" height="20" viewBox="0 0 20 20" fill="none" aria-label="{title}">
      <rect x="2" y="2" width="6" height="8" rx="1" fill="currentColor" opacity="0.9"/>
      <rect x="2" y="12" width="6" height="6" rx="1" fill="currentColor" opacity="0.5"/>
      <rect x="10" y="2" width="8" height="5" rx="1" fill="currentColor" opacity="0.5"/>
      <rect x="10" y="9" width="8" height="9" rx="1" fill="currentColor" opacity="0.9"/>
    </svg>
    <span>{title}</span>
  </div>
  <div class="divider-v"></div>
  <div class="page-title" id="pageTitle">—</div>
  <div class="controls">
    <button class="btn-nav" id="btnPrev" disabled>
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M15 18l-6-6 6-6"/></svg>Prev
    </button>
    <div class="page-counter">
      <span class="cur" id="curPage">—</span>
      <span style="color:var(--color-text-faint)">/</span>
      <span id="totalPages">—</span>
    </div>
    <button class="btn-nav" id="btnNext" disabled>
      Next<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M9 18l6-6-6-6"/></svg>
    </button>
    <div class="divider-v"></div>
    <button class="btn-icon" id="btnStrip" title="Page strip (G)">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="4" height="18" rx="1"/><rect x="10" y="3" width="4" height="18" rx="1"/><rect x="17" y="3" width="4" height="18" rx="1"/></svg>
    </button>
    <button class="btn-icon" id="btnTheme" title="Theme (T)">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
    </button>
    <button class="btn-icon" id="btnFullscreen" title="Fullscreen (F)">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"/></svg>
    </button>
    {translate_button}
  </div>
</header>

<div class="strip-wrapper" id="stripWrapper">
  <div class="strip" id="strip"></div>
</div>

<div class="viewport" id="viewport">
  <div class="slides-track" id="track"></div>
  <div class="swipe-hint">
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
    Swipe or use arrow keys to navigate
  </div>
  <div class="shortcuts">
    <span class="key">←</span><span style="font-size:11px;color:var(--color-text-faint)">prev</span>
    <span class="key">→</span><span style="font-size:11px;color:var(--color-text-faint)">next</span>
    <span style="margin-left:6px" class="key">G</span><span style="font-size:11px;color:var(--color-text-faint)">strip</span>
    <span class="key">F</span><span style="font-size:11px;color:var(--color-text-faint)">fullscreen</span>
    {'<span class="key">L</span><span style="font-size:11px;color:var(--color-text-faint)">translate</span>' if enable_translate else ''}
  </div>
</div>

{translate_script_tag}

<script>
const PAGES  = {pages_json};
const LABELS = {labels_json};
let current = 0;
const track       = document.getElementById('track');
const strip       = document.getElementById('strip');
const stripWrapper= document.getElementById('stripWrapper');
const btnPrev     = document.getElementById('btnPrev');
const btnNext     = document.getElementById('btnNext');
const curPageEl   = document.getElementById('curPage');
const totalPagesEl= document.getElementById('totalPages');
const pageTitleEl = document.getElementById('pageTitle');

// ── Build slides + thumbnails ────────────────────────────────
function init() {{
  totalPagesEl.textContent = PAGES.length;
  PAGES.forEach((html, i) => {{
    // Slide
    const slide = document.createElement('div');
    slide.className = 'slide';
    const loader = document.createElement('div');
    loader.className = 'slide-loader';
    loader.innerHTML = '<div class="spinner"></div><span>Loading\u2026</span>';
    slide.appendChild(loader);
    const iframe = document.createElement('iframe');
    iframe.title = 'Slide ' + (i + 1);
    iframe.setAttribute('sandbox', 'allow-scripts allow-same-origin allow-forms allow-popups');
    if (i === 0) {{ iframe.srcdoc = html; iframe.onload = () => loader.classList.add('hidden'); }}
    slide.appendChild(iframe);
    track.appendChild(slide);

    // Thumbnail
    const thumb = document.createElement('div');
    thumb.className = 'thumb' + (i === 0 ? ' active' : '');
    thumb.setAttribute('role', 'button');
    thumb.setAttribute('tabindex', '0');
    thumb.setAttribute('aria-label', 'Go to slide ' + (i + 1) + ': ' + LABELS[i]);
    thumb.innerHTML = `<span class="thumb-num">${{i + 1}}</span>
      <div class="thumb-preview"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
        <rect x="3" y="3" width="18" height="18" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="3"/></svg></div>
      <div class="thumb-label">${{LABELS[i]}}</div>`;
    thumb.addEventListener('click', () => goTo(i));
    thumb.addEventListener('keydown', e => {{ if (e.key === 'Enter' || e.key === ' ') {{ e.preventDefault(); goTo(i); }} }});
    strip.appendChild(thumb);
  }});
  goTo(0, false);
}}

// ── Navigation ───────────────────────────────────────────────
function goTo(index, animate = true) {{
  if (index < 0 || index >= PAGES.length) return;
  current = index;
  if (!animate) track.style.transition = 'none';
  track.style.transform = `translateX(-${{current * 100}}%)`;
  if (!animate) requestAnimationFrame(() => {{ track.style.transition = ''; }});
  loadSlide(index); loadSlide(index + 1); loadSlide(index - 1);
  document.querySelectorAll('.thumb').forEach((t, i) => t.classList.toggle('active', i === current));
  const at = strip.children[current];
  if (at) at.scrollIntoView({{ behavior: 'smooth', block: 'nearest', inline: 'center' }});
  btnPrev.disabled = current === 0;
  btnNext.disabled = current === PAGES.length - 1;
  curPageEl.textContent  = current + 1;
  pageTitleEl.textContent = LABELS[current];
}}

function loadSlide(index) {{
  if (index < 0 || index >= PAGES.length) return;
  const slide  = track.querySelectorAll('.slide')[index];
  if (!slide) return;
  const iframe = slide.querySelector('iframe');
  const loader = slide.querySelector('.slide-loader');
  if (iframe && !iframe.srcdoc) {{
    iframe.srcdoc = PAGES[index];
    iframe.onload = () => loader && loader.classList.add('hidden');
  }}
}}

// ── Button handlers ──────────────────────────────────────────
btnPrev.addEventListener('click', () => goTo(current - 1));
btnNext.addEventListener('click', () => goTo(current + 1));

// ── Keyboard ─────────────────────────────────────────────────
document.addEventListener('keydown', e => {{
  if (document.activeElement && document.activeElement.tagName === 'IFRAME') return;
  switch (e.key) {{
    case 'ArrowRight': case 'ArrowDown': case 'PageDown':
      e.preventDefault(); goTo(current + 1); break;
    case 'ArrowLeft': case 'ArrowUp': case 'PageUp':
      e.preventDefault(); goTo(current - 1); break;
    case 'Home': e.preventDefault(); goTo(0); break;
    case 'End':  e.preventDefault(); goTo(PAGES.length - 1); break;
    case 'f': case 'F': toggleFullscreen(); break;
    case 'g': case 'G': toggleStrip(); break;
    case 't': case 'T': toggleTheme(); break;
  }}
}});

// ── Touch swipe ──────────────────────────────────────────────
let tX = 0, tY = 0, drag = false, dDelta = 0;
const vp = document.getElementById('viewport');
vp.addEventListener('touchstart', e => {{ tX = e.touches[0].clientX; tY = e.touches[0].clientY; drag = false; dDelta = 0; }}, {{ passive: true }});
vp.addEventListener('touchmove', e => {{
  const dx = e.touches[0].clientX - tX, dy = e.touches[0].clientY - tY;
  if (!drag && Math.abs(dx) > Math.abs(dy) && Math.abs(dx) > 8) drag = true;
  if (drag) {{ dDelta = dx; track.style.transition = 'none'; track.style.transform = `translateX(calc(${{-current * 100}}% + ${{(dDelta / vp.clientWidth) * 100}}%))`; }}
}}, {{ passive: true }});
vp.addEventListener('touchend', () => {{
  if (!drag) return;
  track.style.transition = '';
  const th = vp.clientWidth * 0.2;
  if (dDelta < -th) goTo(current + 1); else if (dDelta > th) goTo(current - 1); else goTo(current);
  drag = false; dDelta = 0;
}});

// ── Mouse drag ───────────────────────────────────────────────
let mX = 0, mDown = false, mDelta = 0;
vp.addEventListener('mousedown', e => {{ if (e.target.tagName === 'IFRAME') return; mDown = true; mX = e.clientX; mDelta = 0; vp.style.cursor = 'grabbing'; }});
window.addEventListener('mousemove', e => {{
  if (!mDown) return; mDelta = e.clientX - mX;
  if (Math.abs(mDelta) > 5) {{ track.style.transition = 'none'; track.style.transform = `translateX(calc(${{-current * 100}}% + ${{(mDelta / vp.clientWidth) * 100}}%))`; }}
}});
window.addEventListener('mouseup', () => {{
  if (!mDown) return; mDown = false; vp.style.cursor = '';
  if (Math.abs(mDelta) < 5) return;
  track.style.transition = '';
  const th = vp.clientWidth * 0.15;
  if (mDelta < -th) goTo(current + 1); else if (mDelta > th) goTo(current - 1); else goTo(current);
  mDelta = 0;
}});

// ── Strip toggle ─────────────────────────────────────────────
let stripOpen = false;
function toggleStrip() {{ stripOpen = !stripOpen; stripWrapper.classList.toggle('open', stripOpen); }}
document.getElementById('btnStrip').addEventListener('click', toggleStrip);

// ── Theme toggle ─────────────────────────────────────────────
let theme = document.documentElement.getAttribute('data-theme') || 'dark';
function toggleTheme() {{
  theme = theme === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', theme);
  const btn = document.getElementById('btnTheme');
  btn.innerHTML = theme === 'dark'
    ? '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>'
    : '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>';
}}
document.getElementById('btnTheme').addEventListener('click', toggleTheme);

// ── Fullscreen ───────────────────────────────────────────────
function toggleFullscreen() {{
  if (!document.fullscreenElement) document.documentElement.requestFullscreen().catch(() => {{}});
  else document.exitFullscreen().catch(() => {{}});
}}
document.getElementById('btnFullscreen').addEventListener('click', toggleFullscreen);

{translate_js}

init();
</script>
</body>
</html>"""


def build():
    print("\n" + "═"*58)
    print("  HTML Viewer — Build Script")
    print("═"*58)

    files = resolve_files()

    print(f"\n  Mode      : {'Auto-discover  →  ' + SOURCE_DIR if AUTO_DISCOVER else 'Manual list'}")
    print(f"  Files     : {len(files)} found")
    print(f"  Assets    : {'Inline local assets' if INLINE_ASSETS else 'Skip (assume self-contained)'}")
    print(f"  Translate : {'Enabled (' + str(len(TRANSLATE_LANGUAGES)) + ' languages)' if ENABLE_TRANSLATE else 'Disabled'}")
    print(f"  Output    : {OUTPUT_FILE}")
    print()

    for i, f in enumerate(files):
        print(f"    [{i+1:02d}] {f}")

    print()

    pages = []
    labels = []
    total_assets = 0

    for i, filepath in enumerate(files):
        label = pathlib.Path(filepath).stem
        labels.append(label)
        print(f"  Processing [{i+1}/{len(files)}]: {label}", end="", flush=True)

        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()

        if INLINE_ASSETS:
            content, inlined, skipped = inline_assets_in_html(content, filepath)
            total_assets += inlined
            note = f"  (+{inlined} assets" + (f", {skipped} skipped" if skipped else "") + ")"
            print(note)
        else:
            print()

        pages.append(content)

    translate_button, translate_css, translate_js = build_translate_html(
        TRANSLATE_LANGUAGES, ENABLE_TRANSLATE
    )

    output = build_viewer_html(
        pages, labels, VIEWER_TITLE,
        translate_button, translate_css, translate_js,
        ENABLE_TRANSLATE
    )

    out_path = pathlib.Path(OUTPUT_FILE)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(output, encoding="utf-8")

    size_kb = out_path.stat().st_size / 1024
    size_label = f"{size_kb:.1f} KB" if size_kb < 1024 else f"{size_kb / 1024:.2f} MB"

    print()
    print("─"*58)
    print(f"  \u2713 Built successfully!")
    print(f"  Output    : {out_path.resolve()}")
    print(f"  Size      : {size_label}")
    print(f"  Pages     : {len(pages)}")
    if INLINE_ASSETS:
        print(f"  Assets    : {total_assets} inlined")
    if ENABLE_TRANSLATE:
        print(f"  Translate : {len(TRANSLATE_LANGUAGES)} languages")
    print(f"  Time      : {datetime.now().strftime('%H:%M:%S')}")
    print("─"*58 + "\n")


if __name__ == "__main__":
    build()
