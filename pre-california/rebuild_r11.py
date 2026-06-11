#!/usr/bin/env python3
"""
Rebuild pre-california-routes.html:
 - Strip Routes 1-10 HTML cards + JS data
 - Rebuild Route 11: verified 18-day itinerary (Jun 15 → Jul 2)
 - Add dest/rest/shower/food pins for new route
 - Update hero, day grid, stats, path chips, tags, states
 - Update Google Maps open link
"""
import re

HTML_PATH = '/Users/adamdrapkin/California Trip/pre-california-routes.html'

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    html = f.read()
print(f'Original: {len(html):,} bytes')

# ── ADD dest CSS after existing food CSS ─────────────────────────────────────
OLD_FOOD_CSS = "    .map-layer-btn.active.food { background: #c05621; color: white; }"
NEW_FOOD_CSS  = """    .map-layer-btn.active.food { background: #c05621; color: white; }
    .map-layer-btn.dest { border-color: #6B46C1; color: #6B46C1; }
    .map-layer-btn.active.dest { background: #6B46C1; color: white; }"""
html = html.replace(OLD_FOOD_CSS, NEW_FOOD_CSS, 1)

# ── HERO ─────────────────────────────────────────────────────────────────────
OLD_HERO = '''<div class="hero">
  <h1>🗺️ Pre-California Route Explorer</h1>
  <p class="sub">June 22 → July 2, 2026 &nbsp;·&nbsp; 11 Days &nbsp;·&nbsp; Huntington Valley, PA → San Francisco, CA</p>
  <p class="meta">Google Maps Distance Matrix Validated · No Chicago · Yellowstone Non-Negotiable (2 Days)</p>
  <div class="badges">
    <span class="hero-badge">⛺ Car camping &amp; truck stops</span>
    <span class="hero-badge">🌋 Yellowstone required</span>
    <span class="hero-badge">🏔️ Utah · Colorado · Oregon · Washington</span>
    <span class="hero-badge">🕛 Arrive SF by noon July 2</span>
  </div>
</div>'''

NEW_HERO = '''<div class="hero">
  <h1>🗺️ The Grand American Loop</h1>
  <p class="sub">June 15 → July 2, 2026 &nbsp;·&nbsp; 18 Days &nbsp;·&nbsp; Huntington Valley, PA → San Francisco, CA</p>
  <p class="meta">All drive times Google Maps verified &nbsp;·&nbsp; Two drivers &nbsp;·&nbsp; ~5,854 miles &nbsp;·&nbsp; 12 states</p>
  <div class="badges">
    <span class="hero-badge">⛺ Glacier NP · Jun 22–25 CONFIRMED</span>
    <span class="hero-badge">🌋 Yellowstone · Jun 25–28 CONFIRMED</span>
    <span class="hero-badge">⬜ Bonneville Salt Flats</span>
    <span class="hero-badge">🌊 Twin Falls · Shoshone Falls</span>
    <span class="hero-badge">🕛 Arrive SF Jul 2 by 11am</span>
  </div>
</div>'''

html = html.replace(OLD_HERO, NEW_HERO, 1)

# ── ROUTES SECTION — replace entire inner content ────────────────────────────
NEW_ROUTES_INNER = '''
  <div class="wrap">

    <h2 class="sec-title">Route 11 — The Grand American Loop</h2>
    <p class="sec-sub">18 days · 12 states · 6 NPS sites · ~5,854 miles · every leg Google Maps verified</p>

    <div class="confirm-note">
      🔒 <strong>CONFIRMED RESERVATIONS:</strong>
      &nbsp;Johnson&#39;s of St. Mary, MT (Jun 22–25)
      &nbsp;·&nbsp; Canyon Campground, Yellowstone (Jun 25–27 + Jun 27–28 · two tent sites)
      &nbsp;·&nbsp; Depart Jun 15 · Arrive SF Jul 2 by 11am
    </div>

    <!-- ═══ ROUTE 11 ═══ -->
    <div class="route-card" style="border:2px solid var(--gold);box-shadow:0 6px 40px rgba(214,158,46,.22);">
      <div class="route-header" style="background:linear-gradient(135deg,#fffdf5 0%,#fff9e6 100%);">
        <div>
          <div class="r11-badge">⭐ Your Custom Route · Departs Jun 15 · Arrives SF Jul 2</div>
          <div class="route-num" style="color:var(--gold);">Route 11 of 11</div>
          <div class="route-title" style="color:#78350f;">🌟 The Grand American Loop</div>
          <div class="route-tag">18 days · 12 states · 6 National Parks · ~5,854 miles · avg 450 mi/day (two drivers)</div>
        </div>
        <div class="stats">
          <div class="stat"><span class="stat-val" style="color:#92400e;">5,854</span><span class="stat-lbl">Total Miles</span></div>
          <div class="stat"><span class="stat-val" style="color:#92400e;">18</span><span class="stat-lbl">Days</span></div>
          <div class="stat"><span class="stat-val" style="color:#92400e;">12</span><span class="stat-lbl">States</span></div>
          <div class="stat"><span class="stat-val" style="color:#92400e;">6</span><span class="stat-lbl">NPS Sites</span></div>
        </div>
      </div>
      <div class="route-body">
        <div class="route-info">
          <div class="path">
            <span class="sc">HV, PA</span><span class="sa">→</span>
            <span class="sc hi">⛰️ Pittsburgh</span><span class="sa">→</span>
            <span class="sc">Dayton, OH</span><span class="sa">→</span>
            <span class="sc">Indianapolis, IN</span><span class="sa">→</span>
            <span class="sc hi">⛵ Gateway Arch · STL</span><span class="sa">→</span>
            <span class="sc hi">💦 Johnson&#39;s Shut-Ins</span><span class="sa">→</span>
            <span class="sc hi">🗿 Meramec Caverns</span><span class="sa">→</span>
            <span class="sc hi">🛣️ Springfield Route 66</span><span class="sa">→</span>
            <span class="sc hi">🍖 Kansas City</span><span class="sa">→</span>
            <span class="sc or">Nebraska · I-80</span><span class="sa">→</span>
            <span class="sc">Rock Springs, WY</span><span class="sa">→</span>
            <span class="sc hi">🌡️ Homestead Crater, UT</span><span class="sa">→</span>
            <span class="sc hi">🏙️ Salt Lake City</span><span class="sa">→</span>
            <span class="sc hi">⬜ Bonneville Salt Flats</span><span class="sa">→</span>
            <span class="sc hi">🌊 Twin Falls · Shoshone Falls</span><span class="sa">→</span>
            <span class="sc hi">🦬 Bison Range</span><span class="sa">→</span>
            <span class="sc hi">🏞️ Polson · Flathead Lake</span><span class="sa">→</span>
            <span class="sc hi">🏔️ Whitefish</span><span class="sa">→</span>
            <span class="sc ys">🏔️ Glacier NP ×3 (CONFIRMED)</span><span class="sa">→</span>
            <span class="sc ys">🌋 Yellowstone ×3 (CONFIRMED)</span><span class="sa">→</span>
            <span class="sc hi">Mt. Rainier NP</span><span class="sa">→</span>
            <span class="sc hi">🌆 Seattle</span><span class="sa">→</span>
            <span class="sc hi">🌹 Portland</span><span class="sa">→</span>
            <span class="sc hi">🔵 Crater Lake</span><span class="sa">→</span>
            <span class="sc hi">🌲 Redwoods</span><span class="sa">→</span>
            <span class="sc ys">San Francisco ✓</span>
          </div>

          <div class="day-grid">

            <div class="day-entry" onclick="toggleDay(this)">
              <div class="day-row"><span class="dn">Jun 15</span><span class="dr">Huntington Valley, PA → Pittsburgh (stop) → Dayton, OH</span><span class="dd">8h 49m · 563 mi</span><span class="di">▼</span></div>
              <div class="day-panel"><p class="panel-loading">📍 Details loading…</p></div>
            </div>

            <div class="day-entry" onclick="toggleDay(this)">
              <div class="day-row"><span class="dn">Jun 16</span><span class="dr">Dayton → ⭐ Indianapolis (Shapiro&#39;s Deli) → ⛵ St. Louis, MO (Gateway Arch)</span><span class="dd">5h 36m · 359 mi</span><span class="di">▼</span></div>
              <div class="day-panel"><p class="panel-loading">📍 Details loading…</p></div>
            </div>

            <div class="day-entry" onclick="toggleDay(this)">
              <div class="day-row"><span class="dn">Jun 17</span><span class="dr">St. Louis → 💦 Johnson&#39;s Shut-Ins → 🗿 Meramec Caverns → 🛣️ Springfield, MO</span><span class="dd">5h 51m · 334 mi</span><span class="di">▼</span></div>
              <div class="day-panel"><p class="panel-loading">📍 Details loading…</p></div>
            </div>

            <div class="day-entry" onclick="toggleDay(this)">
              <div class="day-row"><span class="dn">Jun 18</span><span class="dr">🛣️ Springfield (Route 66 birthplace) → 🍖 Kansas City, MO</span><span class="dd">2h 42m · 170 mi</span><span class="di">▼</span></div>
              <div class="day-panel"><p class="panel-loading">📍 Details loading…</p></div>
            </div>

            <div class="day-entry" onclick="toggleDay(this)">
              <div class="day-row"><span class="dn">Jun 19</span><span class="dr">Kansas City → Nebraska I-80 → Rock Springs, WY ⚡ above Colorado</span><span class="dd">13h 47m · 938 mi</span><span class="di">▼</span></div>
              <div class="day-panel"><p class="panel-loading">📍 Details loading…</p></div>
            </div>

            <div class="day-entry" onclick="toggleDay(this)">
              <div class="day-row"><span class="dn">Jun 20</span><span class="dr">Rock Springs → 🌡️ Homestead Crater (Midway) → 🏙️ SLC → ⬜ Bonneville Salt Flats → 🌊 Twin Falls, ID</span><span class="dd">~10h · ~566 mi</span><span class="di">▼</span></div>
              <div class="day-panel"><p class="panel-loading">📍 Details loading…</p></div>
            </div>

            <div class="day-entry" onclick="toggleDay(this)">
              <div class="day-row"><span class="dn">Jun 21</span><span class="dr">Twin Falls + 🌊 Shoshone Falls → Salmon River Canyon → 🦬 Bison Range → 🏞️ Polson → 🏔️ Whitefish, MT</span><span class="dd">9h 13m · ~580 mi</span><span class="di">▼</span></div>
              <div class="day-panel"><p class="panel-loading">📍 Details loading…</p></div>
            </div>

            <div class="day-entry" onclick="toggleDay(this)">
              <div class="day-row"><span class="dn">Jun 22</span><span class="dr">🏔️ Whitefish → St. Mary · CHECK-IN Johnson&#39;s · Glacier NP Day 1</span><span class="dd">2h 12m · 111 mi ✅</span><span class="di">▼</span></div>
              <div class="day-panel"><p class="panel-loading">📍 Details loading…</p></div>
            </div>

            <div class="day-entry" onclick="toggleDay(this)">
              <div class="day-row"><span class="dn">Jun 23</span><span class="dr">🏔️ Glacier NP Day 2 — Going-to-the-Sun Road · Logan Pass · Hidden Lake</span><span class="dd">~100 mi · park day ✅</span><span class="di">▼</span></div>
              <div class="day-panel"><p class="panel-loading">📍 Details loading…</p></div>
            </div>

            <div class="day-entry" onclick="toggleDay(this)">
              <div class="day-row"><span class="dn">Jun 24</span><span class="dr">🏔️ Glacier NP Day 3 — Many Glacier Valley · Grinnell Glacier hike</span><span class="dd">~50 mi · park day ✅</span><span class="di">▼</span></div>
              <div class="day-panel"><p class="panel-loading">📍 Details loading…</p></div>
            </div>

            <div class="day-entry" onclick="toggleDay(this)">
              <div class="day-row"><span class="dn">Jun 25</span><span class="dr">St. Mary (checkout 11am) → 🌋 Canyon Village, Yellowstone NP (check-in 1pm)</span><span class="dd">6h 53m · 412 mi ✅</span><span class="di">▼</span></div>
              <div class="day-panel"><p class="panel-loading">📍 Details loading…</p></div>
            </div>

            <div class="day-entry" onclick="toggleDay(this)">
              <div class="day-row"><span class="dn">Jun 26</span><span class="dr">🌋 Yellowstone Day 2 — Grand Prismatic Spring · Old Faithful · Grand Canyon of Yellowstone</span><span class="dd">park day ✅</span><span class="di">▼</span></div>
              <div class="day-panel"><p class="panel-loading">📍 Details loading…</p></div>
            </div>

            <div class="day-entry" onclick="toggleDay(this)">
              <div class="day-row"><span class="dn">Jun 27</span><span class="dr">🌋 Yellowstone Day 3 — switch Res. 1→2 · Lamar Valley wildlife</span><span class="dd">park day ✅</span><span class="di">▼</span></div>
              <div class="day-panel"><p class="panel-loading">📍 Details loading…</p></div>
            </div>

            <div class="day-entry" onclick="toggleDay(this)">
              <div class="day-row"><span class="dn">Jun 28</span><span class="dr">Canyon Village (checkout 11am) → Spokane, WA ⚡</span><span class="dd">8h 7m · 500 mi</span><span class="di">▼</span></div>
              <div class="day-panel"><p class="panel-loading">📍 Details loading…</p></div>
            </div>

            <div class="day-entry" onclick="toggleDay(this)">
              <div class="day-row"><span class="dn">Jun 29</span><span class="dr">Spokane → 🌋 Mt. Rainier NP (Paradise) → Seattle, WA</span><span class="dd">7h 29m · 395 mi</span><span class="di">▼</span></div>
              <div class="day-panel"><p class="panel-loading">📍 Details loading…</p></div>
            </div>

            <div class="day-entry" onclick="toggleDay(this)">
              <div class="day-row"><span class="dn">Jun 30</span><span class="dr">Seattle → 🌹 Portland, OR → 🔵 Crater Lake NP</span><span class="dd">6h 38m · 407 mi</span><span class="di">▼</span></div>
              <div class="day-panel"><p class="panel-loading">📍 Details loading…</p></div>
            </div>

            <div class="day-entry" onclick="toggleDay(this)">
              <div class="day-row"><span class="dn">Jul 1</span><span class="dr">Crater Lake → 🌲 Jedediah Smith Redwoods → San Francisco, CA ✅</span><span class="dd">9h 27m · 519 mi</span><span class="di">▼</span></div>
              <div class="day-panel"><p class="panel-loading">📍 Details loading…</p></div>
            </div>

            <div class="day-entry" onclick="toggleDay(this)">
              <div class="day-row"><span class="dn">Jul 2</span><span class="dr">San Francisco — arrive by 11am · California road trip begins 🌉</span><span class="dd">✅ DESTINATION REACHED</span><span class="di">▼</span></div>
              <div class="day-panel"><p class="panel-loading">📍 Details loading…</p></div>
            </div>

          </div>

          <div class="tags">
            <span class="t t-city">⛰️ Pittsburgh, PA</span>
            <span class="t t-city">⛵ Gateway Arch · St. Louis</span>
            <span class="t t-scen">💦 Johnson&#39;s Shut-Ins</span>
            <span class="t t-scen">🗿 Meramec Caverns</span>
            <span class="t t-r11">🛣️ Route 66 Birthplace · Springfield</span>
            <span class="t t-city">🍖 Kansas City BBQ</span>
            <span class="t t-scen">🌡️ Homestead Crater · Midway UT</span>
            <span class="t t-city">🏙️ Salt Lake City</span>
            <span class="t t-scen">⬜ Bonneville Salt Flats</span>
            <span class="t t-scen">🌊 Twin Falls · Shoshone Falls</span>
            <span class="t t-scen">🦬 National Bison Range</span>
            <span class="t t-scen">🏞️ Flathead Lake · Polson</span>
            <span class="t t-park">🏔️ Glacier NP ×3 days (CONFIRMED)</span>
            <span class="t t-park">🌋 Yellowstone NP ×3 days (CONFIRMED)</span>
            <span class="t t-park">🌋 Mt. Rainier NP</span>
            <span class="t t-city">🌆 Seattle, WA</span>
            <span class="t t-city">🌹 Portland, OR</span>
            <span class="t t-park">🔵 Crater Lake NP</span>
            <span class="t t-park">🌲 Redwood NP</span>
            <span class="t t-warn">⚡ Hard days: Jun 19 (KC→Rock Springs 938 mi) · Jun 28 (Yellowstone→Spokane 500 mi)</span>
          </div>

          <div class="states">
            <span class="stag">PA</span><span class="stag">OH</span><span class="stag">IN</span><span class="stag">MO</span><span class="stag">NE</span><span class="stag">WY</span><span class="stag">UT</span><span class="stag">ID</span><span class="stag">MT</span><span class="stag">WA</span><span class="stag">OR</span><span class="stag">CA</span>
          </div>

          <div class="diff" style="border-top:1px solid var(--border);padding-top:12px;margin-top:12px;">
            Drive difficulty: Two-driver manageable — 6 easy days under 400 mi, 2 hard push days (Jun 19 + Jun 28), avg 450 mi/day with partner swaps.
            <div class="bar-track"><div class="bar-fill d3" style="width:65%"></div></div>
          </div>
        </div>

        <div class="route-map">
          <div class="map-controls" style="background:linear-gradient(135deg,#fffdf5,#fff9e6);">
            <span class="map-ctrl-label" style="color:var(--gold);">🌟 Route 11</span>
            <button class="map-layer-btn dest active" onclick="toggleLayer(\'r11\',\'dest\',this)">📍 Destinations</button>
            <button class="map-layer-btn rest active" onclick="toggleLayer(\'r11\',\'rest\',this)">🛌 Rest Stops</button>
            <button class="map-layer-btn shower active" onclick="toggleLayer(\'r11\',\'shower\',this)">🚿 Showers</button>
            <button class="map-layer-btn food active" onclick="toggleLayer(\'r11\',\'food\',this)">🍳 Food</button>
          </div>
          <div id="r11-map-canvas" class="map-canvas"><div class="map-loading">Loading map…</div></div>
          <a class="map-open-btn" href="https://www.google.com/maps/dir/Huntington+Valley,PA/Pittsburgh,PA/Dayton,OH/Indianapolis,IN/St.+Louis,MO/Johnson\'s+Shut-Ins+State+Park,MO/Meramec+Caverns,MO/Springfield,MO/Kansas+City,MO/Rock+Springs,WY/Midway,UT/Salt+Lake+City,UT/Wendover,UT/Twin+Falls,ID/National+Bison+Range,Moiese,MT/Polson,MT/Whitefish,MT/St.+Mary,MT/Canyon+Village,Yellowstone,WY/Spokane,WA/Mount+Rainier+National+Park,WA/Seattle,WA/Portland,OR/Crater+Lake+National+Park,OR/Crescent+City,CA/San+Francisco,CA" target="_blank">🗺️ Open Route 11 in Google Maps ↗</a>
        </div>
      </div>
    </div><!-- /route 11 -->

'''

# Replace the entire routes-section inner content
old_routes_pattern = re.compile(
    r'(<div class="routes-section">)([\s\S]*?)(</div><!-- /routes-section -->)',
    re.DOTALL
)
match = old_routes_pattern.search(html)
if match:
    html = html[:match.start()] + '<div class="routes-section">' + NEW_ROUTES_INNER + '</div><!-- /routes-section -->' + html[match.end():]
    print('  ✓ Routes section replaced (routes 1-10 removed, Route 11 rebuilt)')
else:
    print('  ✗ Routes section not found')

# ── NEW JAVASCRIPT ────────────────────────────────────────────────────────────
NEW_JS = r"""<script>
// ── Day card expand/collapse ───────────────────────────────────────────
function toggleDay(el) { el.classList.toggle('open'); }

// ── Interactive map layer data ────────────────────────────────────────
const ROUTE_STOPS = {
  r11: {
    origin: 'Huntington Valley, PA',
    destination: 'San Francisco, CA',
    waypoints: [
      'Pittsburgh, PA','Dayton, OH','Indianapolis, IN','St. Louis, MO',
      "Johnson's Shut-Ins State Park, MO",'Springfield, MO','Kansas City, MO',
      'Rock Springs, WY','Midway, UT','Salt Lake City, UT','Wendover, UT',
      'Twin Falls, ID','National Bison Range, Moiese, MT','Polson, MT',
      'Whitefish, MT','St. Mary, MT',
      'Canyon Village, Yellowstone National Park, WY',
      'Spokane, WA','Paradise, Mt. Rainier National Park, WA','Seattle, WA',
      'Portland, OR','Crater Lake National Park, OR','Crescent City, CA'
    ],
    stops: {
      dest: [
        /* ── Pennsylvania ── */
        {n:'Mount Washington Overlook — Pittsburgh', lat:40.427, lng:-80.013, note:'Best Pittsburgh skyline view · Duquesne Incline · overlooks all three rivers'},
        /* ── Ohio ── */
        {n:'Dayton Aviation Heritage NHP',          lat:39.771, lng:-84.194, note:'Wright Brothers museum · free NPS site · great 30-min stop'},
        /* ── Indiana ── */
        {n:"Shapiro's Delicatessen — Indianapolis", lat:39.762, lng:-86.151, note:'Legendary deli since 1905 · massive portions · lunch stop on Day 2'},
        /* ── Missouri ── */
        {n:'Gateway Arch NP — St. Louis',          lat:38.625, lng:-90.185, note:'630 ft tall · ride to the top · views of the Mississippi River'},
        {n:"Johnson's Shut-Ins — Lesterville, MO", lat:37.569, lng:-90.843, note:'Nature-made water park in granite gorge · swim! · best swimming hole in MO'},
        {n:'Meramec Caverns — Stanton, MO',        lat:38.215, lng:-91.057, note:'Jesse James hideout · Route 66 landmark · 5-level cavern system'},
        {n:'Route 66 Birthplace — Springfield, MO',lat:37.209, lng:-93.292, note:"Named here in 1926 · Lambert's Throwed Rolls nearby · Route 66 centennial 2026"},
        {n:"Joe's Kansas City Bar-B-Que — KC",     lat:38.979, lng:-94.609, note:'Inside a gas station · get the Z-Man sandwich · BBQ royalty'},
        /* ── Utah ── */
        {n:'Homestead Crater — Midway, UT',        lat:40.514, lng:-111.498, note:'95°F geothermal hot spring inside 55-ft volcanic dome · book swim time in advance'},
        {n:'Temple Square — Salt Lake City, UT',   lat:40.771, lng:-111.891, note:'Historic LDS temple · free outdoor grounds · city center landmark'},
        {n:'Bonneville Salt Flats — Wendover, UT', lat:40.762, lng:-113.889, note:'Drive onto the salt · 30,000 acres of white · land speed record site'},
        /* ── Idaho ── */
        {n:'Shoshone Falls — Twin Falls, ID',      lat:42.590, lng:-114.369, note:'212 ft · taller than Niagara Falls · Snake River Canyon · short walk from parking'},
        /* ── Montana ── */
        {n:'National Bison Range — Moiese, MT',    lat:47.351, lng:-114.075, note:'Wildlife drive through 18,800 acres · 350+ bison · natural pass-through on US-93'},
        {n:'Flathead Lake — Polson, MT',           lat:47.694, lng:-114.159, note:'Largest freshwater lake west of Mississippi · West Shore State Park access'},
        {n:'Whitefish, MT',                        lat:48.412, lng:-114.338, note:'Mountain town overnight · best base before Glacier · MT Coffee Traders morning coffee'},
        {n:'Glacier NP — Lake McDonald',           lat:48.565, lng:-113.881, note:'10-mile turquoise lake · old-growth cedar and hemlock · perfect first Glacier view'},
        {n:'Glacier NP — Logan Pass (GTTS Road)',  lat:48.696, lng:-113.718, note:'6,646 ft · Going-to-the-Sun Road summit · mountain goats · Hidden Lake Overlook trail'},
        {n:'Glacier NP — Many Glacier Valley',     lat:48.797, lng:-113.657, note:'East side · most wildlife density · Grinnell Glacier hike · Swiftcurrent Lake'},
        /* ── Wyoming (Yellowstone) ── */
        {n:'Canyon Village — Yellowstone NP',      lat:44.726, lng:-110.501, note:'CONFIRMED CAMPSITE Jun 25-28 · two reservations · Canyon area of park'},
        {n:'Grand Prismatic Spring — Yellowstone', lat:44.525, lng:-110.838, note:'Largest hot spring in US · stunning rainbow colors · Midway Geyser Basin'},
        {n:'Old Faithful — Yellowstone',           lat:44.460, lng:-110.828, note:'Erupts every 60-110 min · predictable schedule · Old Faithful Inn is historic'},
        {n:'Grand Canyon of Yellowstone',          lat:44.718, lng:-110.496, note:'Lower Falls viewpoint · 308-ft waterfall · Artist Point · Lookout Point'},
        {n:'Lamar Valley — Yellowstone',           lat:44.900, lng:-110.205, note:'Best wildlife in Yellowstone · wolf packs · bison herds · dawn/dusk viewing'},
        /* ── Washington ── */
        {n:'Mt. Rainier NP — Paradise, WA',       lat:46.786, lng:-121.736, note:'14,411 ft volcano · Skyline Trail · wildflower meadows peak in July'},
        {n:'Pike Place Market — Seattle, WA',      lat:47.609, lng:-122.342, note:'Fish throwing · Pike Place Chowder · Original Starbucks · great lunch stop'},
        {n:'Space Needle — Seattle, WA',           lat:47.620, lng:-122.349, note:'605 ft · views of Puget Sound and Mt Rainier · iconic Seattle skyline'},
        /* ── Oregon ── */
        {n:'Multnomah Falls — Columbia Gorge, OR', lat:45.576, lng:-122.116, note:'620 ft waterfall · I-84 pulloff · most-visited natural site in Oregon'},
        {n:'Crater Lake NP — Rim Village, OR',     lat:42.909, lng:-122.148, note:'Deepest lake in US at 1,943 ft · brilliant blue · Rim Drive · Wizard Island boat tour'},
        /* ── California ── */
        {n:'Jedediah Smith Redwoods — Crescent City', lat:41.786, lng:-124.097, note:"World's tallest trees · 350 ft · walk among giants at dawn · first CA stop"},
      ],
      rest: [
        /* ── PA ── */
        {n:'New Stanton Service Plaza — PA Turnpike', lat:40.215, lng:-79.598, note:'PA Turnpike · near Pittsburgh · 24hr facilities · large truck lot'},
        {n:'Midway Service Plaza — PA Turnpike',    lat:40.120, lng:-78.478, note:'PA Turnpike eastbound · 24hr · before Pittsburgh'},
        /* ── OH / IN ── */
        {n:'I-70 Rest Area — Clark County, OH',     lat:39.934, lng:-83.813, note:'Ohio · 24hr overnight ok · near Dayton'},
        {n:'I-70 Rest Area — Preble County, OH',    lat:39.865, lng:-84.558, note:'Near Dayton/IN border · free overnight · quiet'},
        {n:'I-70 Rest Area — Putnam County, IN',    lat:39.764, lng:-86.877, note:'Indiana · 24hr · maintained'},
        /* ── MO ── */
        {n:'Walmart Supercenter — Lebanon, MO',     lat:37.688, lng:-92.637, note:'I-44 Exit 130 · free overnight parking · near Shut-Ins corridor'},
        {n:'I-44 Rest Area — Conway, MO',           lat:37.505, lng:-93.006, note:'Missouri · 24hr · near Springfield'},
        /* ── NE ── */
        {n:'I-80 Rest Area — Kearney, NE',          lat:40.699, lng:-99.082, note:'Nebraska I-80 · 24hr · midpoint Nebraska push'},
        {n:'I-80 Rest Area — Sidney, NE',           lat:41.144, lng:-102.976, note:'Nebraska · near Wyoming border · free overnight'},
        /* ── WY ── */
        {n:'Walmart Supercenter — Rock Springs, WY', lat:41.585, lng:-109.203, note:'Free overnight parking · I-80 exit · good facilities · Day 5 overnight'},
        {n:'I-80 Rest Area — Green River, WY',      lat:41.537, lng:-109.471, note:'Wyoming · 24hr · near Rock Springs'},
        /* ── UT ── */
        {n:'Walmart Supercenter — SLC (West Valley)', lat:40.692, lng:-112.001, note:'Free overnight parking · west side of SLC · easy I-80 access'},
        {n:'Bonneville Salt Flats BLM Area',         lat:40.762, lng:-113.889, note:'Wendover UT · free primitive overnight on the salt · surreal experience'},
        {n:'Nevada Welcome Center — West Wendover', lat:40.739, lng:-114.055, note:'NV border · free overnight · 24hr facilities'},
        /* ── ID ── */
        {n:'Walmart Supercenter — Twin Falls, ID',  lat:42.580, lng:-114.480, note:'Free overnight parking · Day 6 overnight option'},
        /* ── MT ── */
        {n:'Walmart Supercenter — Kalispell, MT',   lat:48.214, lng:-114.320, note:'Near Glacier NP · free overnight parking · last stop before St. Mary'},
        {n:'Apgar Village — Glacier NP (West)',     lat:48.498, lng:-113.981, note:'In-park restrooms · Lake McDonald access · day use area'},
        /* ── WA ── */
        {n:'I-90 Rest Area — Ellensburg, WA',       lat:47.005, lng:-120.540, note:'Washington · 24hr · midway through Cascades on I-90'},
        {n:'Walmart Supercenter — Olympia, WA',     lat:47.028, lng:-122.906, note:'I-5 Exit 109 · free overnight parking'},
        /* ── OR ── */
        {n:'Walmart Supercenter — Medford, OR',     lat:42.326, lng:-122.876, note:'Free overnight · last OR stop before Redwoods'},
        /* ── CA ── */
        {n:'I-5 Rest Area — Yreka, CA',             lat:41.735, lng:-122.635, note:'Northern CA · I-5 · 24hr · heading south toward Redding'},
      ],
      shower: [
        /* ── PA ── */
        {n:'Flying J Travel Center — New Stanton, PA', lat:40.213, lng:-79.600, note:'I-76 Exit 75 · 12 showers · $15 · near Pittsburgh'},
        /* ── OH / IN ── */
        {n:"Love's Travel Stop — Columbus, OH",     lat:39.967, lng:-82.827, note:'I-270 exit · $15 · 24hr'},
        {n:'Pilot Flying J — Dayton, OH',           lat:39.804, lng:-84.271, note:'I-70/I-75 junction · $15 · 24hr'},
        {n:"Love's Travel Stop — Richmond, IN",     lat:39.830, lng:-84.856, note:'I-70 Exit 145 · $15 · 24hr'},
        /* ── MO ── */
        {n:"Love's Travel Stop — Foristell, MO",   lat:38.817, lng:-90.906, note:'I-70 Exit 203 · between STL and KC · $15'},
        {n:'Pilot Flying J — Joplin, MO',          lat:37.053, lng:-94.482, note:'I-44 · $15 · south MO / Route 66 corridor'},
        /* ── NE ── */
        {n:"Love's Travel Stop — Kearney, NE",     lat:40.699, lng:-99.082, note:'I-80 Nebraska · $15 · 24hr · midway push'},
        {n:'Pilot Flying J — North Platte, NE',    lat:41.122, lng:-100.752, note:'I-80 · $15 · 24hr · western Nebraska'},
        /* ── WY ── */
        {n:'Pilot Flying J — Rock Springs, WY',    lat:41.585, lng:-109.205, note:'I-80 Exit 99 · $15 · 24hr · Day 5 overnight stop'},
        {n:'TA Travel Center — Laramie, WY',       lat:41.311, lng:-105.590, note:'I-80 · 8 showers · $15 · Wyoming push'},
        /* ── UT ── */
        {n:"Love's Travel Stop — Wendover, UT",    lat:40.737, lng:-114.041, note:'I-80 state line · $15 · 24hr'},
        {n:'Pilot Flying J — Salt Lake City, UT',  lat:40.761, lng:-111.898, note:'I-15 · $15 · 24hr · SLC area'},
        /* ── ID ── */
        {n:"Love's Travel Stop — Twin Falls, ID",  lat:42.600, lng:-114.447, note:'US-93 South · $15 · 24hr'},
        /* ── MT ── */
        {n:"Love's Travel Stop — Missoula, MT",    lat:46.841, lng:-114.098, note:'I-90 Exit 96 · $15 · 24hr · pass-through on Day 7'},
        {n:'TA Travel Center — Missoula, MT',      lat:46.844, lng:-114.095, note:'Broadway · 8 showers · $15'},
        /* ── WA ── */
        {n:'Pilot Flying J — Spokane, WA',         lat:47.688, lng:-117.297, note:'I-90 · $15 · 24hr · Day 14 overnight'},
        {n:"Love's Travel Stop — Ellensburg, WA",  lat:47.005, lng:-120.540, note:'I-90 · $15 · halfway through Cascades'},
        /* ── OR ── */
        {n:"Love's Travel Stop — Grants Pass, OR", lat:42.441, lng:-123.330, note:'I-5 Exit 55 · $15 · last OR shower stop'},
        /* ── CA ── */
        {n:'Pilot Flying J — Redding, CA',         lat:40.589, lng:-122.393, note:'I-5 · $15 · northern CA heading south'},
      ],
      food: [
        {n:'Primanti Bros — Pittsburgh, PA',             lat:40.441, lng:-79.996, note:'Iconic sandwich with coleslaw + fries inside the bread'},
        {n:'Wheel Restaurant — Dayton, OH',              lat:39.758, lng:-84.192, note:'Dayton classic diner · breakfast all day · local institution'},
        {n:"Shapiro's Delicatessen — Indianapolis, IN",  lat:39.762, lng:-86.151, note:'Legendary deli since 1905 · corned beef · huge portions'},
        {n:"Ted Drewes Frozen Custard — St. Louis, MO",  lat:38.586, lng:-90.316, note:'Summer institution since 1929 · concrete mixer custard · must-stop'},
        {n:"Lambert's Café — Springfield, MO",           lat:37.170, lng:-93.309, note:"Throwed rolls · Route 66 legend · 'Only Home of Throwed Rolls'"},
        {n:"Joe's Kansas City Bar-B-Que — KC, MO",       lat:38.979, lng:-94.609, note:'Inside a gas station · Z-Man sandwich · BBQ scripture'},
        {n:'Red Iguana — Salt Lake City, UT',            lat:40.761, lng:-111.891, note:'Legendary Mexican mole · expect a wait · worth it'},
        {n:"Whitefish Coffee Traders — Whitefish, MT",   lat:48.412, lng:-114.338, note:'Best coffee in Montana · morning before Glacier'},
        {n:'Pike Place Chowder — Seattle, WA',           lat:47.609, lng:-122.341, note:'Award-winning clam chowder · Pike Place Market · must-have'},
        {n:'Voodoo Doughnut — Portland, OR',             lat:45.523, lng:-122.674, note:'24hr · maple bacon doughnut · iconic PDX stop'},
        {n:'Crater Lake Lodge Dining Room',              lat:42.909, lng:-122.148, note:'Rim views while eating · reserve ahead · historic lodge'},
        {n:"In-N-Out Burger — Redding, CA",              lat:40.580, lng:-122.399, note:'First California In-N-Out heading south on I-5'},
      ]
    }
  }
};

// ── Marker store & colors ─────────────────────────────────────────────
const activeMarkers = {};
const LAYER_COLOR = { rest:'#2b6cb0', shower:'#276749', food:'#c05621', dest:'#6B46C1' };

// ── Maps JS API callback ──────────────────────────────────────────────
function initMaps() {
  for (const rId of Object.keys(ROUTE_STOPS)) {
    const canvas = document.getElementById(rId + '-map-canvas');
    if (!canvas) continue;
    const obs = new IntersectionObserver(entries => {
      if (entries[0].isIntersecting) { buildMap(rId); obs.disconnect(); }
    }, { threshold: 0.1 });
    obs.observe(canvas);
  }
}

function buildMap(rId) {
  const data  = ROUTE_STOPS[rId];
  const canvas = document.getElementById(rId + '-map-canvas');
  canvas.innerHTML = '';

  const map = new google.maps.Map(canvas, {
    zoom: 5,
    center: { lat: 44.0, lng: -103.0 },
    mapTypeId: 'roadmap',
    disableDefaultUI: true,
    zoomControl: true,
    fullscreenControl: true
  });

  // Draw route
  new google.maps.DirectionsService().route({
    origin: data.origin,
    destination: data.destination,
    waypoints: data.waypoints.map(l => ({ location: l, stopover: true })),
    travelMode: google.maps.TravelMode.DRIVING,
    optimizeWaypoints: false
  }, (result, status) => {
    if (status === 'OK') {
      new google.maps.DirectionsRenderer({
        map, suppressMarkers: true,
        polylineOptions: { strokeColor:'#1a365d', strokeWeight:5, strokeOpacity:0.75 }
      }).setDirections(result);
    }
  });

  // Place stop markers
  activeMarkers[rId] = {};
  for (const layer of Object.keys(data.stops)) {
    activeMarkers[rId][layer] = [];
  }
  const iw = new google.maps.InfoWindow();

  for (const [layer, stops] of Object.entries(data.stops)) {
    for (const s of stops) {
      const m = new google.maps.Marker({
        position: { lat: s.lat, lng: s.lng },
        map,
        title: s.n,
        icon: {
          path: google.maps.SymbolPath.CIRCLE,
          scale: layer === 'dest' ? 11 : 9,
          fillColor: LAYER_COLOR[layer],
          fillOpacity: layer === 'dest' ? 1.0 : 0.92,
          strokeColor: '#ffffff',
          strokeWeight: 2.5
        }
      });
      m.addListener('click', () => {
        iw.setContent(
          `<div style="font-family:sans-serif;font-size:13px;max-width:240px;line-height:1.5">` +
          `<strong>${s.n}</strong><br><span style="color:#4a5568;font-size:12px">${s.note}</span></div>`
        );
        iw.open(map, m);
      });
      activeMarkers[rId][layer].push(m);
    }
  }
}

// ── Layer toggle ─────────────────────────────────────────────────────
function toggleLayer(rId, layer, btn) {
  const markers = activeMarkers[rId]?.[layer];
  if (!markers) return;
  const on = btn.classList.toggle('active');
  markers.forEach(m => m.setVisible(on));
}
</script>"""

# Replace the existing script block (first <script> tag only, not the Maps API one)
old_script_pattern = re.compile(r'<script>\s*//.*?</script>', re.DOTALL)
match = old_script_pattern.search(html)
if match:
    html = html[:match.start()] + NEW_JS + html[match.end():]
    print('  ✓ JavaScript replaced (ROUTE_STOPS r1-r10 removed, r11 rebuilt with all layers)')
else:
    print('  ✗ Script block not found')

# ── Update section title text ─────────────────────────────────────────────────
html = html.replace(
    '10 Route Combinations — Pick Your Adventure',
    'Route 11 — The Grand American Loop',
    1
)
html = html.replace(
    'All legs validated via Google Maps Distance Matrix API · All arrive SF by noon July 2 · All include Yellowstone (2 nights)',
    '18 days · 12 states · 6 National Parks · ~5,854 miles · every drive time Google Maps verified',
    1
)

with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'Final:    {len(html):,} bytes')
print('Done — pre-california-routes.html rebuilt.')
