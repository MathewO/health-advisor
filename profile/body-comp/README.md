# Body composition photos (local only)

Progress photos live **only on this machine**. Image and video files under this folder are **gitignored** — they are **not** pushed to GitHub.

## Layout

- **`2026-04-12/`** — phone captures imported from Cursor assets (Apr 12 batch).
- **`2026-04-13/`** — phone captures imported from Cursor assets (Apr 13 batch).
- **`2026-04-15/`** — phone captures imported from Cursor assets (Apr 15 batch).

Filenames keep the original `IMG_*.png` stems so you can match back to Photos.app if needed.

## Security notes

- Folder permissions should be **`chmod 700`** (owner read/write/execute only).
- Keep **FileVault** (disk encryption) enabled on macOS.
- Do **not** copy these into `docs/` or any path that gets published (e.g. GitHub Pages).

## Adding new rounds

Drop new photos here (dated subfolders optional). Prefer **PNG/JPEG** — those extensions stay ignored by git.
