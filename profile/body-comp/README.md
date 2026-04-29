# Body composition photos (local only)

Progress photos live **only on this machine**. Image and video files under this folder are **gitignored** — they are **not** pushed to GitHub.

**Agents:** read **`AGENTS.md`** in this folder, then the **`README.md` inside each `progress/` subfolder** you care about.

---

## Progress catalogue (canonical sets)

| Folder | Waist (self) | Notes |
|--------|--------------|--------|
| **`progress/2026-04-15_baseline-108cm-phase1/`** | **~108 cm** | Baseline at Phase 1 start — five poses matching **`01`–`05`** naming — see folder **`README.md`** |
| **`progress/2026-04-29_waist-105cm-phase1/`** | **105 cm** | ~week 3–4 — five poses — see folder **`README.md`** |

Older loose imports (screenshots mixed with unrelated snaps) remain under **`2026-04-12/`**, **`2026-04-13/`**, **`2026-04-15/`** — **not** a clean progress set; prefer **`progress/`** dated folders for comparisons.

---

## Layout

```
profile/body-comp/
  AGENTS.md              ← instructions for AI assistants (tracked)
  README.md              ← this file (tracked)
  progress/
    verify-exif-dates.py ← optional: confirm EXIF dates match folder names (tracked)
    <date>_<label>/
      README.md          ← metrics + pose map for that shoot (tracked)
      01-….png           ← images gitignored
      …
```

---

## Security notes

- Folder permissions should be **`chmod 700`** on `body-comp/` and `progress/` (owner only).
- Keep **FileVault** (disk encryption) enabled on macOS.
- Do **not** copy images into **`docs/`** or any path that gets published (e.g. GitHub Pages).

## Adding new progress sets

1. Create **`progress/YYYY-MM-DD_short-label/`**.
2. Add **`01-front-….png`**, **`02-side-….png`**, … with consistent numbering.
3. Write **`README.md`** in that folder (metrics + pose table + original filenames).
4. Append one row to the **Progress catalogue** table above.
