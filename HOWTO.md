# How to Use Your Health Advisor

This project is a personal health and longevity knowledge base that runs inside Cursor.
Claude reads your full profile at the start of every session — so it always knows who you are, what you're working on, and what you've already tried.

---

## First-Time Setup

### 1. Open this project in Cursor

- In Cursor: **File → Open Folder** → select the `health-advisor` folder
- It will appear in your Recent Projects list from now on

### 2. Fill in your profile

Open a terminal in Cursor and run:

```bash
python scripts/update_profile.py --onboard
```

This walks you through a short questionnaire and writes your profile to:
- `profile/profile.md` (Claude reads this)
- `profile/profile.json` (scripts read/write this)

### 3. Log your supplements

Open `supplements/supplements.md` and add what you're currently taking, or ask Claude in a new chat:

> "Help me log my current supplements"

### 4. Import Apple Health data (optional but recommended)

1. On your iPhone: open **Health app → profile photo → Export All Health Data**
2. AirDrop the `export.zip` to your Mac
3. Place it in `health-advisor/data/`
4. Run:

```bash
python scripts/parse_apple_health.py
```

This generates `profile/health-metrics.md` with your sleep, HRV, steps, and other trends.

---

## Day-to-Day Usage

### Starting a session

Just open a new chat in Cursor (⌘L or the chat panel). Claude already has your full context.

### Example things to ask

**Research:**
> "What does the current evidence say about time-restricted eating for metabolic health? How relevant is it to my profile?"

> "Summarise the research on Zone 2 cardio and longevity biomarkers."

> "Is there good evidence for my current magnesium dose? What does the research say about timing?"

**Recommendations:**
> "Based on my sleep data and HRV trend, what's the single highest-leverage change I could make?"

> "Suggest my next experiment. Keep it simple and evidence-based."

**Logging:**
> "Log that as a 4-week experiment — hypothesis, change, and success metric."

> "Add berberine 500mg before meals to my supplement log and give me your evidence rating for it."

> "Update my weight to 82kg."

**Checking in:**
> "It's been 3 weeks on the magnesium experiment — here's what I've noticed. Help me assess it."

> "Review my active experiments and tell me what to watch for this week."

---

## File Structure Reference

```
health-advisor/
├── profile/
│   ├── profile.md          ← Claude reads this every session
│   ├── profile.json        ← Structured data for scripts
│   └── health-metrics.md  ← Apple Health summary (auto-generated)
├── supplements/
│   └── supplements.md      ← Your current stack + evidence ratings
├── research/
│   ├── _template.md        ← Template for saving study notes
│   ├── sleep/              ← Research Claude saves on sleep topics
│   ├── metabolic/          ← Research on metabolic health
│   ├── nutrition/          ← Research on diet/nutrition
│   └── supplements/        ← Research on specific supplements
├── experiments/
│   └── experiments.md      ← Running log of everything you've tried
├── scripts/
│   ├── update_profile.py   ← Update your profile via questionnaire
│   ├── parse_apple_health.py ← Parse Apple Health XML export
│   └── log_experiment.py   ← CLI helper to add experiments
└── HOWTO.md                ← This file
```

---

## Keeping It Up to Date

The knowledge base is only as good as what's in it. Try to:

- **Update your profile** whenever something significant changes (weight, new condition, changed diet)
- **Re-import Apple Health** every month or so to keep metrics current
- **Log experiments** as you start them — don't wait
- **Check in weekly** on active experiments, even briefly
- **Let Claude save research** — when it finds something useful, say "save that to the research library"

---

## Privacy Note

Everything lives locally on your Mac. Nothing is sent anywhere except to Claude via Cursor (the same as any other Cursor conversation). Your profile files are just text — you can read, edit, or delete them any time.
