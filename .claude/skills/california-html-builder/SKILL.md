---
name: california-html-builder
description: Complete build system for California Road Trip HTML guides (SF→LA, Jul 2–12 2026). Contains CSS variables, component templates, Google Maps Embed patterns, build script instructions, and all verified content data extracted from california-trip-plan.md. Invoke this before writing any California HTML file.
metadata:
  type: reference
---

# California HTML Builder Skill

## CORE PRINCIPLE
`california-trip-plan.md` is the single source of truth. Everything below was extracted from that file. Do not invent content. Do not omit confirmed data. If it is in the markdown, it goes in the HTML.

---

## 1. FILES TO BUILD (7 total, this order)

| # | File | Segment | Hotel | Nights | Days |
|---|---|---|---|---|---|
| 1 | `california-routes.html` | Hub | — | — | Master hub |
| 2 | `sf-guide.html` | San Francisco | Hyatt #40023B19345813 | Jul 2–5 (3) | Days 1–3 |
| 3 | `bigsur-guide.html` | Big Sur → Cambria | Castle Inn (BK.com conf 6459555758, PIN 8199) | Jul 5–6 (1) | Day 4 |
| 4 | `centralcoast-guide.html` | Santa Barbara | Beachside Inn #1075827673 | Jul 6–7 (1) | Day 5 |
| 5 | `sandiego-guide.html` | San Diego/Coronado | Best Western Plus #6459555758 | Jul 7–8 (1) | Day 6 |
| 6 | `la-guide.html` | Los Angeles | TBD (stub only — no invented details) | Jul 8–11 (3) | Days 7–10 + dep |
| 7 | `build_california.py` | — | — | — | Builds docs/california-viewer.html |

---

## 2. CALIFORNIA COLOR SYSTEM

```css
:root {
  --pacific:  #0B4F6C;   /* deep Pacific — SF primary accent */
  --coastal:  #1B7A9E;   /* coastal blue — San Diego */
  --sunset:   #C05621;   /* PCH/sunset orange — LA */
  --golden:   #B7730A;   /* wine country gold — Central Coast */
  --redwood:  #3A6B4A;   /* Big Sur forest — Big Sur */
  --cream:    #FDFBF7;   /* warm body background */
  --sand:     #F5E6D3;   /* beach sand accent panels */
  --dark:     #1A202C;   /* body text */
  --mid:      #4A5568;   /* secondary text */
  --border:   #C8D8EA;   /* borders */
  --snow:     #F0F7FF;   /* card backgrounds */
  --amber:    #92400E;   /* warning amber */
  --green:    #1F6B2A;   /* confirmed green */
  --red:      #C0392B;   /* alert red */
  --gold:     #D69E2E;   /* star ratings */
}
```

Hero gradients:
- **Hub**: `135deg, #0B4F6C 0%, #1B7A9E 40%, #C05621 80%, #B7730A 100%`
- **SF**: `160deg, #0B4F6C, #1B7A9E, #3A6B4A`
- **Big Sur**: `160deg, #1A3D2B, #3A6B4A, #6B4226`
- **Central Coast**: `160deg, #5C3A1E, #B7730A, #C05621`
- **San Diego**: `160deg, #0B4F6C, #1B7A9E, #0D6B7A`
- **LA**: `160deg, #3D1F00, #C05621, #B7730A`

---

## 3. SEGMENT LAYOUT STRUCTURE (all 5 segment guides follow this)

```
<body style="background:var(--cream)">
  <div class="wrap">                     ← max-width:820px; margin:0 auto; padding:0 16px
    <div class="hero">                   ← gradient, title, dates, hotel chip
    <div class="booking-banner">         ← confirmed + pending items
    <div class="overview-strip">         ← N day cards
    <section> (repeat per day)
      <div class="day-section">
        <div class="day-hd [sf|bigsur|coast|sandiego|la]">
        <div class="day-body">
          <div class="map-section">      ← Google Maps embed + route-strip
          <div class="time-block">       ← Morning (repeat for Afternoon, Evening)
            [stop-cards nested inside time-blocks]
          <div class="drive-stat">       ← Day driving total
          <div class="hc">              ← Hotel card (last night of this segment)
    <section class="food-strip">
      <div class="food-grid">            ← .fc cards
    <section class="alerts-section">
      <div class="alerts-grid">          ← .ac cards
    <section class="social-section">
      <div class="si-grid">              ← .si-card quotes
    <div class="footer">
```

---

## 4. COMPLETE CSS (shared across all 7 files)

```css
/* BASE */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: Georgia, serif; background: var(--cream); color: var(--dark); }
.wrap { max-width: 820px; margin: 0 auto; padding: 0 16px 48px; }
section { margin: 0 0 36px; }
.section-title { font-family: sans-serif; font-size: .7rem; text-transform: uppercase; letter-spacing: 1.2px; color: var(--mid); font-weight: 700; margin: 32px 0 12px; border-bottom: 1px solid var(--border); padding-bottom: 8px; }
a { color: var(--pacific); }

/* HERO */
.hero { padding: 56px 24px 64px; text-align: center; color: white; position: relative; margin-bottom: 0; }
.hero::after { content: ''; position: absolute; bottom: -1px; left: 0; right: 0; height: 40px; background: var(--cream); clip-path: ellipse(55% 100% at 50% 100%); }
.hero-sup { font-family: sans-serif; font-size: .78rem; text-transform: uppercase; letter-spacing: 1.5px; opacity: .8; margin-bottom: 8px; }
.hero h1 { font-family: Georgia, serif; font-size: 2.8rem; text-shadow: 0 2px 12px rgba(0,0,0,.4); letter-spacing: 1px; margin: 0 0 8px; }
.hero-dates { font-family: sans-serif; font-size: 1.0rem; opacity: .9; margin-bottom: 6px; }
.hero-base { font-family: sans-serif; font-size: .85rem; opacity: .8; margin-bottom: 16px; }
.hero-chips { display: flex; gap: 10px; flex-wrap: wrap; justify-content: center; }
.hchip { font-family: sans-serif; font-size: .76rem; background: rgba(255,255,255,.15); border: 1px solid rgba(255,255,255,.3); border-radius: 20px; padding: 4px 12px; }

/* BOOKING BANNER */
.booking-banner { background: linear-gradient(135deg, #F0FFF4, #EBF8FF); border: 2px solid #68D391; border-radius: 12px; padding: 20px 24px; margin: 24px 0; }
.bb-title { font-family: sans-serif; font-size: .7rem; text-transform: uppercase; letter-spacing: 1px; color: var(--green); font-weight: 700; margin-bottom: 12px; }
.bb-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 12px; }
.bb-item { background: white; border: 1px solid var(--border); border-radius: 8px; padding: 12px 14px; }
.bb-item.confirmed { border-left: 3px solid var(--green); }
.bb-item.pending { border-left: 3px solid #D97706; background: #FFFBEB; }
.bb-name { font-family: sans-serif; font-size: .88rem; font-weight: 700; color: var(--dark); margin: 4px 0 2px; }
.bb-detail { font-family: sans-serif; font-size: .75rem; color: var(--mid); }

/* BADGES */
.badge { font-family: sans-serif; font-size: .68rem; font-weight: 700; padding: 2px 8px; border-radius: 20px; display: inline-block; }
.badge.booked { background: #C6F6D5; color: #276749; border: 1px solid #68D391; }
.badge.pending { background: #FEF3C7; color: #92400E; border: 1px solid #F6AD55; }
.badge.info { background: #EBF8FF; color: #2B6CB0; border: 1px solid #90CDF4; }

/* OVERVIEW STRIP */
.overview-strip { display: grid; grid-template-columns: repeat(auto-fill, minmax(170px, 1fr)); gap: 12px; margin: 24px 0; }
.ov-card { border: 1px solid var(--border); border-radius: 10px; padding: 14px; }
.ov-card.d1 { background: linear-gradient(135deg, #EBF8FF, #E6FFFA); border-color: var(--pacific); }
.ov-card.d2 { background: linear-gradient(135deg, #EBF8FF, #F0FFF4); border-color: var(--coastal); }
.ov-card.d3 { background: linear-gradient(135deg, #FFF9F0, #FFFBEB); border-color: var(--golden); }
.ov-card.d4 { background: linear-gradient(135deg, #F0FFF4, #F0F7EF); border-color: var(--redwood); }
.ov-card.d5 { background: linear-gradient(135deg, #FFF9F0, #FFF5E6); border-color: var(--golden); }
.ov-card.d6 { background: linear-gradient(135deg, #EBF8FF, #E0F0FF); border-color: var(--coastal); }
.ov-card.d7 { background: linear-gradient(135deg, #FFF3E0, #FFF9F0); border-color: var(--sunset); }
.ov-card.d8 { background: linear-gradient(135deg, #FFF3E0, #FFF0EB); border-color: var(--sunset); }
.ov-card.d9 { background: linear-gradient(135deg, #FFF3E0, #FFF9F0); border-color: var(--sunset); }
.ov-card.d10 { background: linear-gradient(135deg, #FFF3E0, #FFF5E0); border-color: var(--golden); }
.ov-date { font-family: sans-serif; font-size: .72rem; font-weight: 700; color: var(--mid); text-transform: uppercase; letter-spacing: .5px; }
.ov-label { font-family: Georgia, serif; font-size: .95rem; color: var(--dark); margin: 3px 0; }
.ov-note { font-family: sans-serif; font-size: .75rem; color: var(--mid); line-height: 1.4; }

/* DAY SECTIONS */
.day-section { margin-bottom: 40px; }
.day-hd { border-radius: 10px 10px 0 0; padding: 16px 20px; color: white; }
.day-hd.sf { background: linear-gradient(135deg, #0B4F6C, #1B7A9E); }
.day-hd.bigsur { background: linear-gradient(135deg, #1A3D2B, #3A6B4A); }
.day-hd.coast { background: linear-gradient(135deg, #5C3A1E, #B7730A); }
.day-hd.sandiego { background: linear-gradient(135deg, #0B4F6C, #0D6B7A); }
.day-hd.la { background: linear-gradient(135deg, #3D1F00, #C05621); }
.day-hd-label { font-family: sans-serif; font-size: .7rem; text-transform: uppercase; letter-spacing: .8px; opacity: .8; }
.day-hd-title { font-family: Georgia, serif; font-size: 1.35rem; margin: 4px 0; }
.day-hd-sub { font-family: sans-serif; font-size: .82rem; opacity: .85; }
.day-body { background: white; border: 1px solid var(--border); border-top: none; border-radius: 0 0 10px 10px; padding: 24px; }

/* TIME BLOCKS */
.time-block { margin-bottom: 22px; }
.tb-hd { font-family: sans-serif; font-size: .72rem; font-weight: 700; text-transform: uppercase; letter-spacing: .8px; padding-bottom: 8px; margin-bottom: 12px; border-bottom: 2px solid; }
.tb-hd.sf { color: var(--pacific); border-color: var(--pacific); }
.tb-hd.bigsur { color: var(--redwood); border-color: var(--redwood); }
.tb-hd.coast { color: var(--golden); border-color: var(--golden); }
.tb-hd.sandiego { color: var(--coastal); border-color: var(--coastal); }
.tb-hd.la { color: var(--sunset); border-color: var(--sunset); }
.tb-list { list-style: none; padding: 0; }
.tb-list li { font-family: sans-serif; font-size: .85rem; line-height: 1.65; padding-left: 14px; margin-bottom: 6px; color: var(--dark); }
.tb-list li::before { content: '→ '; color: var(--pacific); font-weight: 700; margin-left: -14px; }
.tb-list li strong { color: var(--pacific); }
.tb-list li em { color: var(--amber); font-weight: 600; }

/* STOP CARDS (replaces trail cards — no hiking stats needed) */
.stop-card { background: var(--snow); border: 1px solid var(--border); border-radius: 10px; margin-bottom: 16px; overflow: hidden; }
.sc-hd { padding: 14px 16px; border-bottom: 1px solid var(--border); }
.sc-name { font-family: Georgia, serif; font-size: 1.1rem; margin-bottom: 6px; }
.sc-name.sf { color: var(--pacific); }
.sc-name.bigsur { color: var(--redwood); }
.sc-name.coast { color: var(--golden); }
.sc-name.sandiego { color: var(--coastal); }
.sc-name.la { color: var(--sunset); }
.sc-stats { display: flex; flex-wrap: wrap; gap: 6px; }
.sc-stat { font-family: sans-serif; font-size: .72rem; background: var(--cream); border: 1px solid var(--border); border-radius: 20px; padding: 3px 10px; color: var(--mid); }
.sc-stat.booked { background: #C6F6D5; color: #276749; border-color: #68D391; font-weight: 700; }
.sc-stat.pending { background: #FEF3C7; color: #92400E; border-color: #F6AD55; font-weight: 700; }
.sc-stat.free { background: #EBF8FF; color: #2B6CB0; border-color: #90CDF4; }
.sc-body { background: white; padding: 16px; }
.sc-notes p { font-family: sans-serif; font-size: .84rem; line-height: 1.65; color: var(--dark); margin-bottom: 8px; }
.sc-notes p strong { color: var(--pacific); }
.sc-tip { font-family: sans-serif; font-size: .8rem; font-style: italic; padding: 10px 14px; border-left: 3px solid var(--pacific); background: var(--snow); border-radius: 0 6px 6px 0; margin-top: 8px; color: var(--dark); }

/* MAP SECTION */
.map-section { margin: 24px 0; }
.map-embed-wrap { border-radius: 10px; overflow: hidden; margin-bottom: 8px; box-shadow: 0 2px 12px rgba(0,0,0,.1); }
.map-caption { font-family: sans-serif; font-size: .78rem; color: var(--mid); margin-bottom: 12px; line-height: 1.4; }
.map-actions { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px; }
.mab { font-family: sans-serif; font-size: .78rem; font-weight: 600; padding: 8px 16px; border-radius: 8px; text-decoration: none; cursor: pointer; }
.mab.route { background: #1A73E8; color: white; }
.mab.gmaps { background: white; color: #1A73E8; border: 1px solid #1A73E8; }

/* ROUTE STRIP */
.route-strip { display: flex; flex-direction: column; gap: 0; padding: 18px 0; }
.rs-node { display: flex; align-items: flex-start; gap: 14px; padding: 10px 0; }
.rs-badge { width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-family: sans-serif; font-size: .85rem; font-weight: 700; color: white; background: var(--pacific); flex-shrink: 0; }
.rs-badge.home { background: #2D3748; }
.rs-badge.hotel { background: #553C9A; }
.rs-info { flex: 1; }
.rs-name { font-family: sans-serif; font-size: .9rem; font-weight: 700; color: var(--dark); }
.rs-sub { font-family: sans-serif; font-size: .75rem; color: var(--mid); margin-top: 2px; }
.rs-leg { display: flex; align-items: center; gap: 12px; padding-left: 46px; margin: 2px 0; }
.rs-leg-line { width: 2px; height: 28px; background: var(--border); flex-shrink: 0; }
.rs-leg-time { font-family: sans-serif; font-size: .78rem; font-weight: 700; color: var(--pacific); }
.rs-leg-note { font-family: sans-serif; font-size: .68rem; color: var(--mid); }

/* DRIVE STAT */
.drive-stat { font-family: sans-serif; font-size: .82rem; color: var(--mid); background: var(--sand); border-radius: 8px; padding: 10px 16px; margin: 16px 0; }
.drive-val { font-weight: 700; color: var(--pacific); }

/* HOTEL CARD */
.hc { border: 2px solid #68D391; border-radius: 10px; overflow: hidden; margin: 20px 0; }
.hc.tbd { border-color: #F6AD55; }
.hc-hd { background: linear-gradient(135deg, #F0FFF4, #EBF8FF); padding: 14px 16px; border-bottom: 1px solid var(--border); }
.hc.tbd .hc-hd { background: linear-gradient(135deg, #FEF3C7, #FFF9F0); }
.hc-name { font-family: Georgia, serif; font-size: 1.15rem; color: var(--dark); margin: 6px 0 2px; }
.hc-loc { font-family: sans-serif; font-size: .78rem; color: var(--mid); }
.hc-body { background: white; padding: 16px; }
.hc-row { display: flex; gap: 12px; margin-bottom: 7px; align-items: baseline; }
.hc-lbl { font-family: sans-serif; font-size: .68rem; text-transform: uppercase; letter-spacing: .5px; color: var(--mid); font-weight: 700; min-width: 80px; flex-shrink: 0; }
.hc-val { font-family: sans-serif; font-size: .82rem; color: var(--dark); }

/* FOOD GRID */
.food-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(290px, 1fr)); gap: 16px; margin: 16px 0; }
.fc { border-radius: 10px; overflow: hidden; border: 1px solid var(--border); }
.fc-hd { background: linear-gradient(135deg, #0B4F6C, #1B7A9E); padding: 14px 16px; }
.fc-name { font-family: Georgia, serif; font-size: 1.0rem; color: white; }
.fc-loc { font-family: sans-serif; font-size: .72rem; color: rgba(255,255,255,.8); margin-top: 4px; }
.fc-body { background: white; padding: 14px 16px; }
.fc-rating { font-family: sans-serif; font-size: .78rem; color: var(--gold); font-weight: 600; margin-bottom: 6px; }
.fc-order { font-family: sans-serif; font-size: .82rem; color: var(--dark); line-height: 1.5; margin-bottom: 6px; }
.fc-order strong { color: var(--pacific); }
.fc-hours { font-family: sans-serif; font-size: .75rem; color: var(--mid); margin-bottom: 10px; }

/* ALERTS GRID */
.alerts-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 14px; margin: 16px 0; }
.ac { border-radius: 10px; padding: 14px 16px; border: 1px solid var(--border); border-left-width: 4px; }
.ac.red { background: #FEF2F2; border-left-color: var(--red); }
.ac.amb { background: #FFFBEB; border-left-color: #D97706; }
.ac.blu { background: #EBF8FF; border-left-color: #2B6CB0; }
.ac.grn { background: #F0FFF4; border-left-color: var(--green); }
.ac-icon { font-size: 1.2rem; margin-bottom: 6px; }
.ac-title { font-family: sans-serif; font-size: .75rem; font-weight: 700; text-transform: uppercase; letter-spacing: .5px; color: var(--dark); margin-bottom: 4px; }
.ac-text { font-family: sans-serif; font-size: .8rem; color: var(--mid); line-height: 1.5; }

/* SOCIAL INTEL */
.si-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 12px; margin: 16px 0; }
.si-card { background: var(--snow); border: 1px solid var(--border); border-radius: 8px; padding: 12px 14px; }
.si-quote { font-family: Georgia, serif; font-size: .85rem; color: var(--dark); font-style: italic; margin-bottom: 6px; line-height: 1.5; }
.si-source { font-family: sans-serif; font-size: .7rem; color: var(--pacific); font-weight: 600; }
.si-location { font-family: sans-serif; font-size: .7rem; color: var(--mid); margin-top: 2px; }

/* FOOTER */
.footer { background: var(--pacific); color: rgba(255,255,255,.6); text-align: center; font-family: sans-serif; font-size: .77rem; padding: 22px 24px; margin-top: 48px; border-radius: 10px; }
.footer strong { color: white; }

/* RESPONSIVE */
@media (max-width: 600px) {
  .hero h1 { font-size: 2.0rem; }
  .day-hd-title { font-size: 1.1rem; }
  .overview-strip { grid-template-columns: 1fr 1fr; }
  .bb-grid, .alerts-grid, .food-grid, .si-grid { grid-template-columns: 1fr; }
  .hc-row { flex-direction: column; gap: 2px; }
}
```

---

## 5. COMPONENT TEMPLATES

### 5.1 HERO

```html
<div class="hero" style="background: linear-gradient(160deg, #0B4F6C, #1B7A9E, #3A6B4A);">
  <div class="hero-sup">California Road Trip · San Francisco → Los Angeles</div>
  <h1>San Francisco</h1>
  <div class="hero-dates">July 2–5, 2026 · 3 Nights</div>
  <div class="hero-base">Base: Hyatt Regency SF · 50 Third St, Union Square</div>
  <div class="hero-chips">
    <span class="hchip">3 nights</span>
    <span class="hchip">✅ Booked · Conf. 40023B19345813</span>
    <span class="hchip">Days 1–3 · Jul 2–5</span>
    <span class="hchip">Check-in: 3:00 PM · Check-out: 12:00 PM</span>
  </div>
</div>
```

### 5.2 BOOKING BANNER

```html
<div class="booking-banner">
  <div class="bb-title">Booking Status</div>
  <div class="bb-grid">
    <div class="bb-item confirmed">
      <span class="badge booked">✅ Booked</span>
      <div class="bb-name">Alcatraz Ferry</div>
      <div class="bb-detail">Conf. i77487162 · Jul 3 · 9:20 AM · Pier 33</div>
    </div>
    <div class="bb-item pending">
      <span class="badge pending">⚠️ Not Yet Booked</span>
      <div class="bb-name">Scoma's Birthday Dinner</div>
      <div class="bb-detail">OpenTable or (415) 771-4383 · Jul 4 evening · URGENT</div>
    </div>
  </div>
</div>
```

### 5.3 OVERVIEW STRIP

```html
<div class="overview-strip">
  <div class="ov-card d1">
    <div class="ov-date">Thu, Jul 2</div>
    <div class="ov-label">Day 1 — Arrival</div>
    <div class="ov-note">SFO 11:27 AM · Chinatown · Palace of Fine Arts · Cable Car · Twin Peaks sunset</div>
  </div>
  <div class="ov-card d2">
    <div class="ov-date">Fri, Jul 3</div>
    <div class="ov-label">Day 2</div>
    <div class="ov-note">Alcatraz 9:20 AM · Fort Point · UC Berkeley · Muir Woods 4:00 PM</div>
  </div>
  <div class="ov-card d3">
    <div class="ov-date">Sat, Jul 4 🎂</div>
    <div class="ov-label">Day 3 — Birthday</div>
    <div class="ov-note">Bouchon Bakery · Sterling Vineyards 10:45 AM · Napa/Oxbow · Scoma's dinner</div>
  </div>
</div>
```

### 5.4 MAP SECTION (Google Maps Embed + Route Strip)

**One embed per DAY. `{{GMAPS_KEY}}` is injected by build_california.py — never hardcode.**

```html
<div class="map-section">
  <div class="map-embed-wrap">
    <iframe
      width="100%" height="380"
      style="border:0;"
      loading="lazy"
      allowfullscreen
      src="https://www.google.com/maps/embed/v1/directions?key={{GMAPS_KEY}}&origin=50+Third+St+San+Francisco+CA&destination=50+Third+St+San+Francisco+CA&waypoints=6528+Washington+St+Yountville+CA|1111+Dunaweal+Ln+Calistoga+CA|610+1st+St+Napa+CA&mode=driving">
    </iframe>
  </div>
  <p class="map-caption">Day 3 route: Hyatt SF → Bouchon Bakery (Yountville) → Sterling Vineyards (Calistoga) → Napa Oxbow Public Market → return SF · ~4h total driving</p>
  <div class="route-strip">
    <div class="rs-node start">
      <span class="rs-badge home">🏠</span>
      <div class="rs-info">
        <div class="rs-name">Hyatt Regency SF</div>
        <div class="rs-sub">Starting point · Jul 4 Sat · Depart 8:00 AM</div>
      </div>
    </div>
    <div class="rs-leg">
      <div class="rs-leg-line"></div>
      <div class="rs-leg-time">61 min · 54.5 mi</div>
      <div class="rs-leg-note">Routes API · Jul 4 Sat 8:00 AM with traffic</div>
    </div>
    <div class="rs-node">
      <span class="rs-badge">1</span>
      <div class="rs-info">
        <div class="rs-name">Bouchon Bakery, Yountville</div>
        <div class="rs-sub">45 min · Takeout · Opens 7 AM · Depart 9:46 AM</div>
      </div>
    </div>
    <div class="rs-leg">
      <div class="rs-leg-line"></div>
      <div class="rs-leg-time">26 min · 17.0 mi</div>
      <div class="rs-leg-note">Routes API · Jul 4 Sat ~9:46 AM with traffic</div>
    </div>
    <div class="rs-node">
      <span class="rs-badge">2</span>
      <div class="rs-info">
        <div class="rs-name">Sterling Vineyards, Calistoga</div>
        <div class="rs-sub">✅ Booked · 10:45 AM · Conf. TOCK-R-AE87DB44 · $192.53 paid · ~1 hour</div>
      </div>
    </div>
    <div class="rs-leg">
      <div class="rs-leg-line"></div>
      <div class="rs-leg-time">38 min · 27.5 mi</div>
      <div class="rs-leg-note">Routes API · Jul 4 Sat ~noon</div>
    </div>
    <div class="rs-node">
      <span class="rs-badge">3</span>
      <div class="rs-info">
        <div class="rs-name">Napa Oxbow Public Market</div>
        <div class="rs-sub">610 1st St, Napa · Hog Island Oyster Bar · Arrive ~12:38 PM</div>
      </div>
    </div>
    <div class="rs-leg">
      <div class="rs-leg-line"></div>
      <div class="rs-leg-time">~74 min · 46.3 mi</div>
      <div class="rs-leg-note">Routes API · Jul 4 Sat PM (heavy traffic)</div>
    </div>
    <div class="rs-node overnight">
      <span class="rs-badge hotel">🏨</span>
      <div class="rs-info">
        <div class="rs-name">Hyatt Regency SF + Scoma's Dinner</div>
        <div class="rs-sub">Pier 47, Al Scoma Way · ⚠️ Book now · July 4 fireworks after dinner</div>
      </div>
    </div>
  </div>
  <div class="map-actions">
    <a href="https://www.google.com/maps/dir/50+Third+St+San+Francisco/6528+Washington+St+Yountville/1111+Dunaweal+Ln+Calistoga/610+1st+St+Napa/50+Third+St+San+Francisco" target="_blank" class="mab route">Open Day 3 Route in Google Maps →</a>
  </div>
</div>
```

### 5.5 DAY SECTION WRAPPER

```html
<div class="day-section">
  <div class="day-hd sf">
    <div class="day-hd-label">Friday, July 3, 2026</div>
    <div class="day-hd-title">Alcatraz · Fort Point · UC Berkeley · Muir Woods</div>
    <div class="day-hd-sub">Drive total: ~3h 46m verified · Depart hotel 8:35 AM</div>
  </div>
  <div class="day-body">
    <!-- map-section, time-blocks, stop-cards, drive-stat, hc go here -->
  </div>
</div>
```

### 5.6 TIME BLOCK + STOP CARD

```html
<div class="time-block">
  <div class="tb-hd sf">Morning — Depart 8:35 AM</div>
  <ul class="tb-list">
    <li><strong>Depart hotel 8:35 AM</strong> — Pier 33 is 1.5 miles away. 45-minute arrival deadline before 9:20 AM departure.</li>
    <li>⚠️ No parking at Pier 33. Take rideshare or walk (18 min via Embarcadero).</li>
  </ul>
  <div class="stop-card">
    <div class="sc-hd">
      <div class="sc-name sf">Alcatraz Island — Audio Tour</div>
      <div class="sc-stats">
        <span class="sc-stat">Pier 33 · 9:20 AM departure</span>
        <span class="sc-stat booked">✅ Booked · Conf. i77487162</span>
        <span class="sc-stat">Return ~12:00 PM</span>
      </div>
    </div>
    <div class="sc-body">
      <div class="sc-notes">
        <p>Audio tour ~2.5 hours. The cell house narrated by former guards and prisoners is exceptional — do the full route including recreation yard and library. Bring headphones and fully charge your phone the night before.</p>
        <p>⚠️ <strong>Arrive at Pier 33 by 8:35 AM</strong> — 45 min before departure. No parking. No weapons. Non-refundable.</p>
      </div>
      <div class="map-actions">
        <a href="https://www.google.com/maps/search/?api=1&query=Pier+33+Alcatraz+Landing+San+Francisco+CA+94133" target="_blank" class="mab gmaps">📍 Pier 33 Alcatraz Landing</a>
      </div>
      <div class="sc-tip">Bring: Headphones (app-based audio), fully charged phone, backpack max 16"×20", closed-toe shoes. QR code is valid for entire party.</div>
    </div>
  </div>
</div>
```

### 5.7 DRIVE STAT

```html
<div class="drive-stat">
  <span class="drive-val">3h 46m driving</span> · Depart 8:35 AM · Return SF ~7:10 PM · All times Routes API verified with traffic
</div>
```

### 5.8 HOTEL CARD (confirmed)

```html
<div class="hc">
  <div class="hc-hd">
    <span class="badge booked">✅ Booked · Prepaid</span>
    <div class="hc-name">Hyatt Regency San Francisco</div>
    <div class="hc-loc">50 Third St, Union Square · San Francisco, CA 94103</div>
  </div>
  <div class="hc-body">
    <div class="hc-row"><span class="hc-lbl">Conf #</span><span class="hc-val">40023B19345813 · Marina Drapkin · World of Hyatt</span></div>
    <div class="hc-row"><span class="hc-lbl">Check-in</span><span class="hc-val">Thu Jul 2 · 3:00 PM</span></div>
    <div class="hc-row"><span class="hc-lbl">Check-out</span><span class="hc-val">Sun Jul 5 · 12:00 PM</span></div>
    <div class="hc-row"><span class="hc-lbl">Rate</span><span class="hc-val">$157.46 (Jul 2) + $184.92 (Jul 3) + $184.92 (Jul 4) = $527.30 + taxes · NON-REFUNDABLE</span></div>
    <div class="hc-row"><span class="hc-lbl">Room</span><span class="hc-val">2 Queen Beds · Yerba Buena Park or City View · 55" SMART TV · Technology Hub</span></div>
    <div class="hc-row"><span class="hc-lbl">Amenities</span><span class="hc-val">La Société restaurant · private parking (fee TBD) · fitness center · free WiFi · 24hr desk · ATM</span></div>
    <div class="map-actions" style="margin-top:10px;">
      <a href="https://www.google.com/maps/search/?api=1&query=50+Third+St+San+Francisco+CA+94103" target="_blank" class="mab gmaps">📍 Hotel on Google Maps</a>
    </div>
  </div>
</div>
```

### 5.9 HOTEL CARD (TBD — LA only)

```html
<div class="hc tbd">
  <div class="hc-hd">
    <span class="badge pending">⚠️ Not Yet Booked</span>
    <div class="hc-name">Los Angeles Hotel — TBD</div>
    <div class="hc-loc">Neighborhood TBD · Culver City / Hollywood / Downtown / Koreatown</div>
  </div>
  <div class="hc-body">
    <div class="hc-row"><span class="hc-lbl">Dates</span><span class="hc-val">Wed Jul 8 – Sat Jul 11 · 3 nights</span></div>
    <div class="hc-row"><span class="hc-lbl">Status</span><span class="hc-val" style="color:var(--amber);font-weight:700;">⚠️ Mom researching budget options — booking pending</span></div>
    <div class="hc-row"><span class="hc-lbl">Budget</span><span class="hc-val">Avoid Beverly Hills, Santa Monica, West Hollywood (too expensive for 3 nights)</span></div>
  </div>
</div>
```

---

## 6. BUILD_CALIFORNIA.PY

Copy `build.py` and make exactly these changes:

```python
# Line 44–52: Replace MANUAL_FILES
MANUAL_FILES = [
    "./california-routes.html",
    "./sf-guide.html",
    "./bigsur-guide.html",
    "./centralcoast-guide.html",
    "./sandiego-guide.html",
    "./la-guide.html",
]

# Line 55: Change OUTPUT_FILE
OUTPUT_FILE = "./docs/california-viewer.html"

# Line 59: Change VIEWER_TITLE
VIEWER_TITLE = "California Road Trip · San Francisco → Los Angeles · July 2026"
```

Add Google Maps key injection after the `pages` array is built (after line ~370, before write):

```python
# Inject Google Maps API key from .env
import os
gmaps_key = ""
if os.path.exists('.env'):
    with open('.env') as f:
        for line in f:
            if line.startswith('GOOGLE_MAPS_API_KEY='):
                gmaps_key = line.split('=', 1)[1].strip()
                break
pages = [p.replace('{{GMAPS_KEY}}', gmaps_key) for p in pages]
```

**Output:** `./docs/california-viewer.html`
**GitHub Pages URL:** `https://AdamDrapkin.github.io/grand-american-loop/docs/california-viewer.html`
**Remote:** `https://github.com/AdamDrapkin/grand-american-loop.git`

---

## 7. VERIFIED DRIVING TIMES (use these exactly — do not recalculate)

| Leg | Verified | Miles |
|---|---|---|
| Pier 33 → Fort Point (Jul 3 Fri ~noon) | **17 min** | 4.4 |
| Fort Point → UC Berkeley (Jul 3 Fri ~1:15 PM) | **48 min** | 29.9 |
| UC Berkeley → Muir Woods (Jul 3 Fri ~3:30 PM) | **65 min** | 28.2 |
| Muir Woods → Hyatt SF (Jul 3 Fri ~7:00 PM) | **56 min** | 18.7 |
| Hyatt SF → Yountville (Jul 4 Sat 8:00 AM) | **61 min** | 54.5 |
| Yountville → Sterling (Jul 4 Sat ~9:46 AM) | **26 min** | 17.0 |
| Sterling → Napa City (Jul 4 Sat ~noon) | **38 min** | 27.5 |
| Napa City → Hyatt SF (Jul 4 Sat PM) | **~74 min** | 46.3 |
| Hyatt SF → 17-Mile Drive (Jul 5 Sun 7:00 AM) | **1h 53m** | 123.9 |
| 17-Mile Drive → Carmel | **3 min** | 0.5 |
| Carmel → Point Lobos (Jul 5 Sun ~11 AM) | **13 min** | 4.3 |
| Point Lobos → Bixby Bridge (Jul 5 Sun ~12:15 PM) | **19 min** | 11.2 |
| Bixby → Hurricane Point | **1 min** | 0.7 |
| Hurricane Point → Pfeiffer Beach (Jul 5 Sun ~1:30 PM) | **33 min** | 15.3 |
| Pfeiffer Beach → McWay Falls (Jul 5 Sun ~2:30 PM) | **25 min** | 11.9 |
| McWay Falls → Elephant Seals (Jul 5 Sun ~3:30 PM) | **1h 17m** | 57.3 |
| Elephant Seals → Cambria (Jul 5 Sun ~6:00 PM) | **25 min** | 20.0 |
| Cambria → Hearst Castle (Jul 6 Mon ~8:45 AM) | **15 min** | 9.6 |
| Hearst Castle → Solvang (Jul 6 Mon ~noon) | **1h 54m** | 108.1 |
| Solvang → Santa Barbara (Jul 6 Mon ~2:30 PM) | **45 min** | 33.3 |
| Santa Barbara → El Matador (Jul 7 Tue 8:00 AM) | **1h 5m** | 60.7 |
| El Matador → Newport Beach (Jul 7 Tue ~10:30 AM) | **1h 40m** | 76.7 |
| Newport → Laguna Beach (Jul 7 Tue ~12:15 PM) | **23 min** | 10.7 |
| Laguna Beach → San Diego/Coronado (Jul 7 Tue ~1:30 PM) | **1h 24m** | 79.3 |
| Coronado → LA/Beverly Hills (Jul 8 Wed ~noon) | **2h 31m** | 139.7 |

Display format in route strip: `N min · X.X mi` with sub-note `Routes API · [day] [time] with traffic`

---

## 8. CONTENT DATA — ALL 5 SEGMENTS

### SF (Jul 2–5)

**Hotel:** Hyatt Regency SF · 50 Third St, Union Square, SF, CA 94103
- Conf: 40023B19345813 · Check-in Jul 2 3:00 PM · Check-out Jul 5 12:00 PM
- $157.46 + $184.92 + $184.92 = $527.30 + taxes · NON-REFUNDABLE
- Room: 2 Queen Beds · Yerba Buena Park/City View · 55" TV
- Amenities: La Société restaurant · private parking (fee) · fitness center · free WiFi · 24hr desk

**Day 1 — Thu Jul 2 (Arrival)**
- AA 1524 SFO 11:27 AM (Marina & Liam) · car pickup ~12:15 PM · arrive SF ~1:00 PM
- Chinatown (Grant Ave + Stockton St) — 45 min–1 hr
- Palace of Fine Arts (3601 Lyon St) — 30–45 min · free
- Powell-Hyde Cable Car (Powell & Market turnaround) — all-day Muni passport $24/adult
- Lombard Street (Russian Hill) — 20 min · free
- Painted Ladies (710-720 Steiner St, Alamo Square Park) — 20 min · free
- Twin Peaks SUNSET — 20 min · free (or Mission Dolores Park)
- Dinner: North Beach (Broadway + Columbus Ave) or Ferry Building — no confirmed restaurant

**Day 2 — Fri Jul 3**
- ✅ Alcatraz Ferry · Conf. i77487162/77487159 · 9:20 AM depart · Pier 33 Alcatraz Landing, SF 94133 · arrive by 8:35 AM · return ~12:00 PM · 4 adults · no parking at Pier 33
- ✅ Fort Point NHS · 201 Marine Dr · FREE · 10 AM–5 PM Fri · 45–55 min · depart by ~1:15 PM
- UC Berkeley: Campanile $5/person · Sproul Plaza free · depart 3:00 PM
- ✅ Muir Woods · gomuirwoods.com · 4:00–4:30 PM parking slot · $15/person · Cathedral Grove Trail 1 mi flat · no cell service · auto-theft warning
- Return to SF ~7:10 PM

**Day 3 — Sat Jul 4 (Adam's 22nd Birthday) 🎂**
- Depart Hyatt 8:00 AM
- Bouchon Bakery (6528 Washington St, Yountville) · Opens 7 AM · arrive 9:01 AM · 45 min takeout · depart 9:46 AM · Croissants, TKO cookies, pastries
- ✅ Sterling Vineyards (1111 Dunaweal Ln, Calistoga) · Conf. TOCK-R-AE87DB44 · 10:45 AM (arrive 10:30) · ~1 hr · Sterling Stroll ×2 + Non-taster ×1 + Guest 10–20 ×1 · $192.53 paid Visa 9942 · Gondola pauses >100°F
- Napa Oxbow Public Market (610 1st St, Napa) · arrive ~12:38 PM · Hog Island Oyster Bar
- ⚠️ Scoma's Restaurant (Pier 47, Al Scoma Way, SF) · OpenTable or (415) 771-4383 · Sat 12–10 PM (call for Jul 4 hours) · ~$250–350 family · MUST BOOK NOW · July 4 fireworks from Fisherman's Wharf after dinner

---

### BIG SUR / CAMBRIA (Jul 5)

**Hotel:** Castle Inn · 6620 Moonstone Beach Dr, Cambria, CA 93428 · +1 805-927-8605
- Booking.com · Conf. 6459555758 · PIN: 8199 (confidential)
- 4 adults · 2-Queen Partial Oceanview
- Check-in: Jul 5 3:00–9:00 PM · Check-out: Jul 6 7:30–11:00 AM
- $244.00 + $30.50 tax = $274.50 PREPAID · Breakfast INCLUDED
- Free cancel until Jul 2 11:59 PM PDT; after Jul 3: full charge

**Day 4 — Sun Jul 5 (Marathon Drive — Depart SF 7:00 AM)**

| Stop | Drive | Cost | Notes |
|---|---|---|---|
| 17-Mile Drive (Pacific Grove Gate) | 1h 53m · 123.9 mi | $12.25/vehicle | Ghost Tree, Lone Cypress, Pebble Beach views · exit Carmel Gate · 45 min–1 hr |
| Carmel-by-the-Sea | 3 min · 0.5 mi | Free | Ocean Ave, Sunset Beach, Clinton Walker House (FLW) · 45 min–1 hr |
| Point Lobos State Reserve | 13 min · 4.3 mi | $10/vehicle | ⚠️ NOT BOOKED — reservecalifornia.com · China Cove Bird Island Trail 1 mi · sea lions, otters, seals · 1–1.5 hrs |
| Bixby Creek Bridge | 19 min · 11.2 mi | Free | North turnout for full frame · @luke_eich 109K views · 15–20 min |
| Hurricane Point | 1 min · 0.7 mi | Free | Dramatic headland · 15 min |
| Pfeiffer Beach | 33 min · 15.3 mi | $12/vehicle cash | Sycamore Canyon Rd (unmarked, 0.5 mi N of Big Sur station) · purple sand · Keyhole Arch · 1–1.5 hrs |
| McWay Falls (Julia Pfeiffer Burns SP) | 25 min · 11.9 mi | $12/vehicle | Overlook Trail 0.5 mi flat · 80-ft waterfall onto beach · 45 min–1 hr |
| Secret Swing/Plasket Ridge (opt.) | ~30 min detour | — | ✅ 4WD confirmed · tree swing above clouds |
| Elephant Seal Vista Point (Piedras Blancas) | 1h 17m · 57.3 mi | Free | July = juveniles/sub-adults · paved platform · 30 min |
| Castle Inn, Cambria | 25 min · 20.0 mi | — | Arrive ~6:21 PM |

**Total Day 4:** ~4h 36m driving · Depart 7:00 AM · Arrive ~6:21 PM

---

### CENTRAL COAST / SANTA BARBARA (Jul 6)

**Hotel:** Beachside Inn · 336 W Cabrillo Blvd, Santa Barbara, CA 93101 · (805) 965-6556
- Direct (beachsideinn.com) · Conf. 1075827673
- Guest: Marina Drapkin · marin4ik10@gmail.com · Visa 9942
- Room: 2 Queen Beds · Parkside with Balcony (Plaza Del Mar view)
- Check-in: Jul 6 after 4:00 PM · Check-out: Jul 7 before 12:00 PM
- $240.00 + $34.07 tax = $274.07 · Breakfast INCLUDED · Free parking · Wine & cheese happy hour nightly
- Incidentals: $150 deposit at check-in (credit/debit) · Free cancel until Jul 5; after: first night + tax

**Day 5 — Mon Jul 6 (Depart Cambria ~8:45 AM)**

| Stop | Drive | Cost | Notes |
|---|---|---|---|
| Hearst Castle (750 Hearst Castle Rd, San Simeon) | 15 min · 9.6 mi | ~$30/adult | ⚠️ NOT BOOKED — hearstcastle.org · first slot 9:30–10:00 AM · Grand Rooms Tour 1.5–2 hrs |
| Solvang | 1h 54m · 108.1 mi | — | Ostrichland USA (610 E Hwy 246) · windmill · aebleskivers · 1–1.5 hrs |
| Santa Barbara | 45 min · 33.3 mi | — | Arrive ~3:15 PM · hotel opens 4:00 PM |

**Santa Barbara (all walkable):**
- Old Mission Santa Barbara (2201 Laguna St) — $10/adult · twin bell towers
- El Presidio State Historic Park (123 E Canon Perdido St) — FREE
- Santa Barbara County Courthouse — FREE · clock tower panorama
- MOXI Wolf Museum (125 State St) — admission fee
- State Street + Stearns Wharf — free
- Funk Zone dinner (near train station — wine, breweries, restaurants)

**Food — Santa Barbara Fish Market:**
- 117 Harbor Way, Santa Barbara, CA 93109 · (805) 965-9564
- Mon–Fri 9 AM–6:30 PM · Sat 7:30 AM–6:30 PM · Sun 9 AM–6:30 PM
- Specialty: Santa Barbara Channel Islands red sea urchin (local divers to this market)
- Order: Fresh uni (tray/shell), live rock crab, oysters, lobster
- Est. cost: $60–100 family · Eat at the harbor

---

### SAN DIEGO / CORONADO (Jul 7)

**Hotel:** Best Western Plus Suites Hotel Coronado Island · 275 Orange Ave, Coronado, CA 92118
- Phone: +1 619-437-1666 · Booking.com PAID IN FULL
- Conf. 6459555758 · PIN: 8199 (confidential) · Guest: Marina Drapkin · 4 adults
- Room: Suite with Two Queen Beds · Non-Smoking
- Check-in: Jul 7 3:00 PM · Check-out: Jul 8 12:00 PM
- $279.20 + $27.92 tax = $307.12 PAID IN FULL · Grab-and-go breakfast included
- Damage deposit: $250 hold at check-in (refunded at checkout)
- ⚠️ POOL & HOT TUB CLOSED UNTIL DECEMBER — explicitly flag this in the HTML
- Free cancel until Jul 3 11:59 PM PDT; after Jul 4: full charge
- Location: 0.5 mi from Coronado Beach · 10–15 min from Downtown SD via Coronado Bridge

**Day 6 — Tue Jul 7 (Depart Santa Barbara 8:00 AM)**

| Stop | Drive | Cost | Notes |
|---|---|---|---|
| El Matador Beach (32215 PCH, Malibu) | 1h 5m · 60.7 mi | $8–12/vehicle | Arrive before 10 AM (lot fills 10:30 AM) · sea stacks, sandstone caves, rock arches · 1.5–2 hrs |
| Newport Beach / Balboa Island | 1h 40m · 76.7 mi | — | Marine Ave · Balboa Bar (frozen vanilla ice cream 1945) · Newport Pier · 1–1.5 hrs |
| Laguna Beach | 23 min · 10.7 mi | — | Heisler Park (clifftop) · Main Beach · 1–1.5 hrs |
| Coronado | 1h 24m · 79.3 mi | — | Arrive ~6:00–7:00 PM |

**Evening:** Little Italy (5 min via Coronado Bridge) or Old Town San Diego

---

### LOS ANGELES (Jul 8–11)

**Hotel: TBD — DO NOT INVENT DETAILS. Show stub banner only.**
- 3 nights (Jul 8–11) · Not yet booked
- Mom researching: Culver City / Hollywood / Downtown / Koreatown
- Avoid: Beverly Hills, Santa Monica, West Hollywood

**Drive from Coronado: 2h 31m · 139.7 mi (Jul 8 Wed ~noon, I-5 N → I-405 N)**
**Arrive LA: ~2:30–3:00 PM**

**Day 7 — Wed Jul 8:** Afternoon arrival only. Settle in, explore neighborhood.

**Day 8 — Thu Jul 9:**
- Morning: Beverly Hills — Rodeo Drive, residential streets, Beverly Hills Hotel
- Midday: Hollywood Walk of Fame (15 blocks, La Brea to Gower) · Chinese Theatre (handprints/footprints) · Walt Disney Concert Hall (111 S Grand Ave, free exterior) · Dolby Theatre
- Evening: Sunset Strip / Little Tokyo / Grand Central Market (open to 10 PM)

**Day 9 — Fri Jul 10:**
- Morning: Griffith Observatory (2800 E Observatory Rd) · free admission · opens 10 AM · Planetarium $10/adult · Hollywood Sign view from front lawn · Mt. Hollywood Trail 2.5 mi easy
- Afternoon: Santa Monica Pier (Route 66 end, free) → Venice Boardwalk → Abbot Kinney Blvd
- Evening: Venice / Culver City / Malibu dinner

**Day 10 — Sat Jul 11 (Last full day):**
- ✅ Santa Monica Farmers Market · Arizona Ave & 3rd St · 8 AM–1 PM · 40+ organic farms · $30–50 family
- ⚠️ Getty Center — NOT BOOKED · getty.edu · free admission · timed entry required
- ⚠️ Final LA dinner — NOT BOOKED · Options: Nobu Malibu, Bestia, Republique, Craig's · book 1–2 weeks advance
- Pack tonight

**Departure — Sun Jul 12:**
- Leave hotel no later than 9:00 AM
- In-N-Out Burger (9149 S Sepulveda Blvd, ~0.2 mi from LAX) · Double-Double Animal Style · Fries well-done or Animal Style
- Marina & Liam: AA 3319 · 12:17 PM → PHL 8:39 PM · Seats 28E/28F · Conf. KYUXME · Terminal 4
- Adam & Vadim: drive home after drop-off

---

## 9. SOCIAL INTELLIGENCE (use in .si-card elements)

| Location | Creator | Followers | Views | Quote |
|---|---|---|---|---|
| Bixby Creek Bridge | @luke_eich | 106K | 109,341 | "Most Majestic Bridge I've ever seen" |
| McWay Falls | @wanderingcreator_meghana | 134K | 73,988 | "One of the most dramatic views in California" |
| Pfeiffer Beach | @scenic_adventure_travel | 295K | 187,076 | Purple sand — world-class unique |
| Carmel-by-the-Sea | @globetrottingsu | 195K | 119,337 | "Mini Guide to Carmel-By-The-Sea" |
| Carmel-by-the-Sea | @wellnesstravelled | 611K | 17,064 | "Real life Hansel and Gretel" |
| El Matador Beach | @visitcalifornia | 825K | 8,150 | "High tides and good vibes" |
| Sterling Vineyards | @discover_california_ | 246K | 109,398 | Gondola tram is the signature |
| Alcatraz | @heatherr.eats | 27K | 9,806 | "Audio tour like going back in time" |
| Griffith Observatory | @thisblisslife | 4K | 319 | "Sunset = best views. Arrive early." |
| Solvang | @a.nj.a.l.i._ | 122K | 14,488 | "Stepped into Solvang, suddenly Denmark" |
| Santa Barbara Fish Market | @rockstareater | 80K | 13,104 | "Best fish market in Santa Barbara" |
| Fort Point | @modicumofjoy | — | 377,503 plays / 23,170 likes | Under the Golden Gate arch |
| Venice/Santa Monica | @mini.jetsetter | 291K | 23,338 | "LOS ANGELES WITH KIDS GUIDE" |

---

## 10. PENDING ITEMS (show as .ac.amb or .ac.red alerts in HTML)

**URGENT — must book before Jul 3:**
- ⚠️ Scoma's Restaurant (Jul 4 evening) — OpenTable or (415) 771-4383 — JULY 4 FILLS COMPLETELY
- ⚠️ LA Hotel (Jul 8–11, 3 nights) — Mom researching neighborhoods

**Book within 1–2 weeks:**
- ⚠️ Point Lobos State Reserve (Jul 5) — reservecalifornia.com · $10/vehicle
- ⚠️ Hearst Castle Tour (Jul 6, 9:30 AM slot) — hearstcastle.org · ~$30/adult
- ⚠️ Getty Center timed entry (Jul 10–11) — getty.edu · free
- ⚠️ LA final dinner (Jul 11) — Nobu Malibu / Bestia / Republique / Craig's

**Calls to verify:**
- Scoma's (415) 771-4383 — Jul 4 hours confirmation
- Santa Monica Seafood (310) 393-5244 — hours

---

## 11. WHAT NOT TO DO

- Do NOT invent hotel details for LA — stub only
- Do NOT recalculate any drive times — use the verified table above
- Do NOT include trail cards (difficulty ratings, elevation gain) — California has no hikes
- Do NOT touch `build.py`, `docs/index.html`, or any pre-California HTML files
- Do NOT hardcode `{{GMAPS_KEY}}` — it is injected by `build_california.py` from `.env`
- Do NOT put map embeds on `california-routes.html` (hub page has no route map)
- Output goes to `docs/california-viewer.html` — NOT `dist/`

---

## 12. VERIFICATION CHECKLIST (run after `python3 build_california.py`)

- [ ] `docs/california-viewer.html` opens in browser
- [ ] All 6 slides navigate via arrows and keyboard
- [ ] All Google Maps Embed iframes load (not showing API key errors)
- [ ] All booking banners show correct confirmation numbers
- [ ] Pending items show amber ⚠️ badges
- [ ] All drive times match verified table exactly
- [ ] LA segment shows TBD placeholder — no invented content
- [ ] Pool closed warning visible on San Diego segment
- [ ] Mobile layout works at 375px
- [ ] Pre-California `docs/index.html` is UNCHANGED
- [ ] Push to GitHub: `git add california-routes.html sf-guide.html bigsur-guide.html centralcoast-guide.html sandiego-guide.html la-guide.html build_california.py docs/california-viewer.html`
- [ ] GitHub Pages URL resolves: `https://AdamDrapkin.github.io/grand-american-loop/docs/california-viewer.html`

---

## 13. GOOGLE MAPS LINK FORMAT (coordinate-based — mandatory)

Text-based Maps links break inside the viewer's `<iframe sandbox>`. **Always use coordinate-based URLs.** This applies to all new HTML files and when updating existing ones.

### Individual pin button
```html
<a href="https://www.google.com/maps/search/?api=1&query=LAT,LON" target="_blank" class="mab gmaps">📍 Place Name</a>
```
Opens the Maps app on mobile and drops a pin at the exact coordinates.

### Day route button
```html
<a href="https://www.google.com/maps/dir/LAT1,LON1/LAT2,LON2/LAT3,LON3" target="_blank" class="mab route">Open Day N Route in Google Maps →</a>
```
Opens navigation with all waypoints. Use as many `/LAT,LON` segments as needed.

### Getting coordinates
Run `fix_maps_coords.py` (project root) to batch-geocode all locations in all California guides using the `GOOGLE_MAPS_API_KEY` from `.env`. It reads every `maps/search/TEXT` and `maps/dir/TEXT/TEXT/...` URL, geocodes each text segment via the Google Geocoding API, and rewrites the files in place. Run it then rebuild the viewer.

```bash
python3 fix_maps_coords.py
python3 build_california.py
```

Do not hardcode coordinates manually. Run the script whenever new destinations are added.

---

## 14. PHOTO CAROUSELS — Wikipedia REST API approach (future iteration)

If photo carousels are added to confirmed activities, use the **Wikipedia REST media-list endpoint**, not Wikimedia Commons search (Commons search is unreliable and rate-limited).

### Endpoint
```
GET https://en.wikipedia.org/api/rest_v1/page/media-list/{ARTICLE_NAME}
```
Returns a JSON list of images from the article's gallery. These are curated, always on-topic, and do not require authentication.

### Image selection filter
```python
def fetch_article_images(article, count=3):
    url = f"https://en.wikipedia.org/api/rest_v1/page/media-list/{urllib.parse.quote(article)}"
    with urllib.request.urlopen(url, timeout=10) as r:
        items = json.loads(r.read()).get("items", [])
    
    SKIP_WORDS = {"icon", "logo", "map", "seal", "flag", "coat", "symbol", "diagram", "locator"}
    urls = []
    for item in items:
        if not item.get("showInGallery"):
            continue
        title = item.get("title", "").lower()
        if any(w in title for w in SKIP_WORDS):
            continue
        # Pick largest srcset entry
        srcset = item.get("srcset", [])
        if not srcset:
            continue
        src = srcset[-1].get("src", "")
        if not src:
            continue
        if src.startswith("//"):
            src = "https:" + src
        # Minimum width 400px from srcset width
        width = srcset[-1].get("width", 0)
        if width < 400:
            continue
        urls.append(src)
        if len(urls) >= count:
            break
    return urls
```

### Carousel CSS
```css
.photo-carousel{position:relative;width:100%;height:220px;overflow:hidden;border-radius:8px;margin:10px 0 12px;background:#ccc}
.pc-track{display:flex;height:100%;transition:transform .35s ease}
.pc-track img{min-width:100%;height:220px;object-fit:cover;flex-shrink:0}
.pc-btn{position:absolute;top:50%;transform:translateY(-50%);background:rgba(0,0,0,.45);border:none;color:#fff;font-size:1.2rem;cursor:pointer;padding:6px 10px;border-radius:4px;z-index:2}
.pc-prev{left:7px}.pc-next{right:7px}
.pc-dots{position:absolute;bottom:7px;left:50%;transform:translateX(-50%);display:flex;gap:5px}
.pc-dot{width:7px;height:7px;border-radius:50%;background:rgba(255,255,255,.5);cursor:pointer}
.pc-dot.on{background:#fff}
```

### Carousel JS
```javascript
function pcStep(id,d){var e=document.getElementById(id),n=e.querySelectorAll('.pc-track img').length,c=+(e.dataset.c||0);pcGo(id,(c+d+n)%n)}
function pcGo(id,n){var e=document.getElementById(id);e.querySelector('.pc-track').style.transform='translateX(-'+n+'00%)';e.querySelectorAll('.pc-dot').forEach(function(d,i){d.classList.toggle('on',i===n)});e.dataset.c=n}
```

### HTML structure
```html
<div class="photo-carousel" id="pc-{LOCATION_SLUG}" data-c="0">
  <div class="pc-track">
    <img src="URL1" alt="Location name" loading="lazy">
    <img src="URL2" alt="Location name" loading="lazy">
    <img src="URL3" alt="Location name" loading="lazy">
  </div>
  <button class="pc-btn pc-prev" onclick="pcStep('pc-{LOCATION_SLUG}',-1)">&#8249;</button>
  <button class="pc-btn pc-next" onclick="pcStep('pc-{LOCATION_SLUG}',1)">&#8250;</button>
  <div class="pc-dots">
    <div class="pc-dot on" onclick="pcGo('pc-{LOCATION_SLUG}',0)"></div>
    <div class="pc-dot" onclick="pcGo('pc-{LOCATION_SLUG}',1)"></div>
    <div class="pc-dot" onclick="pcGo('pc-{LOCATION_SLUG}',2)"></div>
  </div>
</div>
```

Place the carousel immediately before the `<div class="map-actions">` of each stop card. Inject CSS/JS once per file in `<style>`/`<script>` tags at the end of `<body>`.

### Rate limiting
Add `time.sleep(1.5)` between Wikipedia API calls. The endpoint returns 429 if called faster than ~1 req/sec over a session.

### Which locations to include
- ✅ Confirmed activities and booked hotels: add carousel
- ✅ Planned-but-not-booked activities (e.g., Point Lobos, Hearst Castle): add carousel
- ❌ Unconfirmed restaurants: skip
- ❌ `la-guide.html`: skip entirely (pending revamp)

### Automation script
See `inject_photos.py` (project root, untracked). It contains the full injection logic: reads each guide, checks a 2000-char guard window before each `map-actions` div to avoid double-injection, fetches images, and writes the carousel HTML. Run `python3 inject_photos.py` then `python3 build_california.py`.
