# Health planning context (durable)

> **Purpose:** Recovery of key decisions and dates from planning chats if **chat history is unavailable**.  
> **Not used by the PWA** — for humans and AI sessions only.  
> **Last updated:** 2026-04-27

---

## Trip and scale targets (fixed dates)

| When | What | Target / note |
|------|------|-----------------|
| **7 Jun 2026** | **Italy** | **~82 kg** (morning scale target for the trip) |
| **12 Sep 2026** | **Bali** | **~77–78 kg / ~22% BF** (longer-horizon goal; see `profile/profile.md` Phase Roadmap if present) |

**Phase wiring (from `logs/dashboard.json` and profile roadmap):**

- **Phase 1 (active in JSON):** 13 Apr 2026 → **6 Jun 2026**, 85.8 → **82.0 kg** (dashboard `target_date` is 6 Jun).  
- **Italy on 7 Jun** is the **day after** that phase end — success = at or near **82 kg** on departure, not a separate app tile.  
- **Maintenance (planned):** ~7 Jun–5 Jul refeed at ~1,935 kcal; expect **~83.5–84 kg** on the scale when fully glycogen-loaded (not “fat regain” — see experiments / profile).  
- **Phase 2 cut:** ~7 Jul–12 Sep toward Bali.

If `profile/profile.md` is missing or empty, this table is the backup for **Italy 7 Jun** and **Bali 12 Sep**.

---

## How success is judged (reframed 2026)

- **Primary outcomes:** **waist** (navel, relaxed, fasted) + **photos** + clothing fit — **not** a single magic kg.  
- **Scale:** use **7-day rolling average**; ignore one-day spikes (alcohol, salt, carby meals).  
- **Clinic / Randox waist (e.g. 105 cm with clothes, different landmark):** do **not** mix into the self-measured navel series — see profile note.

`logs/phone-log.md` supports `waist` lines; the app can **log** waist but has **no waist progress chart** (by design).

---

## Historical activity lesson (Apple Health, 2025 cuts)

From `data/export.xml` (analysed Apr 2026) vs `profile/historical-weights.csv`:

- **Cut #1 (Jun 2025):** many logged **stair** sessions, higher **active kcal** / **exercise minutes** → **~0.45 kg/wk** loss.  
- **Cut #2 (Jul–Sep 2025):** **zero** logged workouts, lower move calories → **~0.21 kg/wk** — more like drift than a hard cut.

**Lever:** if **smoothed** weight **stalls vs projection for ~2 weeks**, reintroduce **structured stair climbing 3–4×/week** (or equivalent) **before** slashing food further — protects **NEAT** and matches what worked in his data.

---

## Deficit “too strong?” heuristics (muscle priority)

- User priority: **retain muscle** (age 39+); protein + hard resistance training are non-negotiable.  
- **Yellow flag:** sustained **7-day average** loss **>** **~1% body weight / week** for **multiple** consecutive weeks **plus** training suffering.  
- **Red flag:** that rate **and** **clear** strength/performance drop — consider **+100–150 kcal/d** or a **short maintenance** block, not deeper cuts by default.  
- Early cut weeks often show a **fast** scale drop (water, glycogen) — do not annualise the first 10–14 days as a full-phase fat-loss rate.

---

## Repo workflow (so data isn’t stale)

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

- Serve from **`docs/`** (e.g. `python3 -m http.server 8765`).  
- If the **Simple Browser** shows an old build: new **`docs/sw.js` CACHE_VERSION`**, or tap the **SW version** on the lock screen, or **Unregister** the service worker.  
- Does not affect the **health plan**; only how you view the app locally.
