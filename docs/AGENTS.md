# Agent notes — docs/

This folder contains the PWA (Progressive Web App) and supporting documentation.

## Key files for agents

| File | Read when |
|------|-----------|
| **`app-state.md`** | **Always read before modifying any PWA file.** Contains current feature state, dev setup, diagnostic checklist, and changelog. |
| `index.html` | The entire PWA — HTML, CSS, and JS all inline. Single file. |
| `sw.js` | Service worker. Bump `CACHE_VERSION` when deploying changes that need old caches cleared on production. |
| `health-conversation-snapshot.md` | Durable health planning context. Not related to the app code. |
| `shortcut-setup.md` | iOS Shortcut setup for auto-logging workouts. |
| `force-update.html` | Utility page — navigating to it clears all SW caches and redirects to the app. Only needed on production when the SW is stuck. |

## Before touching the PWA

1. Read `app-state.md` — specifically the **dev setup** and **diagnostic order** sections.
2. Verify the local server is running and responding before blaming caches.
3. After changes, commit and push — GitHub Pages deploys within ~2 minutes.
