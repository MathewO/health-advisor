# Agent notes — body composition photos

## Where progress photos live

- **`profile/body-comp/progress/<DATE>_<label>/`** — each dated set is one folder with:
  - **`README.md`** — metrics, pose legend, original filename map (always read this first).
  - **`01-*.png` … `05-*.png`** — canonical filenames (images are gitignored).

## Parent index

See **`profile/body-comp/README.md`** for security rules and the **progress catalogue** table.

## Rules

1. **Never `git add` PNG/JPEG/HEIC** under `profile/body-comp/` — `.gitignore` blocks them from pushes.
2. **`README.md` files** under `body-comp/` may be tracked — safe for instructions only.
3. Compare sets using **matching poses** — arms-raised shots are not directly comparable to relaxed sides.
