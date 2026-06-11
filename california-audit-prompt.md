# California Trip — Content Audit: Trip Plan Markdown vs HTML Guides

## CONTEXT

California Road Trip project at `/Users/adamdrapkin/California Trip/`.

The master source of truth is the **trip plan markdown document** (923 lines):
`/Users/adamdrapkin/California Trip/california/california-trip-plan.md`

This file is the Planning Bible — it contains all confirmed flights, hotels, activities, food stops, day-by-day plans, driving times, social media intelligence, and pending items. According to the project rule: **"If it is in the markdown, it goes in the HTML."**

The 7 HTML guide files (DO NOT include itinerary-v1.html or itinerary-v2.html — those are old and ignored):
1. `/Users/adamdrapkin/California Trip/california/california-routes.html`
2. `/Users/adamdrapkin/California Trip/california/sf-guide.html`
3. `/Users/adamdrapkin/California Trip/california/bigsur-guide.html`
4. `/Users/adamdrapkin/California Trip/california/centralcoast-guide.html`
5. `/Users/adamdrapkin/California Trip/california/sandiego-guide.html`
6. `/Users/adamdrapkin/California Trip/california/la-guide.html`
7. `/Users/adamdrapkin/California Trip/california/logistics-guide.html`

**YOUR JOB:** Run 3 waves of parallel agents to audit whether the HTML files fully reflect the trip plan markdown. You MUST use the `Agent` tool — do NOT read files yourself.

---

## WAVE 1 — Launch all 15 agents in a SINGLE message (one tool-use block per agent)

All Wave 1 agents use model **haiku**. Each agent reads a specific file/range and outputs a tight structured bullet list. Nothing more.

### Trip plan markdown agents — 8 agents (S1–S8)

**Agent S1** (haiku) — Read `california-trip-plan.md` lines 1–141
Covers: Flight information, confirmed hotels (Hyatt, Castle Inn, Beachside Inn, Best Western Coronado).
Extract: every flight number, route, confirmation code, seat number, bag fee doc number, dates, times. Every hotel name, address, confirmation number, PIN, room type, rate, check-in/check-out times, included amenities, cancellation policy, special flags. Output as structured bullet list.

**Agent S2** (haiku) — Read `california-trip-plan.md` lines 142–301
Covers: Confirmed activities (Alcatraz, Muir Woods, Sterling Vineyards), Food & Markets section.
Extract: every activity name, confirmation number, date, time, cost, logistics note, booking URL. Every restaurant, market, and food stop — name, address, hours, what to order, cost, special notes. Output as structured bullet list.

**Agent S3** (haiku) — Read `california-trip-plan.md` lines 302–395
Covers: All Gaps / Pending items, Party & Logistics, Critical Flags.
Extract: every ⚠️ pending item with its booking URL, deadline, and cost. Every critical flag, warning, or constraint noted. Output as structured bullet list.

**Agent S4** (haiku) — Read `california-trip-plan.md` lines 396–550
Covers: Revised Day-by-Day Plan — Days 1 through 3 (SF arrival, Jul 3 Alcatraz/Muir Woods, Jul 4 Birthday/Napa).
Extract: every named stop, attraction, timing note, tip, quote, food recommendation, and logistics note for Days 1–3. Output as structured bullet list organized by day.

**Agent S5** (haiku) — Read `california-trip-plan.md` lines 551–700
Covers: Revised Day-by-Day Plan — Days 4–5 (Big Sur marathon drive, Santa Barbara).
Extract: every named stop, drive time, cost, attraction, trail, food stop, timing note, hotel logistics, and tip for Days 4–5. Output as structured bullet list organized by day.

**Agent S6** (haiku) — Read `california-trip-plan.md` lines 701–784
Covers: Revised Day-by-Day Plan — Days 6–10 and Departure (San Diego/Coronado, LA days, Jul 12 departure).
Extract: every named stop, attraction, activity, restaurant, drive time, hotel logistics, timing note, and tip for Days 6–10 and departure. Output as structured bullet list organized by day.

**Agent S7** (haiku) — Read `california-trip-plan.md` lines 785–864
Covers: Verified Driving Times Summary, Social Media Intelligence Log, NPS Data.
Extract: every verified driving leg with exact minutes and miles. Every social media entry — creator handle, follower count, view count, location, quote. Every NPS data point. Output as structured bullet list.

**Agent S8** (haiku) — Read `california-trip-plan.md` lines 865–923
Covers: Pre-Booking Checklist, Location Corrections & Name Decoder, Segment Structure — HTML Build Plan, Open Questions.
Extract: every pre-booking checklist item with status. Every location correction or name variant. Every HTML build instruction or content rule. Output as structured bullet list.

---

### HTML agents — 7 agents (H1–H7)

**Agent H1** (haiku) — Read `/Users/adamdrapkin/California Trip/california/california-routes.html`
Extract: every named destination, route, stop, drive time shown, hero text, section heading. Output as structured bullet list.

**Agent H2** (haiku) — Read `/Users/adamdrapkin/California Trip/california/sf-guide.html`
Extract: every named attraction, restaurant, food card, hotel detail (name, address, confirmation number, rate, dates), activity booking (confirmation number, time, cost), pending/⚠️ alert, time block entry, social proof quote, drive time shown. Output as structured bullet list.

**Agent H3** (haiku) — Read `/Users/adamdrapkin/California Trip/california/bigsur-guide.html`
Extract: every named stop, trail, viewpoint, drive time shown (minutes + miles), hotel detail, booking alert, social proof quote, food stop. Output as structured bullet list.

**Agent H4** (haiku) — Read `/Users/adamdrapkin/California Trip/california/centralcoast-guide.html`
Extract: every named stop, attraction, restaurant, hotel detail, drive time shown, pending alert, social proof quote. Output as structured bullet list.

**Agent H5** (haiku) — Read `/Users/adamdrapkin/California Trip/california/sandiego-guide.html`
Extract: every named attraction, beach, activity, restaurant, hotel detail (confirmation, rate, pool warning), drive time shown, pending alert. Output as structured bullet list.

**Agent H6** (haiku) — Read `/Users/adamdrapkin/California Trip/california/la-guide.html`
Extract: every named attraction, restaurant, food card, activity, drive time shown, pending alert, hotel stub content, social proof quote. Output as structured bullet list.

**Agent H7** (haiku) — Read `/Users/adamdrapkin/California Trip/california/logistics-guide.html`
Extract: every hotel name + confirmation number + dates shown, every activity + confirmation + date + logistics note, every restaurant card name + address, every flight detail (number, route, conf code, seats, bag doc), every pending item with booking URL. Output as structured bullet list.

---

**WAIT for all 15 Wave 1 agents to complete before starting Wave 2.**

---

## WAVE 2 — Launch 2 synthesis agents simultaneously (single message, both at once)

Both Wave 2 agents use model **haiku**.

**Agent SYNC1** (haiku)
Using the outputs from S1–S8 (trip plan content) and H1–H7 (HTML content), produce two markdown tables:

**TABLE A — MATCHES** (content in the trip plan that IS correctly present in the HTMLs)
| Content Item | Trip Plan Section | Present In HTML File(s) |
|---|---|---|

**TABLE B — GAPS** (content in the trip plan that is MISSING, INCOMPLETE, or WRONG in the HTMLs)
| Content Item | Trip Plan Source | Status in HTML | Which HTML File(s) Affected |
|---|---|---|---|

Be specific. If a drive time is present but shows the wrong minutes, flag it. If a confirmation number is in the markdown but absent from the HTML, flag it. If a ⚠️ pending item is in the markdown but its alert is missing from the HTML, flag it. If a social proof quote is in the markdown but not in the HTML, flag it.

**Agent SYNC2** (haiku)
Using the outputs from H1–H7 (HTML content) and S1–S8 (trip plan content), identify content present in the HTML files that does NOT appear in the trip plan markdown — things added to the HTMLs beyond what the markdown specified.

**TABLE C — HTML ADDITIONS** (in HTML but not in trip plan markdown)
| Content Item | Present In HTML File | Not In Trip Plan | Notes |
|---|---|---|---|

---

**WAIT for both Wave 2 agents to complete before starting Wave 3.**

---

## WAVE 3 — 1 final agent (Sonnet)

**Agent PLAN** (sonnet)
Using TABLE B (gaps) from SYNC1 and TABLE C (additions) from SYNC2, produce a structured action plan.

Format it as a file-by-file breakdown:

### Action Plan — [filename]
**Missing from trip plan:** (specific items in the markdown not found in this HTML — priority: 🔴 High / 🟡 Medium / 🟢 Low)
**Incorrect in HTML:** (items present but wrong — wrong drive time, wrong confirmation number, wrong address, etc.)
**HTML additions to review:** (items added beyond the trip plan — flag anything that looks inconsistent)
**Recommended edits:** (specific and actionable — "Add Sterling Vineyards confirmation code TOCK-R-AE87DB44 to the booking card", not vague)

End with a **Top 10 Priority Fixes** — the 10 most impactful gaps across all files, ranked by trip accuracy risk.

**Output the full plan in your response.**

---

## CRITICAL RULES
1. You MUST use the `Agent` tool for every agent — do NOT read files yourself
2. All S and H agents MUST use `model: "haiku"`
3. SYNC1 and SYNC2 MUST use `model: "haiku"`
4. PLAN agent MUST use `model: "sonnet"`
5. Wave 1: ALL 15 agents launch in a single message
6. Wave 2: BOTH agents launch in a single message after Wave 1 is fully complete
7. Wave 3: 1 agent, after Wave 2 is fully complete
8. Do NOT start any wave until the previous wave is fully complete
9. Do NOT read any file yourself — delegate everything to agents
