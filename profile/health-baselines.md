# Health Baselines — Point-in-Time Snapshots

> Append-only record of Apple Health export snapshots. Unlike `health-metrics.md` (which is overwritten on each export), this file accumulates all historical readings for trend comparison over months/years.
>
> Updated automatically by `scripts/parse_apple_health.py`. Do not delete rows.

---

## How to Read This File

Each row is a 30-day average at the time of the export. Use this to compare across phases, before/after interventions, and year-over-year.

---

## Snapshot History

| Export date | Phase context | Weight (scale) | Sleep (total) | REM | Core | Deep | Resp rate | SpO2 | Wrist temp | Resting HR | HRV (SDNN) | VO2 Max | Steps/day | Active kcal/day |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-04-12 | Pre-phase / Randox baseline | 85.8 kg (13 Apr start) | 7.2 hrs | — | — | — | — | — | — | 59.6 bpm | 53.0 ms | 32.89 | 7,292 | 595 kcal |
| 2026-05-05 | Phase 1 day 22 (82.9 kg 7d avg) | 83.5 kg (daily) | 7.4 hrs | 2.1 hrs | 4.0 hrs | 0.6 hrs | 16.4 br/min | 96.8% | 36.0 °C | 56.3 bpm | 53.6 ms | 35.45 | 8,138 | 717 kcal |

---

## Notable Deltas (Apr 12 → May 5, 23 days)

| Metric | Apr 12 | May 5 | Change | Interpretation |
|---|---|---|---|---|
| Resting HR | 59.6 bpm | 56.3 bpm | **−3.3 bpm** | Strong cardiovascular adaptation from training |
| HRV (SDNN) | 53.0 ms | 53.6 ms | +0.6 ms | Stable — not stressed despite deficit |
| VO2 Max | 32.89 | 35.45 | **+2.56** | Weight loss (kg denominator) + real fitness gain |
| Steps/day | 7,292 | 8,138 | **+846** | Phase driving more movement |
| Active kcal/day | 595 | 717 | **+122 kcal** | Higher activity, more exercise sessions |

---

## Planned Future Snapshots

| Target date | Context |
|---|---|
| ~7 Jun 2026 | End of Phase 1 (Italy trip). Compare post-cut vs pre-cut baseline. |
| ~5 Jul 2026 | End of maintenance month. Confirm recovery of resting HR / HRV / VO2 after refeeding. |
| ~12 Sep 2026 | End of Phase 2 (Bali). Full phase comparison. |
