# PWA App State — MyBody Health Logger

> **For AI agents:** Read this file before making any changes to `docs/index.html`, `docs/sw.js`, or any other PWA file. It is the single source of truth for the app's current feature set, architecture, dev setup, and known decisions.
>
> **Last updated:** 2026-05-14

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
- Shows daily weight dots, 7-day rolling average trend line (green), projection (dashed green), plan line (grey dashed)
- Target line at `phase.target_kg` (grey dashed) — currently 82 kg (original goal, kept as historical record)
- **Live target line at 79 kg** (green dashed, added 14 May 2026) — Phase 2 insurance target
- Y-axis: `suggestedMin: 78`, `suggestedMax: phase.start_kg + 0.5` (changed from hardcoded `min: 80` on 14 May — was clipping the 79 kg line)
- Shows current weight, trend projection, progress bar, kg lost / kg to go

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
| 14 May 2026 | Added 79 kg live target line to weight chart (green dashed) | `index.html` |
| 14 May 2026 | Fixed Y-axis: `min: 80` → `suggestedMin: 78` so 79 kg line is visible | `index.html` |
| 14 May 2026 | Removed `border-top` from `.predicted-deficit-row`; tightened spacing | `index.html` |
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
