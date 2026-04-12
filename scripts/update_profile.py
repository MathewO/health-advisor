#!/usr/bin/env python3
"""
update_profile.py — Interactive profile onboarding and update tool.

Usage:
  python scripts/update_profile.py --onboard     # Full first-time setup
  python scripts/update_profile.py --update       # Update individual fields
"""

import json
import argparse
from datetime import date
from pathlib import Path

PROFILE_JSON = Path(__file__).parent.parent / "profile" / "profile.json"
PROFILE_MD = Path(__file__).parent.parent / "profile" / "profile.md"


def ask(prompt, current=None, optional=False):
    suffix = f" [{current}]" if current else (" (optional, press Enter to skip)" if optional else "")
    val = input(f"{prompt}{suffix}: ").strip()
    if not val and current:
        return current
    if not val and optional:
        return None
    return val or None


def ask_list(prompt, current=None):
    print(f"{prompt}")
    if current:
        print(f"  Current: {', '.join(current)}")
    print("  Enter items one per line. Empty line to finish.")
    items = []
    while True:
        item = input("  > ").strip()
        if not item:
            break
        items.append(item)
    return items if items else current or []


def onboard(profile):
    print("\n=== Health Profile Onboarding ===\n")
    print("Answer each question. Press Enter to keep the current value.\n")

    p = profile["personal"]
    p["name"] = ask("Your first name", p.get("name"))
    p["age"] = int(ask("Age", p.get("age")))
    p["sex"] = ask("Sex (male/female/other)", p.get("sex"))
    height = ask("Height (cm)", p.get("height_cm"))
    p["height_cm"] = float(height) if height else None
    weight = ask("Weight (kg)", p.get("weight_kg"))
    p["weight_kg"] = float(weight) if weight else None
    p["location"] = ask("Location (city/country)", p.get("location"), optional=True)

    print()
    profile["health_goals"] = ask_list("What are your main health goals?", profile.get("health_goals"))

    print()
    profile["current_conditions"] = ask_list(
        "Any current health conditions or diagnoses? (or press Enter to skip)",
        profile.get("current_conditions")
    )

    print()
    profile["medications"] = ask_list(
        "Any prescription medications? (or press Enter to skip)",
        profile.get("medications")
    )

    print()
    profile["diet_style"] = ask(
        "How would you describe your diet? (e.g. omnivore, low-carb, Mediterranean, vegetarian)",
        profile.get("diet_style")
    )
    profile["alcohol"] = ask(
        "Alcohol consumption (e.g. none, occasional, 1-2 drinks/week, daily)",
        profile.get("alcohol")
    )
    profile["activity_level"] = ask(
        "Activity level (sedentary / lightly active / moderately active / very active)",
        profile.get("activity_level")
    )
    profile["exercise_types"] = ask_list(
        "What types of exercise do you do regularly?",
        profile.get("exercise_types")
    )

    print()
    sleep_hours = ask("Average sleep hours per night", profile.get("avg_sleep_hours"))
    profile["avg_sleep_hours"] = float(sleep_hours) if sleep_hours else None
    profile["sleep_quality"] = ask(
        "How would you rate your sleep quality? (poor / fair / good / excellent)",
        profile.get("sleep_quality")
    )
    profile["stress_level"] = ask(
        "Typical stress level (low / moderate / high / very high)",
        profile.get("stress_level")
    )
    profile["work_schedule"] = ask(
        "Work schedule (e.g. 9-5 office, remote flexible, shift work, irregular)",
        profile.get("work_schedule"),
        optional=True
    )

    print()
    last_panel = ask(
        "Date of last blood panel? (YYYY-MM or leave blank)",
        profile.get("last_blood_panel_date"),
        optional=True
    )
    profile["last_blood_panel_date"] = last_panel

    profile["updated"] = date.today().isoformat()
    return profile


def write_profile_json(profile):
    with open(PROFILE_JSON, "w") as f:
        json.dump(profile, f, indent=2)
    print(f"\nSaved to {PROFILE_JSON}")


def write_profile_md(profile):
    p = profile["personal"]
    goals = "\n".join(f"- {g}" for g in profile.get("health_goals", [])) or "_(none listed)_"
    conditions = "\n".join(f"- {c}" for c in profile.get("current_conditions", [])) or "_(none listed)_"
    medications = "\n".join(f"- {m}" for m in profile.get("medications", [])) or "_(none listed)_"
    exercises = ", ".join(profile.get("exercise_types", [])) or "_(not set)_"
    focus = "\n".join(f"- {f.capitalize()}" for f in profile.get("focus_areas", []))

    def val(v):
        return str(v) if v else "_(not set)_"

    md = f"""# My Health Profile

> This file is the single source of truth about me. Claude reads this at the start of every session.
> Last updated: {profile.get('updated', 'unknown')}

---

## Personal

| Field | Value |
|---|---|
| Name | {val(p.get('name'))} |
| Age | {val(p.get('age'))} |
| Sex | {val(p.get('sex'))} |
| Height | {val(p.get('height_cm')) + ' cm' if p.get('height_cm') else '_(not set)_'} |
| Weight | {val(p.get('weight_kg')) + ' kg' if p.get('weight_kg') else '_(not set)_'} |
| Location | {val(p.get('location'))} |

---

## Health Goals

{goals}

---

## Focus Areas

{focus}

---

## Current Conditions & Medical Notes

{conditions}

---

## Medications

{medications}

---

## Diet & Lifestyle

| Area | Detail |
|---|---|
| Diet style | {val(profile.get('diet_style'))} |
| Alcohol | {val(profile.get('alcohol'))} |
| Smoking | {val(profile.get('smoking', 'No'))} |
| Activity level | {val(profile.get('activity_level'))} |
| Exercise types | {exercises} |
| Avg sleep | {val(profile.get('avg_sleep_hours')) + ' hours' if profile.get('avg_sleep_hours') else '_(not set)_'} |
| Sleep quality | {val(profile.get('sleep_quality'))} |
| Stress level | {val(profile.get('stress_level'))} |
| Work schedule | {val(profile.get('work_schedule'))} |

---

## Blood Work & Biomarkers

| Marker | Value | Date | Notes |
|---|---|---|---|
"""

    markers = profile.get("notable_blood_markers", {})
    if markers:
        for marker, info in markers.items():
            md += f"| {marker} | {info.get('value', '')} | {info.get('date', '')} | {info.get('notes', '')} |\n"
    else:
        md += "| _(none yet — ask Claude to help you log blood work)_ | | | |\n"

    md += f"""
---

## Apple Health Summary

> Auto-generated by `scripts/parse_apple_health.py`. See `profile/health-metrics.md` for full detail.

_(See health-metrics.md)_

---

## Notes

_(Any additional context Claude should know about me)_
"""

    with open(PROFILE_MD, "w") as f:
        f.write(md)
    print(f"Updated {PROFILE_MD}")


def main():
    parser = argparse.ArgumentParser(description="Update your health profile")
    parser.add_argument("--onboard", action="store_true", help="Run full onboarding questionnaire")
    parser.add_argument("--update", action="store_true", help="Update individual fields")
    args = parser.parse_args()

    with open(PROFILE_JSON) as f:
        profile = json.load(f)

    if args.onboard or not args.update:
        profile = onboard(profile)
        write_profile_json(profile)
        write_profile_md(profile)
        print("\nProfile complete. Open health-advisor in Cursor to start your first session.")
    else:
        print("Use --onboard to run the full questionnaire.")


if __name__ == "__main__":
    main()
