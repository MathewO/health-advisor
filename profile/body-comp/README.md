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
  AGENTS.md                     ← instructions for AI assistants (tracked)
  README.md                     ← this file (tracked)
  progress/
    verify-exif-dates.py        ← optional: confirm EXIF dates match folder names (tracked)
    generate-review-images.py   ← build fast-preview JPEGs under review/ (tracked)
    <date>_<label>/              ← full-resolution / export copies (source of truth)
      README.md                 ← metrics + pose map for that shoot (tracked)
      01-….png                  ← images gitignored
      …
    review/                     ← mirrors each dated folder; same stems, **.jpg** previews (gitignored)
      <date>_<label>/
        01-….jpg
        …
```

**Full-res vs review:** Keep canonical **`01`–`05`** files only under each **`YYYY-MM-DD_*`** folder. **`progress/review/`** duplicates the **folder names** and **file stems** but stores **JPEG**, long edge **~1600 px** — faster to flip through in Cursor. Regenerate review copies whenever full-res files change (see **Adding new progress sets**).

---

## Security notes

- Folder permissions should be **`chmod 700`** on `body-comp/` and `progress/` (owner only).
- Keep **FileVault** (disk encryption) enabled on macOS.
- Do **not** copy images into **`docs/`** or any path that gets published (e.g. GitHub Pages).

## Adding new progress sets

1. Create **`progress/YYYY-MM-DD_short-label/`**.
2. Add **`01-front-….png`**, **`02-side-….png`**, … with consistent numbering (full-resolution / Photos exports live here only).
3. Write **`README.md`** in that folder (metrics + pose table + original filenames).
4. Append one row to the **Progress catalogue** table above.
5. Run **`python3 profile/body-comp/progress/generate-review-images.py`** so **`progress/review/<same-folder>/`** gets matching **`01`–`05`.jpg** previews (same stems as step 2). Re-run after any full-res add/replace.
6. Optionally run **`python3 profile/body-comp/progress/verify-exif-dates.py`** to confirm EXIF dates match folder names.
