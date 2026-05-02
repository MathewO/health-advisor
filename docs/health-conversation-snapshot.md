# Health planning context (durable)

> **Purpose:** Recovery of key decisions and dates from planning chats if **chat history is unavailable**.  
> **Not used by the PWA** — for humans and AI sessions only.  
> **Last updated:** 2026-05-01

---

## Trip and scale targets (fixed dates)

| When | What | Target / note |
|------|------|-----------------|
| **7 Jun 2026** | **Italy** | **~82 kg** (original morning scale target — overshot early; new app target 81 kg; happy range 80–81.5 kg as long as it's fat loss) |
| **12 Sep 2026** | **Bali** | **~77–78 kg / ~22% BF** (longer-horizon goal; see `profile/profile.md` Phase Roadmap if present) |

**Phase wiring (from `logs/dashboard.json` and profile roadmap):**

- **Phase 1 (active in JSON):** 13 Apr 2026 → **6 Jun 2026**, 85.8 → **82.0 kg** (dashboard `target_date` is 6 Jun).
- **Italy on 7 Jun** is the **day after** that phase end — success = at or near **82 kg** on departure, not a separate app tile.
- **Maintenance (planned):** ~7 Jun–5 Jul refeed at ~2,100 kcal (see updated estimate below); expect **~83.5–84 kg** on the scale when fully glycogen-loaded (not "fat regain").
- **Phase 2 cut:** ~7 Jul–12 Sep toward Bali.

**Maintenance block — training (intent):** **Italy trip** (first ~week of the maintenance window) = deliberate **no resistance training** while away. **Following ~3 weeks** = **maintenance calories** in the same ~7 Jun–5 Jul refeed window as above; **resume lifting** and ease volume/intensity in the first sessions back after travel.

If `profile/profile.md` is missing or empty, this table is the backup for **Italy 7 Jun** and **Bali 12 Sep**.

---

## How success is judged (reframed 2026)

- **Primary outcomes:** **waist** (navel, relaxed, fasted) + **photos** + clothing fit — **not** a single magic kg.
- **Scale:** use **7-day rolling average**; ignore one-day spikes (alcohol, salt, carby meals).
- **Clinic / Randox waist (e.g. 105 cm with clothes, different landmark):** do **not** mix into the self-measured navel series — see profile note.

`logs/phone-log.md` supports `waist` lines; the app can **log** waist but has **no waist progress chart** (by design).

**Progress photo catalogue (for humans + agents):** canonical shirtless sets live under **`profile/body-comp/progress/<date>_<label>/`** with numbered PNGs and a **`README.md`** per set (pose map + metrics). Start with **`profile/body-comp/AGENTS.md`**. Image binaries are gitignored and never pushed.

---

## Historical activity lesson (Apple Health, 2025 cuts)

From `data/export.xml` (analysed Apr 2026) vs `profile/historical-weights.csv`:

- **Cut #1 (Jun 2025):** many logged **stair** sessions, higher **active kcal** / **exercise minutes** → **~0.45 kg/wk** loss.
- **Cut #2 (Jul–Sep 2025):** **zero** logged workouts, lower move calories → **~0.21 kg/wk** — more like drift than a hard cut.

**Lever:** if **smoothed** weight **stalls vs projection for ~2 weeks**, reintroduce **structured stair climbing 3–4×/week** (or equivalent) **before** slashing food further — protects **NEAT** and matches what worked in his data.

---

## Training profile (not logged in app — agent context only)

- **Resistance sessions:** 3–5x/week (guaranteed); includes a **squat/legs day**, a **deadlift day**, and 1–2 **accessory/smaller-muscle days**.
- **Cardio:** 1–2 runs/week (auto-logged via Apple Watch shortcut); treated as **additive** to deficit, **not** baked into maintenance baseline.
- **Philosophy:** maintenance figure excludes cardio by design — runs show up as bonus deficit kcal in the app burndown.

---

## Estimated maintenance (cardio-free) — working hypothesis

- **~2,100 kcal/day** with lifting + daily life activity, no structured cardio.
- Current `dashboard.json` figure of **1,935 kcal** is likely an **underestimate** given actual activity level.
- Back-calculated from May 2026 data: implied TDEE ~2,100–2,350; ~2,100 chosen as the **cardio-free** anchor.
- **To be validated at the 25 May 6-week check** using total weight change + estimated average intake.
- **Maintenance planning post-Italy** (~7 Jun): target **~2,100 kcal/day** base; add cardio kcal on top as desired.

---

## Session notes — 2 May 2026

- **Gym performance:** Feeling strong as of 2 May — no strength drops noted despite running above 1 kg/week loss rate. Key signal for 8–9 May check-in: if this holds, no calorie adjustment needed (Scenario A/B). If strength drops appear, add 100–150 kcal/day immediately.
- **Monday weight warning:** 2 May involved 101 min cycling (1,045 kcal) + 3–4 pints + higher-calorie dinner (~400 kcal above plan). Expect Monday 4 May scale to read 0.5–1.5 kg above today's 82.2 due to glycogen refill, alcohol, sodium. Not fat gain — do not panic. Use 7-day avg, not daily readings.
- **Whey protein:** MyProtein Impact Whey (not isolate), various flavours. Dashboard shows 116 kcal / 21g protein per scoop (single) and 232 kcal / 42g protein (double) — consistent with Impact Whey macros. No need to update if flavour changes.
- **Ashwagandha check-in due:** Started ~25 Apr 2026. First noticeable effects (cortisol/stress, sleep) expected 2–4 weeks in (~9–23 May). At 25 May 6-week check, do a brief self-assessment: stress levels, sleep quality, gym recovery. Testosterone effects take 8–12 weeks (retest July 2026).

---

## Phase 1 check-in schedule

| Date | Action |
|------|---------|
| **~8–9 May 2026** | **Weekly check.** Pull log, compute 7-day avg weight (2–8 May) vs prior week avg (~83.24 kg for 25 Apr–1 May). Apply scenario framework below. |
| **~25 May 2026** | **6-week maintenance back-calculation.** Use total weight change + estimated avg intake to tighten TDEE. Decide if ~2,100 stands or needs updating. |
| **6 Jun 2026** | **Phase end.** DEXA scan (DexaStrong, Leeds — baseline post-cut). Start maintenance at ~2,100 kcal + cardio as additive. |

**Weekly check scenario framework (8–9 May and onward):**

| Scenario | Signal | Action |
|----------|--------|--------|
| **A** | 7-day avg loss ~0.4–0.7 kg/week, training solid | No change. Review again in 2 weeks. |
| **B** | Loss still fast (>0.7 kg/wk) but recovery/training fine | Optional +100 kcal/day (carbs/fat). Not urgent. |
| **C** | Fast loss **and** training suffering or strength dropping | Add 100–150 kcal/day now. Muscle-retention flag. |
| **D** | Loss slowing (<0.3 kg/wk) unexpectedly | Check logging accuracy; review drink/cheat kcal. |

---

## Deficit "too strong?" heuristics (muscle priority)

- User priority: **retain muscle** (age 39+); protein + hard resistance training are non-negotiable.
- **Yellow flag:** sustained **7-day average** loss **>** **~1% body weight / week** for **multiple** consecutive weeks **plus** training suffering.
- **Red flag:** that rate **and** **clear** strength/performance drop — consider **+100–150 kcal/d** or a **short maintenance** block, not deeper cuts by default.
- Early cut weeks often show a **fast** scale drop (water, glycogen) — do not annualise the first 10–14 days as a full-phase fat-loss rate.

---

## Repo workflow (so data isn't stale)

- Before answering **any** health / log / phase question, run **`git pull --rebase`** in this repo; the PWA writes **`logs/phone-log.md`** via GitHub.
- This is also stated in **`.cursor/rules/health-context.mdc`** (that file may be **gitignored** — this doc is the **portable** reminder for other machines).

---

## Optional local-only files

These are often **gitignored**; duplicate critical dates here and in `profile` when you change them:

- `profile/profile.md`
- `experiments/experiments.md`
- `supplements/supplements.md`

**Authoritative for daily numbers:** `logs/phone-log.md` + `logs/dashboard.json` (after pull).

---

## PWA / local dev (debugging)

- **Preview in Cursor (recommended):** **Run → Start Debugging** or press **F5**, choose **"Preview: Health Advisor"** — starts the static server on **8765** (repo root) via `preLaunchTask`, then opens **`http://localhost:8765/docs/index.html`** in the **integrated browser** with the URL set in `.vscode/launch.json` (no empty address bar).
- **Alternative:** **Cmd+Shift+B** runs the build task **"Preview: open in Cursor Simple Browser"** (server + `workbench.action.browser.open`). If the browser tab is still blank, use **F5** instead. **Terminal → Run Task… → Preview: static server** — server only. A bookmark alone cannot start the server.
- Serve from the **repository root** on port **8765** (e.g. run task **Preview: static server (repo root, port 8765)**), then open **`http://localhost:8765/docs/index.html`** — so `/logs/` resolves and **Cursor Browser** can load data without a GitHub token (same as empty Settings). Optional: `?local=1` forces local files even if a token is set.
- If the **Simple Browser** shows an old build: new **`docs/sw.js` CACHE_VERSION`**, or tap the **SW version** on the lock screen, or **Unregister** the service worker.
- Does not affect the **health plan**; only how you view the app locally.
