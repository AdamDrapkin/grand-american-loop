#!/usr/bin/env python3
"""
Route 11 map pins overhaul:
1. Add 'dest' (destinations/attractions) layer — all parks + landmarks with exact coords
2. Populate rest (overnight truck stops) + shower (Pilot/Love's/TA) + food across all 22 days
3. Fix Day 2 description to show Ohio
4. Update buildMap() to handle dynamic layers (not hardcoded rest/shower/food)
5. Add dest CSS + LAYER_COLOR + toggle button to r11 map controls
"""

import re, json, subprocess

HTML_PATH = '/Users/adamdrapkin/California Trip/pre-california-routes.html'

# ──────────────────────────────────────────────────────────────────────────────
# 1. COMPLETE r11 ROUTE_STOPS
# ──────────────────────────────────────────────────────────────────────────────
R11_STOPS = """,r11: {
    origin: 'Huntington Valley, PA',
    destination: 'San Francisco, CA',
    waypoints: [
      'Pittsburgh, PA','Indianapolis, IN','Utica, IL','St. Louis, MO',
      'Lesterville, MO','Springfield, MO','Kansas City, MO','Oakley, KS',
      'Denver, CO','Grand Canyon National Park, AZ','Page, AZ',
      'Zion National Park, UT','Bryce Canyon National Park, UT',
      'Salt Lake City, UT','Wendover, UT','Twin Falls, ID',
      'Craters of the Moon National Monument, ID','Missoula, MT','Polson, MT',
      'Glacier National Park, MT','Winthrop, WA','Seattle, WA',
      'Portland, OR','Bend, OR','Crater Lake National Park, OR'
    ],
    stops: {
      dest: [
        /* ── Pennsylvania ── */
        {n:'Mount Washington Overlook — Pittsburgh',      lat:40.427, lng:-80.013, note:'Best Pittsburgh skyline view · Duquesne Incline'},
        /* ── Ohio ── */
        {n:'Short North Arts District — Columbus, OH',    lat:39.976, lng:-83.003, note:'Best food + street art in Columbus · I-70 midpoint'},
        {n:'Dayton Aviation Heritage NHP — Dayton, OH',  lat:39.771, lng:-84.194, note:'Wright Brothers history · free · 30 min off I-70'},
        /* ── Illinois ── */
        {n:'Starved Rock State Park — Utica, IL',         lat:41.318, lng:-88.972, note:'18 canyons · waterfalls · best hiking in IL'},
        /* ── Missouri ── */
        {n:'Gateway Arch National Park — St. Louis, MO', lat:38.625, lng:-90.185, note:'630 ft · go up inside · 315K-view Instagram reel'},
        {n:'Johnson\'s Shut-Ins — Lesterville, MO',      lat:37.569, lng:-90.843, note:'Nature-made water park in granite gorge · swim!'},
        {n:'Meramec Caverns — Stanton, MO',              lat:38.215, lng:-91.057, note:'Jesse James hideout · I-44/Route 66 · 5-level cave'},
        {n:'Route 66 Mural City — Cuba, MO',             lat:38.062, lng:-91.399, note:'14 giant murals · Route 66 centennial 2026'},
        {n:'Route 66 Birthplace — Springfield, MO',      lat:37.209, lng:-93.292, note:'Named here 1926 · Lambert\'s Throwed Rolls'},
        /* ── Kansas ── */
        {n:'Monument Rocks — Oakley, KS',                lat:38.773, lng:-100.850, note:'70-ft chalk pyramids · 8 Wonders of Kansas · free'},
        /* ── Colorado ── */
        {n:'Red Rocks Amphitheatre — Morrison, CO',       lat:39.665, lng:-105.206, note:'Sunset hike · natural sandstone amphitheatre'},
        /* ── New Mexico (I-25 transit) ── */
        {n:'Old Town Albuquerque — Albuquerque, NM',     lat:35.096, lng:-106.670, note:'Brief stretch stop · adobe architecture · green chile'},
        /* ── Arizona ── */
        {n:'Grand Canyon South Rim — Grand Canyon, AZ',  lat:36.058, lng:-112.140, note:'1 mile deep · Rim Trail · Bright Angel viewpoint'},
        {n:'Horseshoe Bend — Page, AZ',                  lat:36.879, lng:-111.510, note:'270° river curve · 10-min walk · free'},
        {n:'Lake Powell Overlook — Page, AZ',            lat:36.942, lng:-111.487, note:'Massive reservoir behind Glen Canyon Dam'},
        /* ── Utah ── */
        {n:'Zion Canyon Visitor Center — Zion NP, UT',   lat:37.199, lng:-112.987, note:'Walk up-canyon · Angels Landing trailhead · Narrows'},
        {n:'Bryce Canyon Rim Trail — Bryce Canyon, UT',  lat:37.629, lng:-112.168, note:'Orange hoodoo spires · Navajo Loop trail'},
        {n:'Bonneville Salt Flats — Wendover, UT',       lat:40.762, lng:-113.889, note:'Drive onto the salt · 30,000 acres · land speed records'},
        /* ── Idaho ── */
        {n:'Shoshone Falls — Twin Falls, ID',             lat:42.590, lng:-114.369, note:'212 ft · taller than Niagara · Snake River Canyon'},
        {n:'Craters of the Moon NM — Arco, ID',          lat:43.396, lng:-113.516, note:'Lava fields · NASA astronaut training site'},
        {n:'Sun Valley / Ketchum — Ketchum, ID',         lat:43.680, lng:-114.363, note:'Hemingway\'s home + burial · mountain town'},
        {n:'Salmon River Canyon — Salmon, ID',           lat:45.174, lng:-113.895, note:'Deepest gorge in North America · whitewater'},
        /* ── Montana ── */
        {n:'National Bison Range — Moiese, MT',          lat:47.351, lng:-114.075, note:'Wildlife drive · 350 bison · on US-93 route'},
        {n:'Flathead Lake — Polson, MT',                 lat:47.694, lng:-114.159, note:'Largest freshwater lake west of Mississippi'},
        {n:'Whitefish, MT',                              lat:48.412, lng:-114.338, note:'Charming mountain town · 35 min from Glacier · MT Coffee Traders'},
        {n:'Glacier NP — Lake McDonald',                 lat:48.565, lng:-113.881, note:'10-mile turquoise lake · surrounded by old-growth'},
        {n:'Glacier NP — Logan Pass (GOTTS Road)',       lat:48.696, lng:-113.718, note:'6,646 ft · mountain goats · Hidden Lake trail'},
        {n:'Glacier NP — Many Glacier Valley',           lat:48.797, lng:-113.657, note:'East side · most wildlife · Grinnell Glacier hike'},
        /* ── Washington ── */
        {n:'North Cascades NP — SR-20 (Diablo Lake)',    lat:48.714, lng:-121.131, note:'Turquoise glacial lake · drive-through on SR-20'},
        {n:'Pike Place Market — Seattle, WA',            lat:47.609, lng:-122.342, note:'Fish throwing · chowder · local produce'},
        {n:'Space Needle — Seattle, WA',                 lat:47.620, lng:-122.349, note:'Views of Puget Sound + Mt Rainier'},
        {n:'Mt Rainier NP — Paradise, WA',               lat:46.786, lng:-121.736, note:'14,411 ft volcano · Skyline Trail · wildflowers in July'},
        /* ── Oregon ── */
        {n:'Multnomah Falls — Columbia Gorge, OR',       lat:45.576, lng:-122.116, note:'620 ft · most-visited OR attraction · I-84 pulloff'},
        {n:'Silver Falls SP — Silverton, OR',            lat:44.877, lng:-122.656, note:'Trail of Ten Falls · 7.2-mile loop'},
        {n:'Tamolitch / Blue Pool — McKenzie Bridge, OR',lat:44.297, lng:-122.057, note:'Crystal-clear lava-rock swimming hole · 4.2-mi hike'},
        {n:'Painted Hills — Mitchell, OR',               lat:44.659, lng:-120.101, note:'Red/gold layered hills · 7 Wonders of Oregon'},
        {n:'Smith Rock SP — Terrebonne, OR',             lat:44.368, lng:-121.140, note:'World-class rock spires · Misery Ridge trail'},
        {n:'Crater Lake NP — Rim Village, OR',           lat:42.909, lng:-122.148, note:'Deepest lake in US · Rim Drive · Wizard Island boat'},
        /* ── California ── */
        {n:'Jedediah Smith Redwoods — Crescent City, CA',lat:41.786, lng:-124.097, note:'World\'s tallest trees · 350 ft · sunrise walk'},
      ],
      rest: [
        /* ── PA / OH ── */
        {n:'Ohio Welcome Center — I-70 EB',              lat:40.012, lng:-80.869, note:'PA/OH border · clean facilities · 24hr'},
        {n:'Pilot Flying J — Zanesville, OH',            lat:39.931, lng:-82.007, note:'I-70 Exit 160 · 24hr · large truck lot'},
        {n:'I-70 Rest Area — Clark County, OH',          lat:39.934, lng:-83.813, note:'Near Columbus · 24hr overnight ok'},
        {n:'I-70 Rest Area — Preble County, OH',         lat:39.865, lng:-84.558, note:'Near Dayton · free overnight · quiet'},
        /* ── IN / IL ── */
        {n:'Indiana I-70 Rest Area — Putnam County',     lat:39.764, lng:-86.877, note:'Indiana · 24hr · maintained'},
        {n:'Illinois I-70 Rest Area — Vandalia, IL',     lat:38.993, lng:-89.091, note:'Central IL · clean · 24hr'},
        /* ── MO ── */
        {n:'Walmart Supercenter — Lebanon, MO',          lat:37.688, lng:-92.637, note:'I-44 Exit 130 · free overnight parking'},
        {n:'I-44 Rest Area — Conway, MO',                lat:37.505, lng:-93.006, note:'Missouri · 24hr · near Springfield'},
        /* ── KS / CO ── */
        {n:'I-70 Rest Area — Salina, KS',                lat:38.841, lng:-97.611, note:'Kansas · spacious truck lot · 24hr'},
        {n:'I-70 Rest Area — Colby, KS',                 lat:39.394, lng:-101.052, note:'West KS · free overnight · quiet'},
        {n:'Colorado Welcome Center — Burlington, CO',   lat:39.304, lng:-102.270, note:'CO border · excellent facilities'},
        {n:'I-70 Rest Area — Limon, CO',                 lat:39.264, lng:-103.692, note:'Central CO · 24hr · heading into Rockies'},
        /* ── NM / AZ ── */
        {n:'Walmart Supercenter — Flagstaff, AZ',        lat:35.197, lng:-111.651, note:'Free overnight parking · near Grand Canyon'},
        /* ── UT ── */
        {n:'Bonneville Salt Flats BLM Area',             lat:40.762, lng:-113.889, note:'Wendover UT · free primitive overnight on the salt'},
        {n:'I-15 Rest Area — Beaver, UT',                lat:38.275, lng:-112.641, note:'Utah · clean · 24hr'},
        /* ── NV / ID ── */
        {n:'Nevada Welcome Center — West Wendover, NV',  lat:40.739, lng:-114.055, note:'NV border · free overnight · 24hr'},
        {n:'I-80 Rest Area — Wells, NV',                 lat:41.114, lng:-114.963, note:'Nevada · free overnight · quiet'},
        {n:'Walmart Supercenter — Twin Falls, ID',       lat:42.580, lng:-114.480, note:'Free overnight parking · Twin Falls'},
        /* ── ID (mountain route) ── */
        {n:'Walmart Supercenter — Boise, ID',            lat:43.619, lng:-116.356, note:'Free overnight parking · I-84 corridor'},
        {n:'Walmart Supercenter — Salmon, ID',           lat:45.174, lng:-113.896, note:'Free overnight · mid-Idaho mountains'},
        /* ── MT ── */
        {n:'Walmart Supercenter — Missoula, MT',         lat:46.871, lng:-114.095, note:'Free overnight parking · I-90 Exit 101'},
        {n:'Walmart Supercenter — Kalispell, MT',        lat:48.214, lng:-114.320, note:'Near Glacier NP · free overnight parking'},
        {n:'Apgar Village — Glacier NP (West)',          lat:48.498, lng:-113.981, note:'In-park restrooms · Lake McDonald access'},
        /* ── WA ── */
        {n:'I-5 Rest Area — Centralia, WA',              lat:46.714, lng:-122.955, note:'WA · midway Seattle-Portland · 24hr'},
        {n:'Walmart Supercenter — Olympia, WA',          lat:47.028, lng:-122.906, note:'I-5 Exit 109 · free overnight parking'},
        /* ── OR ── */
        {n:'Walmart Supercenter — Eugene, OR',           lat:44.058, lng:-123.087, note:'I-5 Eugene · free overnight parking'},
        {n:'Walmart Supercenter — Bend, OR',             lat:44.058, lng:-121.315, note:'Bend base camp · free overnight parking'},
        {n:'Walmart Supercenter — Medford, OR',          lat:42.326, lng:-122.876, note:'Free overnight · last OR stop before CA'},
        /* ── CA ── */
        {n:'I-5 Rest Area — Yreka, CA',                  lat:41.735, lng:-122.635, note:'Northern CA · I-5 · 24hr'},
      ],
      shower: [
        /* ── PA ── */
        {n:'Flying J Travel Center — New Stanton, PA',   lat:40.213, lng:-79.600, note:'I-76 Exit 75 · 12 showers · $15'},
        /* ── OH ── */
        {n:"Love's Travel Stop — Columbus, OH",          lat:39.967, lng:-82.827, note:'I-270 exit · $15 · 24hr'},
        {n:'Pilot Flying J — Dayton, OH',                lat:39.804, lng:-84.271, note:'I-70/I-75 junction · $15 · 24hr'},
        /* ── IN ── */
        {n:"Love's Travel Stop — Richmond, IN",          lat:39.830, lng:-84.856, note:'I-70 Exit 145 · $15 · 24hr'},
        /* ── IL / MO ── */
        {n:"Love's Travel Stop — Foristell, MO",         lat:38.817, lng:-90.906, note:'I-70 Exit 203 · between STL and KC · $15'},
        {n:'Pilot Flying J — Joplin, MO',                lat:37.053, lng:-94.482, note:'I-44 · $15 · south MO Route 66 corridor'},
        /* ── KS / CO ── */
        {n:"Love's Travel Stop — Salina, KS",            lat:38.841, lng:-97.612, note:'I-70 Exit 252 · 12 showers · $15'},
        {n:'Pilot Travel Center — Colby, KS',            lat:39.394, lng:-101.052, note:'I-70 Exit 54 · 5 showers · $15'},
        {n:'Flying J Travel Center — Limon, CO',         lat:39.264, lng:-103.692, note:'I-70 Exit 359 · 8 showers · $15'},
        /* ── AZ / UT ── */
        {n:"Love's Travel Stop — Flagstaff, AZ",         lat:35.197, lng:-111.651, note:'I-40 Exit 195 · $15 · 24hr'},
        {n:"Love's Travel Stop — Cedar City, UT",        lat:37.680, lng:-113.070, note:'I-15 Exit 57 · $15 · near Zion + Bryce'},
        {n:'Pilot Flying J — Salt Lake City, UT',        lat:40.761, lng:-111.898, note:'I-15 · $15 · 24hr'},
        /* ── NV / ID ── */
        {n:"Love's Travel Stop — Wendover, UT/NV",       lat:40.737, lng:-114.041, note:'I-80 state line · $15 · 24hr'},
        {n:"Love's Travel Stop — Twin Falls, ID",        lat:42.600, lng:-114.447, note:'US-93 South · $15 · 24hr'},
        {n:'Pilot Flying J — Boise, ID',                 lat:43.590, lng:-116.552, note:'I-84 Exit 54 · $15 · 24hr'},
        /* ── MT ── */
        {n:"Love's Travel Stop — Missoula, MT",          lat:46.841, lng:-114.098, note:'I-90 Exit 96 · $15 · 24hr'},
        {n:'TA Travel Center — Missoula, MT',            lat:46.844, lng:-114.095, note:'Broadway · 8 showers · $15'},
        /* ── WA / OR ── */
        {n:'Pilot Flying J — Spokane, WA',               lat:47.688, lng:-117.297, note:'I-90 · $15 · 24hr'},
        {n:"Love's Travel Stop — Ellensburg, WA",        lat:47.005, lng:-120.540, note:'I-90 · $15 · halfway through Cascades'},
        {n:"Love's Travel Stop — Grants Pass, OR",       lat:42.441, lng:-123.330, note:'I-5 Exit 55 · $15 · last OR shower stop'},
        /* ── CA ── */
        {n:'Pilot Flying J — Redding, CA',               lat:40.589, lng:-122.393, note:'I-5 · $15 · northern CA on I-5 south'},
      ],
      food: [
        {n:"Primanti Bros — Pittsburgh, PA",             lat:40.441, lng:-79.996, note:'Iconic sandwich · coleslaw + fries inside the bread'},
        {n:'White Castle — Columbus, OH',                lat:39.961, lng:-82.999, note:'Midwest original · 24hr · I-70 corridor'},
        {n:"Shapiro's Delicatessen — Indianapolis, IN",  lat:39.762, lng:-86.151, note:'Legendary deli since 1905 · huge portions'},
        {n:"Ted Drewes Frozen Custard — St. Louis, MO", lat:38.586, lng:-90.316, note:'Summer institution since 1929 · must-stop'},
        {n:"Lambert's Café — Springfield, MO",          lat:37.170, lng:-93.309, note:"Throwed rolls · Route 66 legend · 'Only Home of Throwed Rolls'"},
        {n:"Joe's Kansas City Bar-B-Que — KC, MO",      lat:38.979, lng:-94.609, note:'Inside a gas station · BBQ scripture · get the Z-Man'},
        {n:'Red Rocks Trading Post Café — Morrison, CO', lat:39.665, lng:-105.205, note:'After the sunset hike · views of the amphitheatre'},
        {n:'Bright Angel Restaurant — Grand Canyon, AZ', lat:36.057, lng:-112.143, note:'Inside the park · rim-top dining since 1905'},
        {n:'Red Iguana — Salt Lake City, UT',           lat:40.761, lng:-111.891, note:'Legendary Mexican mole · expect a wait'},
        {n:"Louis' Basque Corner — Reno, NV",           lat:39.530, lng:-119.814, note:'Family-style Basque dinner · huge portions · cheap'},
        {n:"Diablo Burger — Flagstaff, AZ",              lat:35.198, lng:-111.653, note:'Best burger in AZ · local beef · open late'},
        {n:"Whitefish Coffee Traders — Whitefish, MT",  lat:48.412, lng:-114.338, note:'Best coffee in Montana · morning before Glacier'},
        {n:'Pike Place Chowder — Seattle, WA',          lat:47.609, lng:-122.341, note:'Award-winning clam chowder · Pike Place Market'},
        {n:'Voodoo Doughnut — Portland, OR',            lat:45.523, lng:-122.674, note:'24hr · maple bacon doughnut · iconic PDX stop'},
        {n:'Deschutes Brewery Public House — Bend, OR', lat:44.052, lng:-121.311, note:'World-class craft beer + pub food'},
        {n:'Crater Lake Lodge Dining Room',             lat:42.909, lng:-122.148, note:'Rim views while eating · reserve ahead · historic lodge'},
        {n:"In-N-Out Burger — Redding, CA",             lat:40.580, lng:-122.399, note:'First California In-N-Out heading south on I-5'},
      ]
    }
  }"""

# ──────────────────────────────────────────────────────────────────────────────
# 2. JS CHANGES
# ──────────────────────────────────────────────────────────────────────────────

# New LAYER_COLOR including dest
OLD_LAYER_COLOR = "const LAYER_COLOR = { rest:'#2b6cb0', shower:'#276749', food:'#c05621' };"
NEW_LAYER_COLOR = "const LAYER_COLOR = { rest:'#2b6cb0', shower:'#276749', food:'#c05621', dest:'#6B46C1' };"

# Dynamic activeMarkers init in buildMap
OLD_ACTIVEMARKERS = "  activeMarkers[rId] = { rest:[], shower:[], food:[] };"
NEW_ACTIVEMARKERS = """  activeMarkers[rId] = {};
  for (const layer of Object.keys(data.stops)) {
    activeMarkers[rId][layer] = [];
  }"""

# Dest marker gets a larger scale
OLD_ICON_BUILD = """        icon: {
          path: google.maps.SymbolPath.CIRCLE,
          scale: 9,
          fillColor: LAYER_COLOR[layer],
          fillOpacity: 0.92,
          strokeColor: '#ffffff',"""
NEW_ICON_BUILD = """        icon: {
          path: google.maps.SymbolPath.CIRCLE,
          scale: layer === 'dest' ? 11 : 9,
          fillColor: LAYER_COLOR[layer],
          fillOpacity: layer === 'dest' ? 1.0 : 0.92,
          strokeColor: '#ffffff',"""

# ──────────────────────────────────────────────────────────────────────────────
# 3. CSS — add dest button style
# ──────────────────────────────────────────────────────────────────────────────
OLD_CSS_FOOD = "    .map-layer-btn.active.food { background: #c05621; color: white; }"
NEW_CSS_FOOD  = """    .map-layer-btn.active.food { background: #c05621; color: white; }
    .map-layer-btn.dest { border-color: #6B46C1; color: #6B46C1; }
    .map-layer-btn.active.dest { background: #6B46C1; color: white; }"""

# ──────────────────────────────────────────────────────────────────────────────
# 4. r11 map-controls — add 📍 Destinations toggle
# ──────────────────────────────────────────────────────────────────────────────
OLD_R11_CONTROLS = """          <div class="map-controls" style="background:linear-gradient(135deg,#fffdf5,#fff9e6);">
            <span class="map-ctrl-label" style="color:var(--gold);">🌟 Route 11 · Jun 11→Jul 2 · 16 states · 10 NPS sites</span>
          </div>"""
NEW_R11_CONTROLS = """          <div class="map-controls" style="background:linear-gradient(135deg,#fffdf5,#fff9e6);">
            <span class="map-ctrl-label" style="color:var(--gold);">🌟 Route 11</span>
            <button class="map-layer-btn dest active" onclick="toggleLayer('r11','dest',this)">📍 Destinations</button>
            <button class="map-layer-btn rest active" onclick="toggleLayer('r11','rest',this)">🛌 Rest Stops</button>
            <button class="map-layer-btn shower active" onclick="toggleLayer('r11','shower',this)">🚿 Showers</button>
            <button class="map-layer-btn food active" onclick="toggleLayer('r11','food',this)">🍳 Food</button>
          </div>"""

# ──────────────────────────────────────────────────────────────────────────────
# 5. Day 2 description — add Ohio
# ──────────────────────────────────────────────────────────────────────────────
OLD_DAY2 = '<span class="dn">Jun 12</span><span class="dr">Pittsburgh → Indianapolis, IN</span><span class="dd">359 mi · 5h 33m</span>'
NEW_DAY2 = '<span class="dn">Jun 12</span><span class="dr">Pittsburgh, PA → Columbus, OH → Dayton, OH → Indianapolis, IN</span><span class="dd">359 mi · 5h 33m</span>'

# ──────────────────────────────────────────────────────────────────────────────
# APPLY ALL CHANGES
# ──────────────────────────────────────────────────────────────────────────────
with open(HTML_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

print(f'File before: {len(html):,} bytes')

def replace(html, old, new, label):
    if old in html:
        html = html.replace(old, new, 1)
        print(f'  ✓ {label}')
    else:
        print(f'  ✗ NOT FOUND: {label}')
    return html

# Replace r11 ROUTE_STOPS (the empty one)
old_r11_stops = re.search(r',r11: \{[\s\S]*?stops: \{ rest: \[\], shower: \[\], food: \[\] \}\s*\}\s*', html)
if old_r11_stops:
    html = html[:old_r11_stops.start()] + R11_STOPS + '\n  ' + html[old_r11_stops.end():]
    print('  ✓ r11 ROUTE_STOPS populated (dest + rest + shower + food)')
else:
    print('  ✗ r11 ROUTE_STOPS not found')

html = replace(html, OLD_LAYER_COLOR, NEW_LAYER_COLOR, 'LAYER_COLOR + dest')
html = replace(html, OLD_ACTIVEMARKERS, NEW_ACTIVEMARKERS, 'dynamic activeMarkers init')
html = replace(html, OLD_ICON_BUILD, NEW_ICON_BUILD, 'dest marker scale')
html = replace(html, OLD_CSS_FOOD, NEW_CSS_FOOD, 'dest CSS styles')
html = replace(html, OLD_R11_CONTROLS, NEW_R11_CONTROLS, 'r11 map controls (4 buttons)')
html = replace(html, OLD_DAY2, NEW_DAY2, 'Day 2 — Ohio added')

# Validate JS
match = re.search(r'const ROUTE_STOPS = \{([\s\S]*?)\};\s*\n\s*//', html)
if match:
    result = subprocess.run(
        ['node', '-e',
         f'try{{const o=new Function("return {{"+{json.dumps(match.group(1))}+"}}");'
         f'const d=o();const r=d.r11;'
         f'console.log("✓ JS valid");'
         f'console.log("r11 dest pins:",r.stops.dest.length);'
         f'console.log("r11 rest stops:",r.stops.rest.length);'
         f'console.log("r11 showers:",r.stops.shower.length);'
         f'console.log("r11 food:",r.stops.food.length);'
         f'}}catch(e){{console.error("✗",e.message)}}'],
        capture_output=True, text=True
    )
    print('\n' + result.stdout.strip() if result.stdout else '\n✗ ' + result.stderr.strip())

with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'\nFile after: {len(html):,} bytes')
print('Done.')
