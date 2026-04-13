# Phone Log

> Append-only log written by the Health Logger PWA.
> Do not edit manually — entries are added by the app from your iPhone.
> Claude reads this at the start of each session to process new entries.

## Format

All entries: `YYYY-MM-DD | type | value | [optional note]`

| Type | Format | Example |
|---|---|---|
| `weight` | `DATE \| weight \| KG \| [note]` | `2026-04-13 \| weight \| 85.8 \| Post-spa` |
| `drinks` | `DATE \| drinks \| TOTAL_KCAL \| breakdown \| [note]` | `2026-04-19 \| drinks \| 370 \| Pint of beer x1, Negroni x1 \| Birthday` |
| `beers` | `DATE \| beers \| PINTS` | `2026-04-19 \| beers \| 3` _(legacy — use drinks)_ |
| `activity` | `DATE \| activity \| description \| [note]` | `2026-04-19 \| activity \| Walk, 45 min` |
| `cheat` | `DATE \| cheat \| description \| [note]` | `2026-04-19 \| cheat \| Pizza, ~800 kcal extra \| Family dinner` |
| `run` | `DATE \| run \| DURATION min \| DIST km \| KCAL kcal \| BPM bpm` | `2026-04-19 \| run \| 15.0 min \| 2.32 km \| 176 kcal \| 162 bpm` |
| `stair` | `DATE \| stair \| DURATION min \| KCAL kcal \| BPM bpm` | `2026-04-19 \| stair \| 25.0 min \| 230 kcal \| 145 bpm` |

`run` and `stair` entries are auto-logged by the iOS Shortcut after each Apple Watch workout.

**Outlier effect on weekly deficit:**
- `run` / `stair` — adds to deficit (positive)
- `drinks` / `beers` — reduces deficit (negative)
- `cheat` — reduces deficit if `~NNN kcal extra` is included in the description

## Log

2026-04-13 | weight | 85.8 | Morning after spa evening, two rounds of sauna + ice baths
2026-04-13 | run |  min |  km | 1.917 kcal
2026-04-13 | run |  min |  km | 1.917 kcal
