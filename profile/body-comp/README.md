# Body composition photos (local only)

Progress photos live **only on this machine**. Image and video files under this folder are **gitignored** — they are **not** pushed to GitHub.

**Agents:** read **`AGENTS.md`** in this folder, then the **`README.md` inside each `progress/` subfolder** you care about.

---

## Progress catalogue (canonical sets)

| Folder | Waist (self) | Notes |
|--------|--------------|--------|
| **`progress/2026-04-15_baseline-108cm-phase1/`** | **~108 cm** | Baseline at Phase 1 start — five poses matching **`01`–`05`** naming — see folder **`README.md`** |
| **`progress/2026-04-29_waist-105cm-phase1/`** | **105 cm** | ~week 3–4 — five poses — see folder **`README.md`** |
|| **`progress/2026-05-13_week4-103cm-phase1/`** | **103 cm** | Day 30 of Phase 1, 81.6 kg, ~25.1% BF — five poses (01–03 directly comparable to baseline; 04–05 new rear angles) — see folder **`README.md`** |
|| **`progress/2026-05-20_week6-102cm-phase1/`** | **102 cm** | Day 37 of Phase 1, 80.7 kg / 81.0 kg 7d avg, ~24% BF — five poses all directly comparable to prior sets — see folder **`README.md`** |
|| **`progress/2026-05-28_week7-100cm-phase1/`** | **100 cm** | Day 45 of Phase 1, 79.8 kg / 80.1 kg 7d avg, ~23.5% BF — phase-end waist target hit 9 days early — five poses all directly comparable — see folder **`README.md`** |
|| **`progress/2026-06-04_phase1-end-99cm/`** | **99 cm** | Day 52 of Phase 1 (phase end), 79.0 kg / 79.5 kg 7d avg, ~23.0% BF — Phase 1 final set; −9 cm waist from baseline — five poses all directly comparable — see folder **`README.md`** |
|| **`progress/2026-07-06_phase2-start-100cm/`** | **100 cm** | Phase 2 start (Bali cut Day 1), 80.4 kg / 80.2 kg 7d avg, ~27.4% BF — fully refed post-maintenance; +1 cm vs Phase 1 end = glycogen/water only — five poses all directly comparable — see folder **`README.md`** |
|| **`progress/2026-07-22_phase2-week3-77kg/`** | **99 cm** | Phase 2 day 16, 77.9 kg / 78.2 kg 7d avg, ~26.7% BF — −1 cm waist in 16 days (refed→refed); same waist as Phase 1 end but 1.1 kg lighter = real fat loss confirmed — five poses all directly comparable — see folder **`README.md`** |

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
5. Optionally run **`python3 profile/body-comp/progress/verify-exif-dates.py`** to confirm EXIF dates match folder names.
