# PWA App State — MyBody Health Logger

> **For AI agents:** Read this file before making any changes to `docs/index.html`, `docs/sw.js`, or any other PWA file. It is the single source of truth for the app's current feature set, architecture, dev setup, and known decisions.
>
> **Last updated:** 2026-06-04

---

## Architecture Overview

| File | Purpose |
|------|---------|
| `docs/index.html` | Entire PWA — all HTML, CSS, and JavaScript inline in one file |
| `docs/sw.js` | Service worker — network-first caching for HTML/JS/JSON/MD, cache-first for static assets. Bypassed entirely on localhost. |
| `docs/manifest.json` | PWA manifest — name "MyBody", standalone display |
| `docs/sw.js` `CACHE_VERSION` | Bump this string when deploying changes that need the SW cache cleared on production |
| `logs/phone-log.md` | Append-only daily log written by the phone app via GitHub API |
| `logs/dashboard.json` | Active phase parameters — start/target weight, dates, meal plan, maintenance kcal |
| `logs/current-estimates.json` | Live derived metrics (TDEE, rate of loss, VO2 max) — updated each agent session |

**Deployment:** GitHub Pages from the `docs/` folder at `https://mathewo.github.io/health-advisor/`. Pushes to `main` deploy automatically within ~2 minutes (no Actions workflow — direct branch deploy).

---

## Dev Setup

**Start the local server:**
```bash
cd /Users/mathew.ohalloran/health-advisor && python3 -m http.server 8765
```
Then open `http://localhost:8765/docs/index.html` in the Cursor Simple Browser (F5 or Cmd+Shift+B does both).

**On localhost:** the service worker is automatically unregistered on page load (search `__isLocalhost` in `index.html`). Every reload serves fresh files with no caching. No need to bump `CACHE_VERSION` for local changes.

**On production (phone/github.io):** full SW + caching. Bump `CACHE_VERSION` in `sw.js` when deploying changes that need old caches evicted.

### Diagnostic order when "changes don't appear" (mandatory — do this FIRST)

1. **Test the server:** `curl -sS -o /dev/null -w "HTTP: %{http_code}, size: %{size_download} bytes\n" "http://localhost:8765/docs/index.html"`
   - HTTP 000 / empty reply = **server is dead**. Kill: `lsof -ti :8765 | xargs -r kill -9`, restart: `python3 -m http.server 8765`
   - HTTP 200, size > 100KB = server fine, move to step 2
2. **Verify content:** `curl -sS "http://localhost:8765/docs/index.html" | grep "your-new-token"`
3. Only after steps 1–2 pass: consider SW / cache issues

**Lesson (14 May 2026):** A dead Python http.server returns empty replies that look identical to SW stale cache in the browser. Lost an hour to this. Diagnose the server first, always.

---

## Current Feature State (as of 14 May 2026)

### Dashboard Tab

**Phase card (weight chart)**
- Shows daily weight dots, 3-point centred smoothed trend line (green solid), projection (dashed green), plan line (grey dashed)
- Target line at `phase.target_kg` (grey dashed, 2px) — 82 kg original goal, kept as historical record
- **Live target line** (green dashed, 2px) — dynamic, tracks `trend.projectedAtTarget` (the predicted end weight), matches the "Trending to X kg" text above
- Y-axis: `suggestedMin: 78`, `suggestedMax: phase.start_kg + 0.5`
- Shows current weight, trend projection text, progress bar, kg lost / kg to go
- All three reference lines (Plan, Target, Live Target) at `borderWidth: 2`

**Trending projection algorithm (as of 14 May 2026):**
- **Days 1–7:** falls back to planned deficit rate (not enough clean data; first week has glycogen/water flush noise)
- **Days 8+:** 10-day sliding window linear regression on the **smoothed** weigh-in values (3-point centred moving average). Skips the first 7 days. Requires ≥5 data points in window.
- **Rate cap: 0.7 kg/week** — deliberately conservative. The user should always beat the projection, never feel they've underachieved. Do NOT raise this cap without discussing with Mathew.
- **Falls back** to planned deficit rate if window has <5 points.
- Regression uses smoothed (not raw) values to prevent single-day spikes (illness, bank holidays, Imodium rebounds) from distorting the projected rate.

**Weekly deficit card (burndown chart)**
- "Target this week" row (top) — `weekly_deficit_target` from `dashboard.json`
- "Carryover from last week" row — shown only when non-zero, **no bottom border** (changed 14 May)
- Burndown chart (Chart.js) — accumulated deficit vs target projection by day; burger emoji = cheat days, runner emoji = workout days
- **"PREDICTED DEFICIT" row** — no separator line above it, reduced top padding (changed 14 May 2026; previously had `border-top: 2px solid var(--border)`)
- Show Log / Meal Plan buttons

### Log Tab
- Entry forms: weight, waist, cheat, drinks, activity
- Each entry type auto-formats into the `phone-log.md` format
- Workouts auto-logged via iOS Shortcut → GitHub Actions workflow (`logs/log-workout.yml`)

### Settings Tab
- GitHub token + repo config (persisted in localStorage)
- Test Connection button
- Import/export settings JSON (for moving between devices)

### Lock Screen
- PIN entry
- SW version shown at bottom — tap to call `forceSwUpdate()` (clears all caches + unregisters SW + reloads). Useful on production when SW is stuck.

---

## Changelog

| Date | Change | File(s) |
|------|--------|---------|
| 4 Jun 2026 | **Burndown Y-axis extended to 7k** — `max: 5000 → 7000`; same 160px chart height, scale compressed vertically to show 6k and 7k gridlines. | `index.html` |
| 4 Jun 2026 | **Dashboard recalibrated to data-derived TDEE** — `maintenance_kcal` 1,935→2,200; `weekly_deficit_target` 3,500→5,300; `carryover_start_date` 2026-04-20→2026-04-13. All deficit math now uses validated 6-week back-calculated TDEE. | `logs/dashboard.json` |
| 25 May 2026 | **Phase-cumulative carryover** — replaced 2-week rolling window with a running total of all completed weeks since phase start. Surpluses bank indefinitely; planned buffers are never silently forgotten. | `index.html`, `sw.js` |
| 19 May 2026 | **Manual Workout form** — "Extra Activity" button replaced with "Log Workout" (🏃). Dropdown of workout types (Running, Indoor Run, Stair Climbing, Walking, Cycling, Mountain Biking, E-Bike, HIIT, Swimming, Rowing, Other). Fields: duration, distance (running only), active calories, avg HR (optional), date. Writes correct log format: `run`, `stair`, or `workout` entries — all processed for deficit. Use this when the iOS Shortcut fails to auto-log. | `index.html`, `sw.js` |
| 18 May 2026 | **2-level chained carryover** — prev-prev week's result feeds into prev week, which feeds into current week. Bad weeks forgotten after 2 weeks; surpluses and deficits both propagate for up to 2 weeks. | `index.html` |
| 18 May 2026 | **Cumulative carryover** (short-lived) — reverted same day in favour of 1-week lookback. | `index.html` |
| 14 May 2026 | **10-day sliding window linear regression** for trending projection — replaces fixed planned-deficit rate. Uses smoothed values, skips first 7 days, requires 5+ data points, capped at **0.7 kg/week** (deliberately conservative — user should always beat projection). Falls back to planned rate when insufficient data. | `index.html` |
| 14 May 2026 | **Live target line** made dynamic — tracks `trend.projectedAtTarget` instead of hardcoded 79 kg. Matches "Trending to X kg" text. | `index.html` |
| 14 May 2026 | Plan, Target, and Live Target lines all set to `borderWidth: 2` for consistency | `index.html` |
| 14 May 2026 | Section label top margin halved: `24px → 12px` (tightens gap between MyBody and CURRENT PHASE) | `index.html` |
| 14 May 2026 | Live target line (predicted end weight) changed from hardcoded 79 to dynamic; `borderWidth` 1→2, slightly more opaque | `index.html` |
| 14 May 2026 | Fixed Y-axis: `min: 80` → `suggestedMin: 78` so predicted end weight line is always visible | `index.html` |
| 14 May 2026 | Removed `border-top` from `.predicted-deficit-row`; tightened spacing | `index.html` |
| 14 May 2026 | Removed `border-top` above "Target this week" (weeklyDeficitCard separator) | `index.html` |
| 14 May 2026 | Removed bottom border from "Carryover from last week" row | `index.html` |
| 14 May 2026 | Auto-unregister SW on localhost (`__isLocalhost` block) | `index.html` |
| 14 May 2026 | SW fetch handler: bypass all caching on localhost | `sw.js` |
| Pre-14 May | E-bike kcal correction factor (×0.65) applied to Cycling workouts | `index.html` |
| Pre-14 May | Log filters, centered layout, icon edit/delete | `index.html` |
| Pre-14 May | Waist (cm) log type added | `index.html` |
| Pre-14 May | Network-first service worker + auto-update + version indicator | `sw.js` |

---

## Key Data Contracts

**`dashboard.json` fields used by the app:**
- `phase.start_kg`, `phase.target_kg`, `phase.start_date`, `phase.target_date`
- `meal_plan.maintenance_kcal`, `meal_plan.weekly_deficit_target`
- `meal_plan.cycling_kcal_factor` (currently `0.65` — e-bike motor assist correction)
- `meal_plan.weekday.items[]` and `meal_plan.weekend.items[]` — base meal plan for deficit calculation
- `meal_plan.common_cheats[]` — quick-select cheat options in log form

**`phone-log.md` entry types:**
`weight`, `waist`, `cheat`, `drinks`, `beers` (legacy), `activity`, `run`, `stair`, `workout`

**Cheat net-delta logic (mirrors app):**
`outlierKcal = -(cheat_kcal - replaced_kcal)`. Parse `~NNN kcal` from cheat description; parse replaced kcal from `replaces: X (NNN kcal)` if present (0 if absent). A cheat cheaper than its replaced meal adds to the deficit.

**Cycling kcal correction:**
For `workout | Cycling`, `workout | Mountain Biking`, `workout | E-Bike` entries: multiply logged kcal by `cycling_kcal_factor` (0.65) before adding to deficit. Raw kcal is preserved in the log.
