# PWA App State — MyBody Health Logger

> **For AI agents:** Read this file before making any changes to `docs/index.html`, `docs/sw.js`, or any other PWA file. It is the single source of truth for the app's current feature set, architecture, dev setup, and known decisions.
>
> **Last updated:** 2026-07-06

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
| 29 Aug 2026 | **Weekly energy maths is stage-aware, per day** — resolves the known limitation in the *Meal plan stages* entry below. New `mealPlanForDate(mp, date)` resolves stages by date (distinct from `resolveMealPlan()`, which follows the tab the user tapped), and `dailyPlannedDelta(mp, date)` returns one day's `maintenance − target intake`. A stage may declare `target_kcal_weekday` / `target_kcal_weekend` numerically, which wins over summing meal items — needed during a ramp, where intake steps up mid-week and no item list describes the day. `computeWeeklyDeficit()` and `getCompletedWeeks()` now build a 7-element `dailyRates` array (null = day predates the phase) instead of a weekday/weekend pair, so a week straddling a stage boundary is costed correctly and the burndown takes the array directly. `meal_plan.weekly_energy_target_from_plan` makes the weekly target the sum of the in-phase days' planned deltas, the only coherent option when stages don't align to Mon–Sun. Meal Plan screen shows the declared target and an "Items short/over" pill when the items disagree with it. | `index.html`, `sw.js`, `logs/dashboard.json` |
| 29 Aug 2026 | **Weekly energy card clamped to the phase start** — a phase beginning mid-week no longer inherits the previous phase's days. `computeWeeklyDeficit()` returns `phaseStartIdx` / `inPhaseDays` / `partialWeek`, pro-rates both the planned base and the target to the in-phase days, and filters outliers from the phase start rather than Monday. The burndown leaves pre-phase days `null` (no line, no event icons); the card and week-history rows label a part week. Full weeks and phases starting on a Monday are unaffected. | `index.html`, `sw.js` |
| 29 Aug 2026 | **Balance phases show no projection at all** — `computeTrendProjection()` forces a null rate in `balance` mode even once the regression has 5+ points, so the projection line, live-target line and "Trending to X kg" verdict are all absent. The smoothed rolling average over real weigh-ins is kept (neutral grey), since it's measurement, not forecast. Week-history "vs Target" colour now goes through `energyColor()` so balance mode isn't permanently amber/red. | `index.html`, `sw.js` |
| 29 Aug 2026 | **Phase direction + tracking modes** — a phase can now be a tracked *gain* (refeed, bulk) rather than only a cut. `phase.direction` (`loss`\|`gain`) flips the progress labels, the trend-projection clamp, and the weight-change colour; `phase.tracking_mode` (`deficit`\|`surplus`\|`balance`) reframes the weekly energy card. `meal_plan.weekly_energy_target` is signed (positive = deficit, negative = surplus, 0 = hold) and supersedes `weekly_deficit_target`, which is still honoured. Burndown y-axis now spans the data in both directions instead of a fixed 0–7,000, with a zero reference line off deficit mode. Weight-chart y-axis derived from data instead of hardcoded 78–81. Phases without the new fields are unchanged. | `index.html`, `sw.js`, `logs/dashboard.json` |
| 29 Aug 2026 | **Meal plan stages** — `meal_plan.stages[]` lets one phase hold several dated meal plans (for refeed / maintenance ramps). The Meal Plan screen auto-selects the stage covering today and adds a stage selector row above the Weekday/Weekend/Supplements tabs. Stage fields override the parent plan; omitted fields are inherited, so a stage with no `weekday`/`weekend` uses the top-level items. `getMealOptions()` gathers replaceable meals from every stage. Plans without `stages` are unaffected. **Known limitation:** `computeMealPlanWeekDeficit()` still reads top-level `weekday`/`weekend` only, so a *fat-loss* phase using stages would compute its burndown from the top-level plan. Fine for maintenance phases (deficit card is skipped); needs addressing before staging an active cut. | `index.html`, `sw.js`, `logs/dashboard.json` |
| 6 Jul 2026 | **Active phase weight chart scoped to current phase** — `parseWeightLog` filters `date >= phase.start_date`; x-axis anchored to `phase.start_date` not first log entry. Y-axis max `Math.max(81, start_kg + 0.5)` for week-1 spike headroom. Previous phase charts use `p.start_date` for axis. | `index.html`, `sw.js` |
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
- `meal_plan.stages[]` — optional; see *Meal plan stages* below
- `phase.direction`, `phase.tracking_mode`, `meal_plan.weekly_energy_target` — optional; see *Phase direction and tracking modes* below

**Phase direction and tracking modes (optional — added 29 Aug 2026):**

| Field | Values | Default | Effect |
|---|---|---|---|
| `phase.direction` | `loss` \| `gain` | `loss` | Flips progress labels ("kg lost"/"kg gained"), the trend-projection clamp, the goal-margin colour test, and the weekly weight-change colour |
| `phase.tracking_mode` | `deficit` \| `surplus` \| `balance` | `deficit` | Reframes the weekly energy card: labels, verdict colours, burndown axis and reference line |
| `meal_plan.weekly_energy_target` | signed integer | falls back to `weekly_deficit_target`, then 3500 | Positive = deficit, negative = surplus, **0 = hold at maintenance** |

- **`deficit`** — a cut. Unchanged behaviour: axis 0–7,000, 5k reference line, green when at or above target.
- **`surplus`** — a bulk. Target is negative; green when the surplus meets or exceeds it; weight *is* projected from energy balance, which is valid because the calorie-to-tissue link holds.
- **`balance`** — a refeed. Target is ~0. Weight is **never** projected, from calories or from regression: refeed gain is glycogen plus ~3g bound water per gram, not tissue, so a few weeks of it extrapolate to nonsense. `computeTrendProjection()` returns `projectedAtTarget: null` and an empty `projection` for the whole phase; the "Plan" line, the "Live Target" line and the "Trending to X kg" verdict text are all suppressed. Callers must handle the null. What remains is the weigh-in dots, the smoothed rolling average of those dots in neutral grey, and the goal line.
- Because `energyProgress()` can never be positive in balance mode, `energyColor()` treats landing inside the tolerance band (either direction) as on plan rather than requiring an exact hit.
- `weeklyEnergyTarget()` uses explicit `!= null` checks — a legitimate target of `0` must not fall through to the 3500 default.
- **Setting up a bulk:** `direction: 'gain'`, `tracking_mode: 'surplus'`, `weekly_energy_target: -2100` (a ~300 kcal/day surplus), and a `target_kg` above `start_kg`.

**Meal plan stages (optional — added 29 Aug 2026):**

A phase can hold several dated meal plans, for ramps where intake steps up mid-phase:

```json
"meal_plan": {
  "maintenance_kcal": 2200,
  "protein_target": "150g+ per day",
  "weekday": { "items": [ ... ] },        // the end-state plan
  "weekend": { "items": [ ... ] },
  "weekly_energy_target_from_plan": true, // target = sum of the days' planned deltas
  "stages": [
    { "label": "Week 1", "start_date": "2026-08-29", "end_date": "2026-09-04",
      "target_kcal": "1750-2000 ramp",     // human-readable only, never parsed
      "target_kcal_weekday": 1893,         // numeric — used by the energy maths
      "target_kcal_weekend": 1893,
      "weekday": { "items": [ ... ] },     // optional; overrides the top-level plan
      "weekend": { "items": [ ... ] } },
    { "label": "Week 2", "start_date": "2026-09-05", "end_date": "2026-09-11",
      "target_kcal_weekday": 2129,
      "target_kcal_weekend": 2379 }        // no items → inherits the top-level plan
  ]
}
```

- Resolution is `{ ...meal_plan, ...stage }` — a stage overrides only the keys it declares.
- Two resolvers, and the distinction matters. `resolveMealPlan()` follows the stage the **user tapped** (`activeMealStageIdx`, defaulting to today's) and drives the Meal Plan screen. `mealPlanForDate(mp, date)` resolves by **date** and drives all energy maths, which must never depend on which tab is open. Dates outside every range fall back to the first or last stage.
- **Intake resolution per day** (`dailyPlannedDelta()`): a numeric `target_kcal_weekday` / `target_kcal_weekend` on the resolved plan wins; otherwise the day's item totals are summed. Declare the numbers during a ramp, where intake steps up mid-week and no item list describes the day — that also decouples the weekly card from meal items that haven't been agreed yet. `target_kcal` is a label (it may be a string or a range) and is **never** used arithmetically.
- **`weekly_energy_target_from_plan: true`** makes the weekly target the sum of the in-phase days' planned deltas rather than a fixed weekly constant. Use it whenever the stages don't align to Mon–Sun weeks — the refeed's stages run Sat→Fri, so every card week straddles a boundary and a weekly constant can't be split across it. Consequence: base − target = 0 by construction, so the card measures only how far outliers moved you off plan. For a phase whose target is an independent commitment (a cut), leave it off and set `weekly_energy_target`.
- Weeks are costed per day via a 7-element `dailyRates` array where **null means the day predates the phase**. Both `computeWeeklyDeficit()` and `getCompletedWeeks()` build it with `weekPlannedRates()`, and the burndown consumes it directly, so clamping and stage resolution are handled in one place.
- **Keep the top-level `weekday`/`weekend` populated** with the phase's end-state plan. `computeMealPlanWeekDeficit()` still reads it directly for the Previous Phases average, as do the Previous Phases meal plan tabs after archiving. Letting the final stage inherit rather than duplicate keeps the two in step.

**`previous_phases[]` — archiving convention (when closing a phase):**
Each archived phase entry should include: `meal_plan` (full object from active phase), `supplements` (copy of top-level `dashData.supplements` at close time), `end_date`. These power the Previous Phases card's Meal Plan and Supplements tabs. Without them the tabs show "No data". Always copy both when archiving a phase.

**`phone-log.md` entry types:**
`weight`, `waist`, `cheat`, `drinks`, `beers` (legacy), `activity`, `run`, `stair`, `workout`

**Cheat net-delta logic (mirrors app):**
`outlierKcal = -(cheat_kcal - replaced_kcal)`. Parse `~NNN kcal` from cheat description; parse replaced kcal from `replaces: X (NNN kcal)` if present (0 if absent). A cheat cheaper than its replaced meal adds to the deficit.

**Cycling kcal correction:**
For `workout | Cycling`, `workout | Mountain Biking`, `workout | E-Bike` entries: multiply logged kcal by `cycling_kcal_factor` (0.65) before adding to deficit. Raw kcal is preserved in the log.
