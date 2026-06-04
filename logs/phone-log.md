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
2026-04-28 | weight | 83.4
2026-04-28 | run | 22 min |  km | 202 kcal
2026-04-29 | weight | 83.5
2026-04-29 | workout | Walking | 13 min | 62 kcal
2026-04-29 | workout | Walking | 13 min | 68 kcal
2026-04-29 | waist | 105
2026-04-29 | cheat | Caesar Salad, ~450 kcal | replaces: Gousto Meal (640 kcal)
2026-04-29 | drinks | 154 | Guinness
2026-04-30 | weight | 83
2026-04-30 | workout | Walking | 12 min | 61 kcal
2026-04-30 | workout | Walking | 22 min | 224 kcal
2026-04-30 | workout | Walking | 10 min | 76 kcal
2026-04-30 | cheat | Single shake, ~116 kcal
2026-04-30 | cheat | Crisps, ~60 kcal
2026-05-01 | weight | 82.6
2026-05-01 | workout | Cycling | 15 min | 107 kcal
2026-05-01 | cheat | Chicken burger + chicken, ~920 kcal | replaces: Gousto Meal (640 kcal)
2026-05-01 | cheat | Fruit Stack, ~55 kcal | replaces: Milk Chocolate (100 kcal)
2026-05-02 | weight | 82.2
2026-05-02 | cheat | Oats, ~185 kcal | replaces: Single Shake (116 kcal)
2026-05-02 | workout | Cycling | 101 min | 1045 kcal
2026-05-02 | cheat | Brunch, ~608 kcal | replaces: Weekend Brunch (648 kcal)
2026-05-02 | drinks | 210 | Pint of beer
2026-05-02 | drinks | 210 | Pint of beer
2026-05-02 | drinks | 180 | Half DIPA
2026-05-02 | drinks | 210 | Pint of beer
2026-05-02 | cheat | Watt bar, ~1100 kcal | replaces: Gousto Meal (640 kcal)
2026-05-02 | drinks | 155 | 2/3 Sour
2026-05-02 | cheat | Skipped pudding | replaces: Milk Chocolate (100 kcal)
2026-05-03 | weight | 82.5 | 4-5 Pints Yesterday
2026-05-03 | cheat | PB Toast, ~275 kcal | replaces: Single Shake (116 kcal)
2026-05-03 | workout | Cycling | 65 min | 735 kcal
2026-05-03 | cheat | Fancy Bacon Butty, ~550 kcal | replaces: Weekend Brunch (648 kcal)
2026-05-03 | cheat | Double Shake, ~232 kcal
2026-05-03 | cheat | Caesar Salad, ~555 kcal | replaces: Gousto Meal (640 kcal)
2026-05-04 | weight | 82.9 | Imodium used yesterday morning
2026-05-04 | cheat | Haddock Sandwich, ~530 kcal | replaces: Chicken Wrap (376 kcal)
2026-05-04 | drinks | 210 | Pint of beer
2026-05-04 | cheat | Skipped shake | replaces: Double Shake (232 kcal)
2026-05-04 | cheat | Cutlery works, ~1000 kcal | replaces: Gousto Meal (640 kcal)
2026-05-05 | weight | 83.5
2026-05-05 | workout | Walking | 13 min | 60 kcal
2026-05-05 | run | 20 min |  km | 184 kcal
2026-05-05 | workout | Walking | 13 min | 85 kcal
2026-05-05 | cheat | Leftover fried chicken, ~565 kcal | replaces: Chicken Wrap (376 kcal)
2026-05-06 | workout | Walking | 13 min | 59 kcal
2026-05-06 | weight | 83.0
2026-05-06 | workout | Walking | 11 min | 61 kcal
2026-05-06 | cheat | Extra gousto, ~130 kcal
2026-05-07 | weight | 82.8
2026-05-07 | workout | Walking | 13 min | 60 kcal
2026-05-07 | stair | 20 min | 191 kcal
2026-05-07 | workout | Walking | 13 min | 66 kcal
2026-05-07 | cheat | Gousto, ~620 kcal | replaces: Gousto Meal (640 kcal)
2026-05-08 | weight | 82.4
2026-05-08 | waist | 103
2026-05-08 | cheat | Chicken burger, ~400 kcal | replaces: Chicken Wrap (376 kcal)
2026-05-08 | drinks | 105 | Half Pint
2026-05-08 | workout | Walking | 89 min | 217 kcal
2026-05-08 | cheat | Chicken wrap, ~376 kcal | replaces: Gousto Meal (640 kcal)
2026-05-08 | cheat | Magnum, ~220 kcal | replaces: Milk Chocolate (100 kcal)
2026-05-08 | cheat | Spaghetti + mozarella, ~365 kcal
2026-05-09 | weight | 82.0
2026-05-09 | cheat | Breakfast, ~613 kcal | replaces: Weekend Brunch (648 kcal)
2026-05-09 | workout | Walking | 51 min | 161 kcal
2026-05-09 | cheat | Coffee, ~50 kcal
2026-05-09 | cheat | Skipped Shake | replaces: Single Shake (116 kcal)
2026-05-09 | drinks | 330 | Half bottle of wine
2026-05-09 | cheat | Lasagna, ~600 kcal | replaces: Gousto Meal (640 kcal)
2026-05-10 | weight | 81.5
2026-05-10 | workout | Cycling | 99 min | 1116 kcal
2026-05-10 | cheat | Porridge, ~185 kcal
2026-05-10 | cheat | Brunch, ~669 kcal | replaces: Weekend Brunch (648 kcal)
2026-05-10 | workout | Walking | 70 min | 306 kcal
2026-05-10 | cheat | Crisps, ~200 kcal
2026-05-10 | cheat | Lasagna, ~600 kcal | replaces: Gousto Meal (640 kcal)
2026-05-11 | weight | 81.7
2026-05-11 | cheat | Chicken fried rice, ~530 kcal | replaces: Chicken Wrap (376 kcal)
2026-05-11 | cheat | Enchilada’s, ~745 kcal | replaces: Gousto Meal (640 kcal)
2026-05-12 | workout | Walking | 12 min | 61 kcal
2026-05-12 | run | 19 min |  km | 200 kcal
2026-05-12 | workout | Walking | 28 min | 147 kcal
2026-05-12 | weight | 81.6
2026-05-12 | cheat | Chicken fried rice, ~530 kcal | replaces: Chicken Wrap (376 kcal)
2026-05-12 | cheat | Coffee & Tonic, ~25 kcal
2026-05-10 | drinks | 155 | Guinness
2026-05-12 | cheat | Caesar Salad, ~497 kcal | replaces: Gousto Meal (640 kcal)
2026-05-12 | cheat | Skipped chocolate | replaces: Milk Chocolate (100 kcal)
2026-05-13 | weight | 81.6
2026-05-13 | workout | Walking | 13 min | 60 kcal
2026-05-13 | workout | Walking | 12 min | 72 kcal
2026-05-13 | cheat | Caesar Salad, ~497 kcal | replaces: Chicken Wrap (376 kcal)
2026-05-13 | cheat | Single shake, ~105 kcal
2026-05-13 | cheat | Gousto, ~585 kcal | replaces: Gousto Meal (640 kcal)
2026-05-14 | weight | 80.9
2026-05-14 | workout | Walking | 13 min | 61 kcal
2026-05-14 | run | 20 min |  km | 198 kcal
2026-05-14 | workout | Walking | 14 min | 79 kcal
2026-05-14 | cheat | Chilli + 50g Fage, ~377 kcal | replaces: Chicken Wrap (376 kcal)
2026-05-14 | cheat | Sausage Roll, ~250 kcal
2026-05-14 | cheat | Extra Gousto Cals, ~45 kcal
2026-05-15 | weight | 81.3
2026-05-15 | waist | 102
2026-05-15 | cheat | Cafe ZaZa, ~750 kcal | replaces: Gousto Meal (640 kcal)
2026-05-15 | cheat | Protein Oats, ~236 kcal | replaces: Chicken Wrap (376 kcal)
2026-05-15 | cheat | Skipped desert | replaces: Milk Chocolate (100 kcal)
2026-05-16 | weight | 80.3
2026-05-15 | drinks | 190 | Pint of 4% Pale Ale
2026-05-16 | cheat | Clear shake, ~88 kcal | replaces: Single Shake (116 kcal)
2026-05-16 | cheat | Brunch, ~535 kcal | replaces: Weekend Brunch (648 kcal)
2026-05-16 | drinks | 59 | AF Beer
2026-05-16 | cheat | Meats & Cheeses, ~1138 kcal | replaces: Gousto Meal (640 kcal)
2026-05-16 | drinks | 330 | Half Bottle of Wine
2026-05-16 | cheat | Skipped desert | replaces: Milk Chocolate (100 kcal)
2026-05-17 | weight | 80.7
2026-05-17 | cheat | Banana, ~100 kcal | replaces: Single Shake (116 kcal)
2026-05-17 | workout | Cycling | 92 min | 1080 kcal
2026-05-17 | cheat | Orange Juice, ~72 kcal | replaces: Single Shake (116 kcal)
2026-05-17 | workout | Walking | 58 min | 275 kcal
2026-05-17 | cheat | Pizza + Tiramisu, ~1300 kcal | replaces: Gousto Meal (640 kcal)
2026-05-17 | cheat | Clear Shake, ~88 kcal | replaces: Milk Chocolate (100 kcal)
2026-05-18 | weight | 81.7
2026-05-18 | cheat | Salami, ~80 kcal
2026-05-18 | cheat | Gousto, ~525 kcal | replaces: Gousto Meal (640 kcal)
2026-05-19 | weight | 81.6
2026-05-19 | run | 20 min | 2.32 km | 201 kcal | 153 bpm
2026-05-19 | workout | Walking | 11 min | 55 kcal
2026-05-19 | run | 12 min |  km | 91 kcal
2026-05-19 | cheat | Gousto, ~600 kcal | replaces: Gousto Meal (640 kcal)
2026-05-20 | weight | 80.7
2026-05-20 | workout | Walking | 12 min | 59 kcal
2026-05-20 | workout | Walking | 12 min | 65 kcal
2026-05-20 | cheat | Wrap, extra chicken, ~425 kcal | replaces: Chicken Wrap (376 kcal)
2026-05-20 | cheat | Gousto, ~592 kcal | replaces: Gousto Meal (640 kcal)
2026-05-21 | weight | 80.7
2026-05-21 | workout | Walking | 13 min | 59 kcal
2026-05-21 | workout | Walking | 18 min | 90 kcal
2026-05-21 | cheat | Wrap, extra chicken, ~425 kcal | replaces: Chicken Wrap (376 kcal)
2026-05-21 | workout | Indoor Cycling | 43 min | 340 kcal
2026-05-21 | cheat | Zaap Thai, ~1200 kcal | replaces: Gousto Meal (640 kcal)
2026-05-21 | cheat | Skipped pudding | replaces: Milk Chocolate (100 kcal)
2026-05-22 | weight | 80.4
2026-05-22 | waist | 101
2026-05-22 | cheat | Wrap, extra chicken, ~450 kcal | replaces: Chicken Wrap (376 kcal)
2026-05-22 | cheat | Caesar Salad, ~497 kcal | replaces: Gousto Meal (640 kcal)
2026-05-23 | cheat | Banana, ~100 kcal | replaces: Single Shake (116 kcal)
2026-05-23 | weight | 80.2
2026-05-23 | workout | Walking | 14 min | 59 kcal
2026-05-23 | workout | Walking | 9 min | 40 kcal
2026-05-23 | cheat | Clear shake, ~70 kcal
2026-05-23 | cheat | Brunch, ~618 kcal | replaces: Weekend Brunch (648 kcal)
2026-05-23 | drinks | 158 | 330ml Hazy Jane
2026-05-23 | cheat | BBQ, ~856 kcal | replaces: Gousto Meal (640 kcal)
2026-05-23 | drinks | 56 | AF Beer
2026-05-24 | weight | 80.5
2026-05-24 | workout | Cycling | 106 min | 1110 kcal
2026-05-24 | cheat | Clear shake, ~88 kcal | replaces: Single Shake (116 kcal)
2026-05-24 | cheat | Brunch, ~600 kcal | replaces: Weekend Brunch (648 kcal)
2026-05-24 | drinks | 158 | 330ml Hazy Jane
2026-05-24 | cheat | Nespresso, ~30 kcal
2026-05-24 | cheat | Oyster fest, ~461 kcal | replaces: Gousto Meal (640 kcal)
2026-05-24 | drinks | 800 | Pint of 4% Pale Ale, Small fizz, Campari spritz, Damm lemon, Orange wine, Negroni
2026-05-25 | weight | 79.8
2026-05-25 | cheat | Double beef burger, ~650 kcal | replaces: Chicken Wrap (376 kcal)
2026-05-25 | cheat | BBQ, ~985 kcal | replaces: Gousto Meal (640 kcal)
2026-05-26 | weight | 79.8
2026-05-26 | workout | Walking | 12 min | 56 kcal
2026-05-26 | run | 20 min |  km | 195 kcal
2026-05-26 | workout | Walking | 11 min | 88 kcal
2026-05-26 | cheat | Barebell, ~190 kcal | replaces: Milk Chocolate (100 kcal)
2026-05-27 | weight | 79.9
2026-05-27 | workout | Walking | 13 min | 59 kcal
2026-05-27 | workout | Walking | 17 min | 73 kcal
2026-05-28 | weight | 79.8
2026-05-28 | workout | Walking | 13 min | 58 kcal
2026-05-28 | run | 20 min |  km | 194 kcal
2026-05-28 | workout | Walking | 13 min | 78 kcal
2026-05-28 | waist | 100
2026-05-28 | cheat | Gousto, ~590 kcal | replaces: Gousto Meal (640 kcal)
2026-05-29 | weight | 79.8
2026-05-29 | cheat | Salmon + Salad, ~875 kcal | replaces: Gousto Meal (640 kcal)
2026-05-30 | weight | 79.8
2026-05-30 | workout | Cycling | 114 min | 1155 kcal
2026-05-30 | cheat | Coffee, ~50 kcal
2026-05-30 | cheat | Brunch, ~608 kcal | replaces: Weekend Brunch (648 kcal)
2026-05-30 | drinks | 160 | Hugo spritz
2026-05-30 | drinks | 190 | Pint of 4% Pale Ale
2026-05-30 | drinks | 260 | Damm lemon x2
2026-05-30 | drinks | 120 | Gin &amp; Tonic
2026-05-30 | drinks | 282 | Shots x6
2026-05-30 | cheat | Skipped shake | replaces: Single Shake (116 kcal)
2026-05-30 | cheat | Ceaser salad, ~600 kcal | replaces: Gousto Meal (640 kcal)
2026-05-30 | cheat | Chicken, ~150 kcal | replaces: Milk Chocolate (100 kcal)
2026-05-31 | weight | 79.5
2026-05-31 | workout | Walking | 12 min | 56 kcal
2026-05-31 | workout | Walking | 13 min | 72 kcal
2026-05-31 | cheat | Brunch, ~571 kcal | replaces: Weekend Brunch (648 kcal)
2026-05-31 | cheat | Clear shake, ~88 kcal | replaces: Single Shake (116 kcal)
2026-05-31 | workout | Walking | 51 min | 212 kcal
2026-05-31 | cheat | Coffee, ~30 kcal
2026-05-31 | cheat | Caesar Salad + focaccia, ~742 kcal | replaces: Gousto Meal (640 kcal)
2026-05-31 | cheat | Digestive, ~80 kcal
2026-06-01 | weight | 79.5
2026-06-01 | workout | Walking | 40 min | 222 kcal
2026-06-01 | workout | Walking | 51 min | 251 kcal
2026-06-01 | cheat | Scotch Egg, ~350 kcal
2026-06-01 | cheat | Half scotch egg, ~175 kcal
2026-06-01 | cheat | Pastel de nata, ~150 kcal
2026-06-02 | weight | 79.5
2026-06-02 | workout | Walking | 13 min | 60 kcal
2026-06-02 | workout | Walking | 12 min | 83 kcal
2026-06-02 | run | 20 min | 2.33 km | 204 kcal | 154 bpm
2026-06-02 | cheat | Gousto, ~700 kcal | replaces: Gousto Meal (640 kcal)
2026-06-03 | weight | 79.4
3 Jun 2026 at 07:49
2 Jun 2026 at 08:58 | workout | Walking
Walking | 0 min | 0 kcal
2026-06-03 | workout | Walking | 13 min | 60 kcal
2026-06-03 | workout | Walking | 13 min | 63 kcal
2026-06-03 | cheat | Tea, ~40 kcal
2026-06-03 | cheat | Gousto, ~540 kcal | replaces: Gousto Meal (640 kcal)
2026-06-04 | weight | 79.0
