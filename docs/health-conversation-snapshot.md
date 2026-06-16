# Health planning context (durable)

> **Purpose:** Recovery of key decisions and dates from planning chats if **chat history is unavailable**.  
> **Not used by the PWA** — for humans and AI sessions only.  
> **Last updated:** 2026-05-28

---

## Trip and scale targets (fixed dates)

| When | What | Target / note |
|------|------|-----------------|
| **7 Jun 2026** | **Italy** | **~82 kg** (original dashboard target — **already hit on 9 May, 28 days early**). **Revised live target: 80 kg** (decided 10 May — Phase 2 insurance, trajectory already points here at 0.83 kg/wk). Dashboard kept at 82 kg to preserve the overachievement record. |
| **12 Sep 2026** | **Bali** | **~77–78 kg / ~22% BF** (longer-horizon goal; see `profile/profile.md` Phase Roadmap if present) |

**Phase wiring (from `logs/dashboard.json` and profile roadmap):**

- **Phase 1 (active in JSON):** 13 Apr 2026 → **6 Jun 2026**, 85.8 → **82.0 kg** (dashboard `target_date` is 6 Jun).
- **Italy on 7 Jun** is the **day after** that phase end — success = at or near **82 kg** on departure, not a separate app tile.
- **Maintenance (planned):** ~7 Jun–5 Jul refeed at **~2,200 kcal** (revised from 2,100 following 6-week TDEE validation); expect **~80.5–81 kg** on the scale after Italy rebound (lower than earlier estimates — Italy is Jun 7–13, city walking with high steps, so glycogen rebound is ~0.5–1 kg rather than 1.5–2 kg from a sedentary refeed).
- **Phase 2 cut:** ~7 Jul–12 Sep toward Bali. Expected Phase 2 start weight: **~80–80.5 kg**.
- **Phase 2 gate check (late June / early July):** blood test (testosterone, LDL, HOMA-IR, fasting glucose) + DEXA scan — both to be done before Phase 2 start. If T ≤13 nmol/l, address hormones before committing to another 10-week cut.

**Maintenance block — training (intent):** **Italy trip** (Jun 7–13, confirmed city walking — deliberate **no resistance training** while away). **Following ~3 weeks** = **maintenance calories** at 2,200 kcal; **resume lifting** and ease volume/intensity in the first sessions back after travel.

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
- **All `workout` entries:** all logged workout types (cycling, walking, MTB, etc.) are treated as **additive to deficit** (same as `run` and `stair`). Routine dog walks are NOT logged and are already baked into maintenance NEAT.
- **E-bike correction (`cycling_kcal_factor`):** for `Cycling`, `Mountain Biking`, and `E-Bike` workout types, the app applies `cycling_kcal_factor` from `dashboard.json` (currently **0.65**) to the raw Apple Watch kcal before using it in deficit calculations and charts. The raw kcal is preserved in the log; the corrected value is shown in the app log view as ~~raw~~ → corrected. Chat calculations must apply the same factor.
- **Indoor Cycling (spin class) — full kcal, no correction factor.** The 0.65 factor does NOT apply to `Indoor Cycling` entries. A spin class is pure human effort; the factor only exists to correct for e-bike motor assist.
- **Known shortcut behaviour (confirmed 21 May 2026):** Apple Watch logs Indoor Cycle under `HKWorkoutActivityTypeCycling`, so the iOS Shortcut sends `type: "Cycling"` for both outdoor e-bike rides AND indoor spin classes. The workflow writes `workout | Cycling | ...` in both cases, which incorrectly applies the 0.65 factor to spin sessions. **Fix:** manually edit the log entry from `Cycling` to `Indoor Cycling` after the fact. The shortcut has not been updated (rare edge case). Alternatively, delete the auto-logged entry and re-log via the "Log Workout" form selecting "Indoor Cycling".
- **Cheat net-delta logic (mirrors app):** `outlierKcal = -(cheat_kcal - replaced_kcal)`. Parse `~NNN kcal` from the cheat description; parse replaced meal kcal from `replaces: X (NNN kcal)` if present (0 if absent). A cheat cheaper than its replaced meal adds to the deficit; a cheat with no replaces tag is fully additional calories.

---

## Estimated maintenance (cardio-free) — data-derived estimate

> **This section is the single source of truth for the TDEE estimate.** `experiments/experiments.md` references this; do not maintain a separate figure there. When revising the estimate, update this section first, then sync any references in other files.

- **Data-derived estimate: ~2,200 kcal/day** (cardio-free — gym + dog walks only, no structured cardio). **Validated 25 May 2026.**
- **How derived (25 May 2026 — 6-week check-in):** 84.1 kg (Apr 20, week-2 start) → 80.6 kg (7d avg May 25), 35 days. actual_daily_deficit = (84.1 − 80.6) × 7,700 ÷ 35 = **770 kcal/day**. TDEE = 770 + 1,435 avg intake = **2,205, rounded to 2,200**.
- **Previous estimate (10 May): 2,050–2,075.** Revised upward ~125 kcal at 6-week check-in. The earlier estimate was based on 27 days of data; this 35-day figure is more reliable with water noise fully settled.
- **Algorithm baseline was ~1,850–2,000** (Mifflin-St Jeor / formula-based). Phase 1 data confirms this was an underestimate.
- `dashboard.json` `maintenance_kcal` left at **1,935** as a conservative anchor and to preserve the original phase record. The data-derived estimate here supersedes it for planning purposes.
- **Maintenance planning post-Italy** (~7 Jun): target **~2,200 kcal/day** base (revised from 2,100 following 6-week validation); add workout kcal on top as logged.

---

## Body fat % projections and phase structure (12 May 2026)

> Source: Navy formula baseline + DEXA belly fat layer analysis (Ethier / Built With Science, 18k scans). See `research/metabolic/belly-fat-layers-dexa-2026.md`. **DEXA planned for late June (post-Italy, before Phase 2) — will replace these estimates with actuals.**

| Weight | Est. BF% | Layer | Notes |
|---|---|---|---|
| 85.4 kg (Apr baseline) | ~28.5% | Layer 1 | Starting point |
| 81.6 kg (12 May) | ~25.1% | Layer 1→2 | At belly fat inflection point — accelerating now |
| 80 kg (Phase 1 target) | ~23.6% | Layer 2 | Not yet into stubborn-fat territory — right stop point |
| 78 kg (Bali / Phase 2) | ~21.7% | Layer 2→3 boundary | Lower belly/love handles last to go |

**10% rule check:** Phase 1 (85.8→80 kg) = 6.7% loss ✅. Phase 2 (~82→78 kg) = ~4.9% ✅. Both within the research-backed 5–7% per phase sweet spot.

**Why 80 kg is the right Phase 1 stop:** At 80 kg you're in Layer 2 (~23.6% BF), making good visible progress, but not yet in the high-cortisol Layer 3 zone. Pushing harder pre-Italy would hit the stubborn-fat wall at a poorly timed moment. Phase 2 starts fresh from a better position after the maintenance month.

**Steps insurance policy (Layer 2 stall lever):** Current avg steps: 8,073/day. If rate slows in the next 2 weeks, the first lever is **bumping steps to 10,000/day** before cutting calories further. This maintains calorie burn without spiking hunger or triggering deeper metabolic adaptation.

**Diet break protocol (Phase 2 / Layer 3 tool):** When deep in Layer 3 (~15–20% BF), if cortisol-driven water retention and severe hunger appear, a 5–14 day break at +500 kcal (mainly carbs) brings cortisol down and resets hunger. Not the same as the maintenance month — this is a short tactical tool for mid-phase if needed in Phase 2.

---

## 25 May 2026 — TDEE Back-Calculation Protocol (mandatory)

> **For the agent running the 25 May check-in:** follow this exact methodology. Do not substitute the old water-correction or workout-subtraction approach.

### Rationale (agreed 18 May 2026)
- All logged workouts (runs, stairs, cycling, walks) are deliberate phase activity and net against cheats/drinks each week. Unlogged activity (gym sessions, dog walks, routine NEAT) is already baked into the baseline TDEE.
- Tracked weekly deficits confirm workouts ≈ offset cheats/drinks: cumulative carryover across 5 weeks ≈ 0 kcal. This means net actual intake = meal plan base = 1,435 kcal/day.
- Week 1 (Apr 13–19) is excluded to avoid the glycogen/water flush, which inflates apparent fat loss rate.

### Input values
| Input | Value | Source |
|---|---|---|
| Start weight | **84.1 kg** | Apr 20 morning (phone-log.md) |
| End weight | **May 25 7-day average** | Compute from phone-log.md on the day |
| Days | **35** | Apr 20 → May 25 |
| Average intake | **1,435 kcal/day** | Derived: 3,500 kcal/wk tracked deficit ÷ 7 = 500/day → 1,935 − 500 = 1,435 |

### Formula
```
actual_daily_deficit = (84.1 − may25_7d_avg) × 7,700 ÷ 35
TDEE = actual_daily_deficit + 1,435
```

### What to do with the result
- Update `logs/current-estimates.json`: `tdee.estimate_kcal_per_day`, `tdee.range`, `tdee.derivation`, remove `pending_validation` tag
- Update `docs/health-conversation-snapshot.md` Estimated maintenance section
- Cross-check: if TDEE > 2,050, revise Phase 2 maintenance planning calories upward accordingly
- Note the result alongside today's TDEE calculation for comparison

---



### Phase 2 revised projections
- Phase 1 on track to end at **~78-79 kg** (vs original 82 kg target — significantly ahead)
- Maintenance rebound will bring scale to **~80-81 kg** (glycogen + water, not fat)
- **Phase 2 revised realistic range: 75-77 kg / 19-21% BF at Bali (12 Sep)**
  - Conservative (0.5 kg/wk × 9.6 wks from 81 kg): ~76 kg / ~20% BF
  - Optimistic (0.7 kg/wk × 9.6 wks from 81 kg): ~74 kg / ~18% BF
  - Sweet spot target: **75-77 kg** — gets to Layer 2→3 boundary without grinding through stubborn-fat territory right before a holiday
- Original Bali target of 77-78 kg is now comfortably beatable. Update Phase 2 planning accordingly when setting up the next phase.

### Post-Bali lean bulk — intent recorded
- Decided in principle: **lean bulk starting ~Oct 2026**
- Parameters: ~250-400 kcal/day surplus above TDEE, 180-200g protein/day, increase training volume progressively
- **Gating condition: July testosterone retest.** If T still low-normal (≤13 nmol/l) despite deficit resolved and infection cleared, address hormonal issue first before committing to a bulk. Mid-range T (15+ nmol/l) = green light.
- DEXA planned for late June (post-Italy, pre-Phase 2) gives lean mass baseline for tracking actual muscle gain during the bulk. Doing it post-refeed (glycogen fully restored) gives more accurate lean mass reading than post-cut depleted state.
- Realistic gain rate at age 39, experienced trainee: ~0.25-0.5 kg lean mass per month in a dedicated lean bulk.

### Blood pressure — monitoring log

| Date | Settled readings | Avg systolic | Context | vs NICE threshold |
|------|-----------------|--------------|---------|-------------------|
| 5 May 2026 | ~128/71 | 128 | Baseline check | ✅ Below 135 |
| 17 May 2026 | 133/72, 135/64 | ~133–134 | Big ride day + charcuterie + wine | ⚠️ Above 130, below 135 — occasion #1 |
| 31 May 2026 | 129/78, 131/69 | ~130 | Morning after social drinks (stopped 18:30), coffee before measuring | ⚠️ Above 130, below 135 — occasion #2 |

- UK NICE home hypertension threshold: **≥135/85** sustained. Neither reading has crossed this.
- **Pattern: settled systolic consistently 128–134** — Stage 1 territory (ACC/AHA) but below NICE threshold.
- Likely contributors: prolonged calorie deficit elevating cortisol; job-related background stress; may also relate to CSC eye fluid finding (cortisol-linked).
- **Related symptoms (29–31 May):** orthostatic dizziness on quick positional changes; fluid behind one eye (CSC diagnosed by optician, specialist appointment 2 Jun).
- **Action:** eye specialist appointment **29 Jun 2026** (delayed from Jun 2). By then: 3 weeks into maintenance, post-Italy recovery, cortisol load reduced. Condition may have improved. Full GP review also warranted post-maintenance. Recheck BP mid-June after Italy.
- Full readings in `profile/profile.md` (gitignored).

---

## Session notes — 16 Jun 2026

### Maintenance month — plan confirmed and live

**Phase 1 final closeout:**
- Phase-end weight: 79.3 kg (6 Jun). Low: 78.7 kg (5 Jun). Waist: 99 cm (4 Jun).
- Italy 7–13 Jun: natural refeeding, city walking. Scale rebound: 79.3 → 81.0 (14 Jun) → 79.9 (15 Jun) → 79.7 (16 Jun). Waist on return: 100 cm (14 Jun) — essentially unchanged, confirming rebound is glycogen/water only.

**Maintenance meal plan (confirmed, live in `dashboard.json`):**

| Week | Daily kcal target | Notes |
|------|------------------|-------|
| Week 2 (14–20 Jun) | ~1,810 avg | Structured plan: weekday 1,780 / weekend 1,886. Sat ~5 beers (~1,200 kcal) → week avg ~1,980 kcal. |
| Weeks 3–4 (21 Jun – 5 Jul) | ~2,150 | Add oats (~175 kcal/day) to weekday plan to bridge gap. |

- **Food tracking intent:** not logging food unless waist exceeds 102 cm on 2 consecutive weekly readings
- **Waist monitoring:** weekly, same protocol (navel, relaxed, fasted morning). Alert at 102 cm.
- **7d avg ceiling:** 84.0 kg — unchanged
- **Protein:** 160g+/day (weekday ~162g, weekend ~150g)

**Pending actions before Phase 2:**
- Book DEXA scan (DexaStrong, Leeds) — late June / early July, after glycogen fully restored
- Book blood panel (T, LH, LDL, HOMA-IR) — early July, after 2–3 weeks at full maintenance
- Eye specialist appointment: 29 Jun (CSC)

---

## Session notes — 4 Jun 2026

### Phase 1 end — final metrics

- **Weight:** 79.0 kg this morning / 7d avg **79.4 kg** (29 May–4 Jun)
- **Waist:** **99 cm** (navel, self-measured, fasted) — down from 108 cm baseline = **−9 cm**
- **Total loss:** 6.8 kg from phase start (85.8 kg, Apr 13); 4.7 kg from week-2 start (84.1 kg, Apr 20)
- **Phase 1 verdict:** target was 82 kg / ~102–104 cm waist — delivered 79.0 kg / 99 cm. 3 kg and 5 cm ahead of target. Full strength preserved (squat 100 kg ×4 consecutive matches, deadlift 140 kg, DB press 35 kg × 7–8 reps new PB).

### Phase 1 end photos logged

- New progress set created: `profile/body-comp/progress/2026-06-04_phase1-end-99cm/` (5 poses, all directly comparable to prior sets)
- Catalogue updated in `profile/body-comp/README.md`

### App recalibrated to data-derived TDEE

Three fields updated in `logs/dashboard.json`:

| Field | Old | New | Reason |
|-------|-----|-----|--------|
| `maintenance_kcal` | 1,935 | **2,200** | Data-derived TDEE validated at 6-week check-in (25 May) |
| `weekly_deficit_target` | 3,500 | **5,300** | Aligns with meal plan base deficit vs 2,200 TDEE (5,302 kcal/wk) |
| `carryover_start_date` | 2026-04-20 | **2026-04-13** | Full phase carryover from day 1; new carryover ≈ +385 kcal |

- **Carryover sanity check:** +385 kcal vs +273 before the change — close enough for continuity, more accurate
- **Deficit math cross-check:** app's 6-week cumulative (32,185 kcal) implies 4.2 kg fat + ~1.5 kg glycogen/water = 5.7 kg expected scale drop; actual was 6.0 kg. Gap of ~0.3 kg = within noise. Numbers align.
- **Burndown Y-axis** extended from 5k max → **7k max** (same 160px chart height, scale compressed). `index.html`.

### TDEE re-check with full 45-day dataset (4 Jun)

- (84.1 − 79.4) × 7,700 ÷ 45 = 804 kcal/day deficit + 1,435 avg intake = **2,239 kcal/day**
- vs May 25 estimate of 2,205 — nudge of +34 kcal. Within noise. **2,200 remains the planning anchor.**
- Maintenance target for July: Mathew intends to aim for **~2,150 kcal/day** (slightly conservative, not recorded in dashboard — working number only).

### VO2 max

- Last reading: **37.74 mL/kg/min** (May 26 export, ~79.8 kg). Export 9 days old as of today.
- **Action before Italy:** run fresh Apple Health export (goal: Jun 5–6) to capture phase-end reading at 79.0 kg.
- Passive-only projection at 79.0 kg: 2,822 ÷ 79.0 = **35.7 mL/kg/min** — fitness-driven gain component is anything above that.

---

## Session notes — 25 May 2026

### 6-week TDEE check-in — validated

- **TDEE revised to ~2,200 kcal/day** (up from 2,050–2,075 at 10 May estimate)
- Calculation: 84.1 kg (Apr 20) → 80.6 kg (7d avg May 25), 35 days → 770 kcal/day deficit + 1,435 avg intake = 2,205 kcal/day
- **Phase 2 maintenance planning target revised from 2,100 → 2,200 kcal/day**
- **Metabolic phenotype:** spendthrift supported. TDEE above formula baseline (1,850–2,000), rate sustained at 35 days with no crash, RHR/HRV improving throughout. Not confirmed without calorimetry but consistent across all signals.
- **True average daily deficit: ~765 kcal/day (~5,350 kcal/week).** The app tracked against a 1,935 kcal/day maintenance baseline (the dashboard figure, used as a conservative anchor because the real TDEE wasn't known at phase start). The true TDEE turned out to be ~2,200 kcal/day — 265 kcal/day higher than assumed. This means the actual deficit was ~54% above the planned 500 kcal/day (3,500 kcal/week target). The app's burndown showed ~3,500 kcal/week achieved, which is correct relative to the 1,935 baseline, but the real-world deficit was materially larger. This explains the faster-than-projected rate of loss.
- **Scale milestone:** 79.8 kg this morning — first reading below 80 kg. Live target of 80 kg is hit with 12 days remaining.
- **7d avg: 80.6 kg.** Projected end-of-phase (Jun 6): ~79.4 kg 7d avg, scale potentially 78.5–79 kg.

---

## Session notes — 14 May 2026

### Planned social drinking night — Saturday 30 May
- Drinks with friends planned. Strategy agreed for minimising cut damage:
  1. Eat a high-protein meal (40g+ protein) before going out
  2. Choose spirits + slimline mixer first; Guinness if wanting a pint
  3. Front-load deficit Mon–Fri 25–29 May (clean eating + runs/stairs)
  4. Sunday 31 May: return to plan immediately, no compensation restriction
  5. Expect scale 0.5–1.0 kg higher Sun/Mon — not fat, resolves in 48 hrs

### Alcohol and water retention — mechanism (14 May 2026)
- Spirits cause less water retention than beer primarily because of **carb content**, not because alcohol is processed differently
- Beer = ADH rebound *plus* glycogen-water loading (10–20g carbs/pint × ~3g water per g glycogen)
- Spirits + slimline mixer = ADH rebound only (0g carbs)
- Guinness is the lowest-carb pint option (~10g/pint); dry white wine is similarly efficient (~1–2g carbs/125ml)
- ADH suppression (dehydration → rebound water retention) is driven by alcohol quantity and affects all drinks equally

### Drinks ranked by glycogen storage impact (lowest → highest carbs)

**Tier 1 — ~0g carbs (no glycogen effect)**
- Spirit neat (gin, vodka, whisky, rum, tequila)
- Spirit + soda water
- Spirit + slimline/diet tonic (~65 kcal)

**Tier 2 — ~1–4g carbs per drink**
- Brut Nature / Extra Brut champagne or prosecco
- Dry white wine (Sauvignon Blanc, Pinot Grigio, Chablis) — ~120 kcal/175ml
- Dry red wine — ~160 kcal/175ml
- Dry rosé

**Tier 3 — ~8–15g carbs per drink**
- G&T with regular tonic (~120 kcal)
- Guinness — ~10g/pint (~155–210 kcal depending on size)
- Standard lager (Heineken, Peroni) — ~10–12g/pint
- Negroni — ~12–15g (~185 kcal)

**Tier 4 — ~12–25g carbs per drink**
- Aperol Spritz — ~15–20g
- Pale ale — ~12–16g/pint
- IPA — ~15–20g/pint (~270 kcal/pint)
- Mojito — ~25–30g

**Tier 5 — avoid on a cut (~20–50g+ per drink)**
- DIPA / strong ales — ~20–30g/pint
- Cider — ~20–25g/pint
- Alcopops (WKD, Smirnoff Ice) — ~30–40g/bottle
- Piña colada, Long Island Iced Tea — ~35–50g

---

## Session notes — 13 May 2026 (afternoon)

### Hunger increase — first noted 13 May
- Afternoon hunger (pre-dinner) and going-to-bed hungry noted for the first time. Day 30 of phase, ~25% BF.
- Consistent with leptin drop at this stage — as fat mass decreases, leptin production falls and hunger signals increase. Normal physiology, not a red flag.
- Response: added a single whey shake (~116 kcal) as a mid-afternoon bridge on hungry days. Low calorie cost, good protein hit.
- Also noted: Caesar salad lunch (30g protein) is lower satiety than the chicken wrap (51g protein). Protein quantity matters for satiety during a deficit.
- **Low-cal satiety options identified:** sparkling water, Pepsi Max, black coffee, pickles, cucumber, Fage 0% yoghurt, miso soup (especially for bedtime hunger).
- Weight still flat 4 days (81.5–81.7 kg) — not a plateau, normal noise. 7-day avg is the signal. 4-day flat at this stage likely reflects water catching up to real fat loss rate after early glycogen/water flush.

### Dr. Mike Israetel / Renaissance Periodization video review (13 May)
- Video: "I Lost Over Half My Body Fat DOING THIS" (YouTube, Jan 2026 approx). 15.6% → 6.0% BF over ~15 weeks.
- **Transferable takeaways:**
  1. **10,000 steps/day** is the single most-emphasised practical lever — Dr. Mike tried 12k and 14k but found 10k was the sweet spot (diminishing fatigue returns above that). Directly validates the steps lever in the plan as the first response to any stall.
  2. **Conservative progression during a cut** — 2.5 lbs/week or +1 rep. Don't chase big strength gains; provide just enough stimulus to retain muscle and keep strength stable.
  3. **Consistency formula** (his closing takeaway): high protein + moderate calorie deficit + 10k steps + regular weight training = the transformation formula. Drugs help but don't replace this.
- **Non-transferable (pharmacological context):** Results included gaining 9.7 lbs of lean mass simultaneously — enabled by escalating TRT from 150mg → ~750mg testosterone-equivalent + SARMs. The fat loss methodology transfers; the simultaneous recomp at that rate does not apply to a natural trainee.
- He also used tirzepatide + retatrutide (GLP-1/GIP/glucagon triple agonist) to manage steroid-induced hunger and preferentially reduce visceral fat. Transparent about this.

### Retatrutide (reta) — UK status (13 May 2026)
- **Not approved anywhere.** Still in Phase 3 trials. FDA approval expected late 2026/early 2027. MHRA (UK) approval would follow, putting realistic UK availability at **2027–2028**.
- NHS availability would require additional NICE evaluation — likely 2028 or later.
- **Closest available UK equivalent now:** Mounjaro (tirzepatide, dual GLP-1/GIP agonist) — available privately. ~22.5% average weight loss in trials.
- **Relevance to Mathew:** not needed given current progress. Worth revisiting after July blood panel **only if** HOMA-IR and fasting glucose haven't improved with fat loss.

---

## Session notes — 12 May 2026 (afternoon)

### Thrifty vs spendthrift metabolic phenotype — tentative assessment
- Studied Hollstein et al. 2020 (*J Clin Endocrinol Metab*) — the NIH study on thrifty vs spendthrift metabolism referenced in Jeremy Ethier's 3 Jan 2026 YouTube video.
- Key finding: thrifty people have *higher* metabolism at energy balance, not lower — their metabolism crashes more steeply during a deficit. Spendthrift people burn less at balance but maintain more of that burn during a cut (driven by 4× higher epinephrine response to fasting).
- **Tentative verdict: spendthrift.** Three converging signals as of 4 weeks in:
  1. Data-derived TDEE (~2,050–2,075) is above formula baseline (~1,850–2,000) — higher actual burn than predicted
  2. Loss rate (~0.87 kg/week 7d-avg) sustained at 4 weeks with no metabolic crash
  3. RHR and HRV both *improving* during the cut — body not fighting the deficit
- **Not confirmed.** Cannot know without whole-room calorimetry. Pending validation at 25 May check-in — if rate is still solid at 6 weeks (water weight fully settled), spendthrift more likely.
- Research saved: `research/metabolic/thrifty-spendthrift-phenotype-2020.md`

---

## Session notes — 12 May 2026

### Apple Health export refreshed
- New export processed (12 May 2026). `profile/health-metrics.md` updated.
- VO2 max: 35.45 → **36.6 mL/kg/min** (+1.15 in 7 days). Absolute VO2 baseline: 2,822 mL/min (recorded in snapshot for projection maths).
- RHR: 56.3 → 55.0 bpm. HRV: 53.6 → 54.5 ms. Sleep: 7.4 → 7.6 hrs. All trending right.
- Passive uplift from 3.9 kg weight loss: ~1.3 mL/kg/min (~35% of total gain). Fitness-driven gain: ~2.4 mL/kg/min (~65%). See VO2 Max working figures table below.

### VPA frequency gap identified (12 May 2026)
- Current confirmed VPA: ~2–3 days/week (runs + stair sessions). Hill bursts on rides add unmeasured VPA.
- Evidence-backed target: 5–6 days/week of some vigorous effort (even 2–5 min counts as VILPA).
- This is the primary cardiorespiratory gap. Not urgent during the cut — establish the habit going into Phase 2.
- Research ingested: Biswas et al. Nat Comms 2025 + Stamatakis VILPA Nat Med 2022. See `research/activity/vigorous-exercise-equivalence-vilpa-2025.md`.

### VILPA / exercise philosophy codified (12 May 2026)
- Short frequent vigorous efforts are the primary target — not longer runs.
- Time-poor constraint is a hard requirement. Frequency over duration.
- Exercise philosophy section added to this snapshot and to `profile/profile.md`.
- Numerical reasoning rule added to `.cursor/rules/health-context.mdc` to prevent sloppy maths in future sessions.

### Phase status (12 May 2026)
- Weight: 81.6 kg (evening). 7-day avg: 82.2 kg. Start: 85.8 kg. Loss: 3.9–4.2 kg depending on reading.
- 80 kg target by 6 Jun: 2.2 kg remaining over ~25 days (~0.6 kg/week needed) — comfortably on track.
- Waist: 103 cm (8 May). Strength fully preserved. Phase outperforming on all dimensions.

### Log correction (12 May 2026)
- `2026-05-10 | cheat | Guinness & Crisps, ~355 kcal` was incorrectly combined. Corrected in app to:
  - `2026-05-10 | drinks | 155 | Guinness` (now correctly subtracted from deficit)
  - `2026-05-10 | cheat | Crisps, ~200 kcal`

---

## Session notes — 10 May 2026

### Revised Phase 1 target: 80 kg (from 82 kg)
- Original dashboard target of 82 kg was **hit on 9 May 2026**, 28 days early. Dashboard left unchanged as historical record of the original plan.
- **New live target: 80 kg by 6 Jun 2026.** Rationale: current trajectory (0.83 kg/wk) already points to ~79.4 kg; 80 kg is the conservative version of where this is heading.
- Phase 2 insurance: ending leaner absorbs the maintenance rebound and gives Phase 2 a better starting position.
- Waist at 80 kg expected to be ~100–101 cm (vs 102–104 cm target at 82 kg).

### Maintenance rebound expectation (confirmed understanding)
- Returning to maintenance calories will add **~1.5–2 kg on the scale** within 1–2 weeks — this is glycogen (~400–500g) + bound water (~3g per g glycogen), stored in **skeletal muscle and liver**, not in fat depots.
- Gut content adds another ~0.3–0.5 kg.
- **Scale at full maintenance: ~82–82.5 kg from an 80 kg depleted starting point.** Waist measurement unchanged — glycogen does not live in love handles or belly.
- Rolling average ceiling for maintenance month remains 84 kg. If it plateaus at 82–82.5 kg and stops, that's the plan working.

### Maintenance calorie baseline (revised upward — 10 May 2026)
- Earlier estimate of ~1,950–2,050 kcal/day was algorithm-based. Phase 1 back-calculation (10 May) revised this upward to **~2,050–2,075 kcal/day**. See the *Estimated maintenance* section above for full derivation.
- Phase has run hot due to elevated activity (MTB rides, stair sessions, higher step count) — these are logged as additive workout kcal, not baked into the baseline.
- Dashboard `maintenance_kcal` (1,935) left unchanged as a conservative anchor; use 2,050–2,075 for planning and back-calculation purposes.

---

## Session notes — 9 May 2026

### Phase milestone — Italy target hit 28 days early
- Morning weight **82.0 kg** on 9 May 2026 — the exact Phase 1 target, with 28 days still remaining (phase end: 6 Jun 2026)
- 7-day rolling avg: **82.73 kg** — well inside the 82 kg target zone
- Rate of loss has been ~0.83 kg/wk (target was 0.45 kg/wk) — nearly double, with no strength regression
- Waist: **103 cm** (8 May) — inside the Phase 1 success range (102–104 cm), 28 days ahead of schedule
- **Strength fully preserved:** squat 100 kg (matched pre-phase max), deadlift 140 kg (clean, confirmed Scenario A), DB chest press 35 kg × 5–6 reps (near all-time best)
- **Next decision:** whether to push toward 80–81 kg (Phase 2 insurance option — already flagged in profile as preferred), ease deficit, or hold pace. To be discussed after Sunday's ride and weekly review.

### Rex
- AI coach/assistant name chosen by Mathew on 9 May 2026. Name was self-chosen by the AI and approved by Mathew. Recorded in `.cursor/rules/health-context.mdc`.

---

## Session notes — 5 May 2026

### Weight spike explanation (83.5 kg on 5 May)
- **Imodium taken ~Sun 3 May** to settle an upset stomach. Caused 2–3 days of constipation. Being backed up can add 0.5–1.5 kg on the scale with zero fat change. Explains a significant portion of the 5 May spike.
- **Bank holiday weekend (2–4 May)** also contributed: May 2 was essentially a zero-deficit day (4–5 pints + Watt bar dinner despite 101-min ride), May 4 had another pint + Cutlery Works. Three consecutive days of restaurant food + alcohol = glycogen + sodium + alcohol water retention.
- **Not a fat story.** 7-day avg was 82.9 kg — only 0.9 kg from Italy target. Scale expected to drop back to 82–83 range within 2–3 days once constipation resolves.

### Ride day + social occasion behavioural heuristic (validated 5 May 2026)
- A big e-MTB ride does **not** create a licence for both a restaurant meal *and* significant drinking on the same day.
- After the 0.65 correction factor, even a 100-min ride ≈ ~680 kcal of real burn — roughly one restaurant meal's buffer, not a restaurant meal + 4–5 pints.
- **Decision rule:** on a ride day that is also a social occasion, treat the ride as covering one of the two extras (the meal *or* the drinks), not both. If both happen, log it as a near-zero deficit day and don't compensate by eating less the next day — just return to plan.

---

## Session notes — 2 May 2026

- **Gym performance:** Feeling strong as of 2 May — no strength drops noted despite running above 1 kg/week loss rate. Key signal for 8–9 May check-in: if this holds, no calorie adjustment needed (Scenario A/B). If strength drops appear, add 100–150 kcal/day immediately.
- **Monday weight warning:** 2 May involved 101 min cycling (1,045 kcal) + 3–4 pints + higher-calorie dinner (~400 kcal above plan). Expect Monday 4 May scale to read 0.5–1.5 kg above today's 82.2 due to glycogen refill, alcohol, sodium. Not fat gain — do not panic. Use 7-day avg, not daily readings.
- **Whey protein:** MyProtein Impact Whey (not isolate), various flavours. Dashboard shows 116 kcal / 21g protein per scoop (single) and 232 kcal / 42g protein (double) — consistent with Impact Whey macros. No need to update if flavour changes.
- **Ashwagandha check-in (13 May 2026):** 18 days in. **Reported feeling calmer and less stressed** — consistent with the 2–4 week cortisol/stress window. Testosterone effects not expected until 8–12 weeks (retest July 2026 with lipid panel). No side effects noted. Continue monitoring at 25 May 6-week check.

---

## Strength check-ins — Phase 1

| Date | Movement | Result | Verdict |
|---|---|---|---|
| 2 May 2026 | General | No drops noted | Scenario A — no change |
| 6 May 2026 | Squat 1RM | **100 kg** — matches pre-phase max | ✅ Strength preserved |
| 6 May 2026 | Deadlift | Failed 140 kg | ⚠️ Explained by BH weekend MTB fatigue (101+65 min rides 2–3 days prior, posterior chain unrecovered). Curls + lateral raises were above normal same session = systemic strength fine. **Not a muscle loss signal.** |
| 6 May 2026 | Dips | More reps than normal (BW + 15 kg plate) | ✅ Upper body strength maintained/improving |
| 9 May 2026 | Deadlift retest | **140 kg — clean pull, felt good** | ✅ Scenario A confirmed — May 6 failure was MTB fatigue, not strength decline. No calorie adjustment needed. |
| 9 May 2026 | DB Chest Press | **35 kg × 5–6 reps — near all-time best** | ✅ Upper body strength at personal best levels during a deficit — strong muscle retention signal |
| 13 May 2026 | Squat 1RM | **100 kg with knee sleeves (first time using them)** | ✅ Matched pre-phase max — knee sleeves felt good; will use going forward |
| 21 May 2026 | Squat 1RM | **100 kg** | ✅ Third consecutive match of pre-phase max — strength fully preserved at 80.7 kg / week 5 of cut |
| 27 May 2026 | Squat 1RM | **100 kg** | ✅ Fourth consecutive match of pre-phase max — strength fully preserved at 79.9 kg |
| 2 Jun 2026 | DB Chest Press | **35 kg × 7–8 reps** | ✅ New rep PB — beats May 9 (5–6 reps). Upper body strength improving during the cut at 79.5 kg. |
| 31 May 2026 | Deadlift | **140 kg** | ✅ Same load as May 9 retest, now at 79.5 kg — 6 kg lighter body weight. Strong muscle retention signal going into maintenance. |

**Decision rule:** ~~Planned retest to confirm~~ **Resolved 9 May — Scenario A confirmed across all movements. No calorie adjustment needed.**

---

## Phase 1 check-in schedule

| Date | Action |
|------|---------|
| **~8–9 May 2026** | **Weekly check.** Pull log, compute 7-day avg weight (2–8 May) vs prior week avg (~83.24 kg for 25 Apr–1 May). Apply scenario framework below. |
| **~25 May 2026** | **6-week check-in.** (1) TDEE back-calculation: use total weight change + avg intake to tighten estimate. Decide if ~2,100 maintenance stands or needs updating. (2) **Metabolic phenotype assessment:** by 6 weeks, water weight is settled and rate-of-loss signal is clean. If 7-day avg is still dropping at ~0.4–0.7 kg/week on current intake, spendthrift phenotype is supported. If rate has slowed significantly (< 0.3 kg/week) without obvious dietary cause, thrifty adaptation may be occurring — consider increasing activity rather than cutting calories further. See `research/metabolic/thrifty-spendthrift-phenotype-2020.md`. |
| **6 Jun 2026** | **Phase end.** Start maintenance at ~2,200 kcal + cardio as additive. |
| **7–13 Jun 2026** | **Italy.** City walking, no training. Refeed naturally — expect ~0.5–1 kg glycogen rebound (lower than sedentary refeed due to high steps). |
| **Late Jun / early Jul** | **DEXA scan** (DexaStrong, Leeds) + **blood test** (testosterone, LDL, HOMA-IR, fasting glucose). Both to be done before Phase 2 start. DEXA post-Italy gives better lean mass reading with glycogen fully restored. |

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

## Apple Health metrics (4 Jun 2026 export — current)

| Metric | 30-day avg | 90-day avg | Trend | Notes |
|---|---|---|---|---|
| Total sleep | 7.7 hrs | 7.4 hrs | Stable | Unchanged |
| REM sleep | 2.3 hrs | 2.1 hrs | Stable | ↑ +0.1 vs May 26 |
| Core sleep | 4.5 hrs | 4.0 hrs | Stable | ↑ +0.2 vs May 26 |
| Deep sleep | 0.6 hrs | 0.6 hrs | Stable | AW known to undercount deep |
| Respiratory rate | 15.9 br/min | 16.4 br/min | Stable | Normal (12–20) |
| SpO2 | 96.8% | 96.7% | Stable | Normal; no apnea concern |
| Wrist temp (sleep) | 35.9 °C | 36.1 °C | Stable | Normal |
| Resting HR | **53.8 bpm** | 58.0 bpm | ↓ **−4.2 bpm vs 90d** | ↓ −0.8 vs May 26 — continuing to fall |
| HRV (SDNN) | **57.8 ms** | 52.6 ms | ↑ up 5.2 | ↑ +1.9 ms vs May 26 — phase-end best |
| Steps/day | **9,365** | 7,446 | ↑ +1,919 vs 90d | ↑ +502 vs May 26 |
| Active kcal/day | **845.8** | 652.2 | ↑ +193.6 vs 90d | Essentially flat vs May 26 |
| Exercise min/day | **72.5** | 42.2 | ↑ +30.3 vs 90d | ↑ +3.6 min vs May 26 |
| VO2 Max | **37.98** mL/kg/min | — | ↑ **+0.24 from May 26** | +5.09 since Apr. Passive (weight) 56% / fitness 44%. Target: 40+ by Sep 2026. |

> Source: `profile/health-metrics.md` (auto-generated from Apple Health export). Refresh this table when a new export is run.

### VO2 Max — working figures (17 May 2026)

| Figure | Value | Notes |
|---|---|---|
| VO2 max at Apr export | 32.89 mL/kg/min | Baseline, ~85.8 kg |
| VO2 max at May 5 export | 35.45 mL/kg/min | ~82–83 kg range |
| VO2 max at May 12 export | 36.6 mL/kg/min | 81.9 kg |
| VO2 max at May 17 export | 36.73 mL/kg/min | ~80.7 kg |
| VO2 max at May 26 export | 37.74 mL/kg/min | ~79.8 kg |
| VO2 max at Jun 4 export | **37.98 mL/kg/min** | 79.0 kg — **phase-end reading** |
| Total improvement since Apr | **+5.09 mL/kg/min** | |
| Absolute VO2 at baseline | **2,822 mL/min** | 85.8 kg × 32.89 — use this to project forward |
| Passive uplift from weight loss (85.8 → 79.0 kg) | ~2.83 mL/kg/min | 2,822 ÷ 79.0 − 32.89 |
| Passive uplift as % of total gain | **~56%** | 2.83 ÷ 5.09 |
| Fitness-driven gain (residual) | **~2.26 mL/kg/min** | Total − passive — genuine aerobic adaptation |
| Projected VO2 max at 78 kg (passive only) | **~36.2 mL/kg/min** | 2,822 ÷ 78 − 32.89 — fitness gains add on top |
| Projected VO2 max at 78 kg (passive + continued fitness) | **~39–41 mL/kg/min** | Assumes ~2–3 mL/kg/min further fitness gain by Sep 2026 |

**Rule for future VO2 max projections:** always split the gain into (a) passive weight-loss component (2,822 ÷ new_kg − current reading) and (b) fitness-driven component. Never attribute all improvement to one factor without showing the split.

**Cross-reference rule for agents:** `profile/health-metrics.md` is authoritative for Apple Health data. If `profile/profile.md` shows "Not recorded yet" for sleep, HRV, resting HR, or VO2 max, check `health-metrics.md` before concluding the data is missing. Flag any gap to the user and offer to backfill `profile/profile.md`.

---

## Exercise philosophy & VPA guidance (established 12 May 2026)

> **Read this before making any cardio or fitness recommendations.** It supersedes generic advice to "run longer" or "add Zone 2."

### Core principle — frequency over duration

Based on the 2025 Nature Communications study (Biswas, Ahmadi, Stamatakis et al.) and the 2022 VILPA Nature Medicine paper, the evidence strongly supports **short, frequent vigorous efforts** as the highest-ROI cardio approach for Mathew. See `research/activity/vigorous-exercise-equivalence-vilpa-2025.md`.

- The true VPA:MPA equivalence ratio is **4–10x** (not 2x as assumed by WHO guidelines)
- **VILPA (1–2 min vigorous bouts, 3–4×/day)** in non-exercisers cuts all-cause mortality ~40% and cancer mortality ~50%
- Light activity (LPA) **cannot** achieve more than ~15% risk reduction regardless of volume
- The dose-response is nearly linear — every additional VPA minute has meaningful returns

### Mathew's current VPA sources (confirmed vigorous, HR 144–161 bpm)

| Source | Frequency | Notes |
|---|---|---|
| Runs | 1–2×/week | 19–24 min, 144–161 bpm — confirmed vigorous |
| Stair sessions | 1–2×/week | 20–25 min, 147 bpm — confirmed vigorous |
| Ride hill bursts | Multiple per ride | Hard climbs during MTB/e-bike sessions; natural interval pattern |

Estimated confirmed VPA: **~40–50 min/week** on average (excluding hill bursts, which add meaningfully but aren't measured precisely).

### Constraints to respect always

- **Time-poor** — efficiency is a hard requirement, not a preference
- Sedentary job means incidental VILPA (stairs, fast walking) is the most time-efficient VPA lever
- Runs do **not** need to get longer — the current 19–24 min runs are appropriate; more days > longer sessions
- E-bike rides already accumulate real VPA via hill climbs — do not discount these

### Target state

- VPA on **5–6 days/week** (currently ~2–3) — primary gap to close
- Each vigorous effort can be as short as **2–5 minutes** (VILPA counts)
- VO2 max from **35.45 → 40+ mL/kg/min** over 6–12 months (weight loss + more VPA frequency)
- Do NOT suggest adding long Zone 2 sessions or extending run duration as the primary lever

### Recommended default suggestions (in priority order)

1. **Protect existing stair sessions** — highest VPA density per minute of commitment
2. **Add a second short run mid-week** — 15–20 min is sufficient; don't extend existing ones
3. **Exploit VILPA opportunities** — office stairs at pace, fast walking uphill, a 90-second sprint burst during a lunchtime walk
4. **Ride hard on climbs** — already doing this; validate and count it explicitly
5. **Structured intervals (optional uplift)** — 4×4 min hard / 3 min easy is the most evidence-backed VO2 max protocol if time allows once per week

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

## PWA / local dev

> Full app state, dev setup, diagnostic checklist, and changelog live in **`docs/app-state.md`**. Read that file before making any PWA changes.
> Agent entry point for the `docs/` folder: **`docs/AGENTS.md`**.

**Quick start:** F5 or Cmd+Shift+B starts the server on port 8765 and opens the Cursor Simple Browser. URL: `http://localhost:8765/docs/index.html`. On localhost the SW is auto-bypassed — every reload serves fresh files.

**If changes don't appear:** test the server first with curl before assuming a cache issue. See `docs/app-state.md` → Diagnostic order.
