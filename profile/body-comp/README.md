# Body composition photos (local only)

Progress photos live **only on this machine**. Image and video files under this folder are **gitignored** — they are **not** pushed to GitHub.

**Agents:** read **`AGENTS.md`** in this folder, then the **`README.md` inside each `rounds/` subfolder** you care about.

---

## Rounds index (canonical progress sets)

| Round folder | Waist (self) | Notes |
|--------------|--------------|--------|
| **`rounds/2026-04-29_waist-105cm-phase1/`** | **105 cm** | Five poses: front + sides + arms raised — see round `README.md` |

Older loose imports (screenshots mixed with unrelated snaps) remain under **`2026-04-12/`**, **`2026-04-13/`**, **`2026-04-15/`** — **not** a clean progress set; prefer **`rounds/`** for comparisons.

---

## Layout

```
profile/body-comp/
  AGENTS.md              ← instructions for AI assistants (tracked)
  README.md              ← this file (tracked)
  rounds/
    <date>_<label>/
      README.md          ← metrics + pose map for that shoot (tracked)
      01-….png           ← images gitignored
      …
```

---

## Security notes

- Folder permissions should be **`chmod 700`** on `body-comp/` and `rounds/` (owner only).
- Keep **FileVault** (disk encryption) enabled on macOS.
- Do **not** copy images into **`docs/`** or any path that gets published (e.g. GitHub Pages).

## Adding new rounds

1. Create **`rounds/YYYY-MM-DD_short-label/`**.
2. Add **`01-front-….png`**, **`02-side-….png`**, … with consistent numbering.
3. Write **`README.md`** in that folder (metrics + pose table + original filenames).
4. Append one row to the **Rounds index** table above.
