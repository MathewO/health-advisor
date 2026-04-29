# Phone Log

> Append-only log written by the Health Logger PWA.
> Do not edit manually — entries are added by the app from your iPhone.
> Claude reads this at the start of each session to process new entries.

## Format

All entries: `YYYY-MM-DD | type | value | [optional note]`

| Type | Format | Example |
|---|---|---|
| `weight` | `DATE \| weight \| KG \| [note]` | `2026-04-13 \| weight \| 85.8 \| Post-spa` |
| `waist` | `DATE \| waist \| CM \| [note]` | `2026-04-21 \| waist \| 106 \| Navel, relaxed, end of exhale, fasted morning` |
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
2026-04-14 | weight | 85.1
2026-04-14 | run | 20 min |  km | 188 kcal
2026-04-15 | weight | 85
2026-04-15 | waist | 108 | Baseline — navel, relaxed, end of exhale, fasted morning (body comp)
2026-04-16 | weight | 84.6 | Bad tummy last night
2026-04-16 | run | 20 min |  km | 192 kcal
2026-04-16 | drinks | 89 | Alcohol free beer
2026-04-16 | cheat | Caesar Salad + chips, ~650 kcal | replaces: Gousto Meal (640 kcal)
2026-04-17 | weight | 84.6
2026-04-17 | cheat | Skipped coffee | replaces: Coffee + Oatly (50 kcal)
2026-04-17 | cheat | Anchovies, ~50 kcal
2026-04-17 | cheat | Lux pasta, ~780 kcal | replaces: Gousto Meal (640 kcal)
2026-04-18 | weight | 84.2
2026-04-18 | workout | Cycling | 92 min | 783 kcal
2026-04-18 | cheat | Pasta, ~300 kcal | replaces: Weekend Brunch (648 kcal)
2026-04-18 | cheat | Sausage roll + coffee, ~400 kcal
2026-04-18 | workout | Walking | 23 min | 106 kcal
2026-04-18 | cheat | Double shake, ~220 kcal | replaces: Single Shake (116 kcal)
2026-04-18 | drinks | 312 | 1/2 bottle win
2026-04-18 | cheat | Greedy Greek, ~1100 kcal | replaces: Gousto Meal (640 kcal)
2026-04-18 | cheat | Skipped pudding | replaces: Milk Chocolate (100 kcal)
2026-04-19 | weight | 83.9
2026-04-19 | cheat | Omelette, ~250 kcal | replaces: Weekend Brunch (648 kcal)
2026-04-19 | cheat | Coffee, ~50 kcal | replaces: Single Shake (116 kcal)
2026-04-19 | cheat | Broadfield, ~1250 kcal | replaces: Gousto Meal (640 kcal)
2026-04-19 | cheat | Ice cream, ~102 kcal | replaces: Milk Chocolate (100 kcal)
2026-04-20 | weight | 84.1 | Big roast dinner yesterday
2026-04-20 | cheat | Tuna Power Bowl, ~508 kcal | replaces: Chicken Wrap (376 kcal)
2026-04-20 | workout | Walking | 34 min | 134 kcal
2026-04-21 | weight | 84.2
2026-04-21 | run | 24 min |  km | 216 kcal
2026-04-21 | cheat | Turkey Meatball Spaghetti, ~400 kcal | replaces: Chicken Wrap (376 kcal)
2026-04-22 | weight | 83.7
2026-04-22 | cheat | Gousto Calories, ~28 kcal
2026-04-22 | cheat | Turkey Meatball Spaghetti , ~400 kcal | replaces: Chicken Wrap (376 kcal)
2026-04-23 | weight | 83.8
2026-04-23 | run | 20 min |  km | 215 kcal
2026-04-23 | cheat | Turkey Meatball Spaghetti, ~400 kcal | replaces: Chicken Wrap (376 kcal)
2026-04-23 | cheat | Caesar Salad + Bread, ~690 kcal | replaces: Gousto Meal (640 kcal)
2026-04-24 | weight | 83.4
2026-04-24 | waist | 106 | Navel, relaxed, end of exhale, fasted morning
2026-04-24 | cheat | Turkey Meatball Spaghetti, ~400 kcal | replaces: Chicken Wrap (376 kcal)
2026-04-24 | workout | Walking | 23 min | 97 kcal
2026-04-24 | drinks | 190 | Green mountain
2026-04-24 | cheat | Prawn Stir Fry, ~510 kcal | replaces: Gousto Meal (640 kcal)
2026-04-25 | weight | 83.7 | One pint after work yesterday
2026-04-25 | cheat | Bacon roll + eggs, ~550 kcal | replaces: Weekend Brunch (648 kcal)
2026-04-25 | workout | Walking | 15 min | 84 kcal
2026-04-25 | workout | Walking | 16 min | 85 kcal
2026-04-25 | cheat | Skipped shake | replaces: Single Shake (116 kcal)
2026-04-25 | drinks | 56 | AF beer
2026-04-25 | workout | Walking | 31 min | 161 kcal
2026-04-25 | drinks | 454 | Pale ale, Cobra
2026-04-25 | cheat | Skipped chocolate | replaces: Milk Chocolate (100 kcal)
2026-04-25 | cheat | BBQ, ~1050 kcal | replaces: Gousto Meal (640 kcal)
2026-04-26 | stair | 25 min | 241 kcal
2026-04-26 | weight | 83.3
2026-04-26 | cheat | Sandwich, ~600 kcal | replaces: Weekend Brunch (648 kcal)
2026-04-26 | drinks | 155 | Aperol Spritz
2026-04-26 | cheat | Urban pitta, ~700 kcal | replaces: Gousto Meal (640 kcal)
2026-04-27 | weight | 83.2
2026-04-27 | cheat | Egg fried rice, ~570 kcal | replaces: Chicken Wrap (376 kcal)
2026-04-27 | cheat | Gousto, ~458 kcal | replaces: Gousto Meal (640 kcal)
2026-04-27 | cheat | Skipped chocolate | replaces: Milk Chocolate (100 kcal)
2026-04-28 | weight | 83.1
2026-04-28 | run | 22 min |  km | 202 kcal
2026-04-29 | weight | 83.5
2026-04-29 | workout | Walking | 13 min | 62 kcal
2026-04-29 | workout | Walking | 13 min | 68 kcal
