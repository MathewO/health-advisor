# Agent notes — body composition photos

## Where progress photos live

- **`profile/body-comp/progress/<DATE>_<label>/`** — each dated set is one folder with:
  - **`README.md`** — metrics, pose legend, original filename map (always read this first).
  - **`01-*.png` … `05-*.png`** — canonical filenames (images are gitignored).

## Parent index

See **`profile/body-comp/README.md`** for security rules and the **progress catalogue** table.

## Canonical pose schema — use for every new set

All progress sets must use these exact filenames and poses, in this order. Do not invent new names.

| File | Pose | Notes |
|------|------|-------|
| `01-front-relaxed.png` | Front, arms at sides | |
| `02-side-left-dragon-tattoo.png` | Subject's **left** side profile — dragon tattoo arm visible | Wood door background |
| `03-side-right-mushroom-tattoo.png` | Subject's **right** side profile — mushroom tattoo visible | "YOU ARE ENOUGH" poster + dog |
| `04-side-relaxed-you-are-enough.png` | Side, relaxed upright — "YOU ARE ENOUGH" poster visible | Same room as 03 |
| `05-side-arms-raised-forward.png` | Side profile, **arms raised forward** (abdominal stretch) | Not comparable to relaxed sides for waist line |

When creating a new set: copy this table into the folder's `README.md`, fill in the metrics, and map each original filename to the canonical name above.

## Rules

1. **Never `git add` PNG/JPEG/HEIC** under `profile/body-comp/` — `.gitignore` blocks them from pushes.
2. **`README.md` files** under `body-comp/` may be tracked — safe for instructions only.
3. Compare sets using **matching poses** — arms-raised shots (`05`) are not directly comparable to relaxed sides.
4. **Always use the canonical filenames above** — do not create new names or reorder slots.
