#!/usr/bin/env python3
"""
parse_apple_health.py — Parse an Apple Health export and write a summary to health-metrics.md.

How to export from iPhone:
  1. Open the Health app
  2. Tap your profile photo (top right)
  3. Scroll down -> Export All Health Data
  4. AirDrop or share the export.zip to your Mac
  5. Place export.zip in the health-advisor/data/ folder
  6. Run: python scripts/parse_apple_health.py

The script extracts key metrics and updates profile/health-metrics.md.
"""

import xml.etree.ElementTree as ET
import zipfile
import re
import statistics
from datetime import datetime, date, timedelta
from pathlib import Path
from collections import defaultdict

DATA_DIR    = Path(__file__).parent.parent / "data"
METRICS_MD  = Path(__file__).parent.parent / "profile" / "health-metrics.md"

RECORD_TYPES = {
    "HKQuantityTypeIdentifierHeartRateVariabilitySDNN": "hrv",
    "HKQuantityTypeIdentifierRestingHeartRate":         "resting_hr",
    "HKQuantityTypeIdentifierStepCount":                "steps",
    "HKQuantityTypeIdentifierActiveEnergyBurned":       "active_calories",
    "HKQuantityTypeIdentifierAppleExerciseTime":        "exercise_minutes",
    "HKQuantityTypeIdentifierAppleStandHour":           "stand_hours",
    "HKQuantityTypeIdentifierBodyMass":                 "weight",
    "HKQuantityTypeIdentifierVO2Max":                   "vo2max",
}

# These metrics are recorded by multiple sources; restrict to Apple Watch only.
WATCH_ONLY_KEYS = {"steps", "active_calories"}

WORKOUT_TYPES = {
    "HKWorkoutActivityTypeRunning":                      "Run",
    "HKWorkoutActivityTypeStairClimbing":                "Stair Climbing",
    "HKWorkoutActivityTypeWalking":                      "Walk",
    "HKWorkoutActivityTypeCycling":                      "Cycling",
    "HKWorkoutActivityTypeHighIntensityIntervalTraining": "HIIT",
    "HKWorkoutActivityTypeFunctionalStrengthTraining":   "Strength",
}


def normalise_date(raw):
    return re.sub(r" ([+-]\d{2})(\d{2})$", r" \1:\2", raw)


def get_workout_stats(workout_el):
    """Extract active calories, avg HR, and distance from WorkoutStatistics children.
    watchOS 10+ stores these as child elements rather than top-level attributes."""
    stats = {}
    for child in workout_el:
        if child.tag != "WorkoutStatistics":
            continue
        t = child.get("type", "")
        if "ActiveEnergyBurned" in t:
            val = child.get("sum")
            if val:
                stats["kcal"] = round(float(val))
        elif "HeartRate" in t:
            val = child.get("average")
            if val:
                stats["hr_avg"] = round(float(val))
        elif "DistanceWalkingRunning" in t or "DistanceCycling" in t:
            val = child.get("sum")
            if val:
                stats["km"] = round(float(val), 2)
    return stats


def find_export():
    zip_path = DATA_DIR / "export.zip"
    xml_path = DATA_DIR / "export.xml"

    if zip_path.exists():
        print(f"Found {zip_path}, extracting...")
        with zipfile.ZipFile(zip_path, "r") as z:
            for name in z.namelist():
                if name.endswith("export.xml"):
                    z.extract(name, DATA_DIR)
                    extracted = DATA_DIR / name
                    extracted.rename(xml_path)
                    print(f"Extracted to {xml_path}")
                    break
    elif xml_path.exists():
        print(f"Using existing {xml_path}")
    else:
        print(f"ERROR: No export found. Place export.zip in {DATA_DIR}/")
        return None
    return xml_path


def parse_records(xml_path):
    print("Parsing health records (this may take a minute for large exports)...")
    tree = ET.parse(xml_path)
    root = tree.getroot()

    data = defaultdict(list)
    cutoff_30 = date.today() - timedelta(days=30)
    cutoff_90 = date.today() - timedelta(days=90)

    for record in root.iter("Record"):
        rtype = record.get("type", "")
        key = RECORD_TYPES.get(rtype)
        if not key:
            continue

        if key in WATCH_ONLY_KEYS and "Watch" not in record.get("sourceName", ""):
            continue

        try:
            val = float(record.get("value", 0))
            dt  = datetime.fromisoformat(normalise_date(record.get("startDate", ""))).date()
        except (ValueError, TypeError):
            continue

        data[key].append((dt, val))

    # Sleep (CategorySamples, not Records)
    sleep_data = []
    for sample in root.iter("Record"):
        if sample.get("type") != "HKCategoryTypeIdentifierSleepAnalysis":
            continue
        if "Asleep" not in sample.get("value", ""):
            continue
        try:
            start = datetime.fromisoformat(normalise_date(sample.get("startDate", "")))
            end   = datetime.fromisoformat(normalise_date(sample.get("endDate",   "")))
            hours = (end - start).total_seconds() / 3600
            if 0.05 < hours < 14:
                sleep_data.append((end.date(), hours))
        except (ValueError, TypeError):
            continue

    # Workouts (last 90 days, known types only)
    workouts = []
    for w in root.findall("Workout"):
        wtype = w.get("workoutActivityType", "")
        label = WORKOUT_TYPES.get(wtype)
        if not label:
            continue
        try:
            dt = datetime.fromisoformat(normalise_date(w.get("startDate", ""))).date()
        except (ValueError, TypeError):
            continue
        if dt < cutoff_90:
            continue
        duration = round(float(w.get("duration", 0)), 1)
        stats = get_workout_stats(w)
        workouts.append({
            "date":         dt,
            "type":         label,
            "duration_min": duration,
            "kcal":         stats.get("kcal"),
            "hr_avg":       stats.get("hr_avg"),
            "km":           stats.get("km"),
        })
    workouts.sort(key=lambda x: x["date"], reverse=True)

    return data, sleep_data, cutoff_30, cutoff_90, workouts


def avg(values):
    return round(statistics.mean(values), 1) if values else None


def trend(recent, older):
    if not recent or not older:
        return "Stable"
    diff = avg(recent) - avg(older)
    if abs(diff) < 1:
        return "Stable"
    return f"{'up' if diff > 0 else 'down'} {abs(round(diff, 1))}"


def summarise(data, sleep_data, cutoff_30, cutoff_90):
    def split(key):
        all_vals = data.get(key, [])
        r30 = [v for d, v in all_vals if d >= cutoff_30]
        r90 = [v for d, v in all_vals if cutoff_90 <= d < cutoff_30]
        return r30, r90

    def split_sleep():
        by_day = defaultdict(float)
        for d, v in sleep_data:
            by_day[d] += v
        tracked = {d: v for d, v in by_day.items() if v >= 3.0}
        r30 = [v for d, v in tracked.items() if d >= cutoff_30]
        r90 = [v for d, v in tracked.items() if cutoff_90 <= d < cutoff_30]
        return r30, r90

    def daily_sum(key):
        by_day = defaultdict(float)
        for d, v in data.get(key, []):
            by_day[d] += v
        r30 = [v for d, v in by_day.items() if d >= cutoff_30]
        r90 = [v for d, v in by_day.items() if cutoff_90 <= d < cutoff_30]
        return r30, r90

    sleep30, sleep90 = split_sleep()
    hrv30,   hrv90   = split("hrv")
    rhr30,   rhr90   = split("resting_hr")
    steps30, steps90 = daily_sum("steps")
    cal30,   cal90   = daily_sum("active_calories")
    ex30,    ex90    = daily_sum("exercise_minutes")

    weight_vals   = sorted(data.get("weight", []), key=lambda x: x[0])
    latest_weight = weight_vals[-1][1]  if weight_vals else None
    prev_weight   = weight_vals[-30][1] if len(weight_vals) >= 30 else (weight_vals[0][1] if weight_vals else None)

    vo2_vals   = sorted(data.get("vo2max", []), key=lambda x: x[0])
    latest_vo2 = vo2_vals[-1][1] if vo2_vals else None

    if latest_weight and prev_weight:
        wt = "up" if latest_weight > prev_weight else ("down" if latest_weight < prev_weight else "Stable")
    else:
        wt = "Stable"

    return {
        "sleep":    {"avg30": avg(sleep30), "avg90": avg(sleep90), "trend": trend(sleep30, sleep90)},
        "hrv":      {"avg30": avg(hrv30),   "avg90": avg(hrv90),   "trend": trend(hrv30, hrv90)},
        "rhr":      {"avg30": avg(rhr30),   "avg90": avg(rhr90),   "trend": trend(rhr30, rhr90)},
        "steps":    {"avg30": avg(steps30), "avg90": avg(steps90), "trend": trend(steps30, steps90)},
        "calories": {"avg30": avg(cal30),   "avg90": avg(cal90),   "trend": trend(cal30, cal90)},
        "exercise": {"avg30": avg(ex30),    "avg90": avg(ex90),    "trend": trend(ex30, ex90)},
        "weight":   {"latest": latest_weight, "trend": wt},
        "vo2":      {"latest": latest_vo2},
    }


def fmt(val, unit=""):
    return f"{val}{unit}" if val is not None else "—"


def write_metrics_md(s, workouts=None):
    today_str = date.today().isoformat()

    lines = [
        "# Health Metrics",
        "",
        "> Auto-generated from Apple Health export. Do not edit manually.",
        "> To update: export from iPhone Health app, place `export.zip` in `data/`, run `python scripts/parse_apple_health.py`",
        "",
        "---",
        "",
        "## Last Updated",
        "",
        today_str,
        "",
        "---",
        "",
        "## Sleep",
        "",
        "| Metric | 30-day avg | 90-day avg | Trend |",
        "|---|---|---|---|",
        f"| Total sleep | {fmt(s['sleep']['avg30'], ' hrs')} | {fmt(s['sleep']['avg90'], ' hrs')} | {s['sleep']['trend']} |",
        "",
        "---",
        "",
        "## Heart Rate & HRV",
        "",
        "| Metric | 30-day avg | 90-day avg | Trend |",
        "|---|---|---|---|",
        f"| Resting heart rate | {fmt(s['rhr']['avg30'], ' bpm')} | {fmt(s['rhr']['avg90'], ' bpm')} | {s['rhr']['trend']} |",
        f"| HRV (SDNN) | {fmt(s['hrv']['avg30'], ' ms')} | {fmt(s['hrv']['avg90'], ' ms')} | {s['hrv']['trend']} |",
        "",
        "---",
        "",
        "## Activity",
        "",
        "| Metric | 30-day avg | 90-day avg | Trend |",
        "|---|---|---|---|",
        f"| Steps | {fmt(s['steps']['avg30'])} | {fmt(s['steps']['avg90'])} | {s['steps']['trend']} |",
        f"| Active calories | {fmt(s['calories']['avg30'], ' kcal')} | {fmt(s['calories']['avg90'], ' kcal')} | {s['calories']['trend']} |",
        f"| Exercise minutes | {fmt(s['exercise']['avg30'], ' min')} | {fmt(s['exercise']['avg90'], ' min')} | {s['exercise']['trend']} |",
        "",
        "---",
        "",
        "## Body",
        "",
        "| Metric | Latest | Source |",
        "|---|---|---|",
        "| Weight | See `profile/weight-log.md` | Self-reported morning weight — not pulled from Apple Health |",
        "",
        "---",
        "",
        "## VO2 Max",
        "",
        "| Metric | Latest |",
        "|---|---|",
        f"| VO2 Max (estimated) | {fmt(s['vo2']['latest'], ' mL/kg/min')} |",
        "",
        "---",
        "",
        "## Recent Workouts (90 days)",
        "",
    ]

    if workouts:
        lines.append("| Date | Type | Duration | Distance | Calories | Avg HR |")
        lines.append("|---|---|---|---|---|---|")
        for w in workouts[:30]:
            km_str   = f"{w['km']} km"      if w.get("km")     else "—"
            kcal_str = f"{w['kcal']} kcal"  if w.get("kcal")   else "—"
            hr_str   = f"{w['hr_avg']} bpm" if w.get("hr_avg") else "—"
            lines.append(f"| {w['date']} | {w['type']} | {w['duration_min']} min | {km_str} | {kcal_str} | {hr_str} |")
    else:
        lines.append("_No tracked workouts found in the last 90 days._")

    lines.append("")

    with open(METRICS_MD, "w") as f:
        f.write("\n".join(lines))
    print(f"\nWritten to {METRICS_MD}")


def main():
    DATA_DIR.mkdir(exist_ok=True)
    xml_path = find_export()
    if not xml_path:
        return

    data, sleep_data, cutoff_30, cutoff_90, workouts = parse_records(xml_path)
    summary = summarise(data, sleep_data, cutoff_30, cutoff_90)
    write_metrics_md(summary, workouts)

    print("\nKey metrics:")
    print(f"  Sleep:      {summary['sleep']['avg30']} hrs avg (30d), trend: {summary['sleep']['trend']}")
    print(f"  HRV:        {summary['hrv']['avg30']} ms avg (30d), trend: {summary['hrv']['trend']}")
    print(f"  Resting HR: {summary['rhr']['avg30']} bpm avg (30d)")
    print(f"  Steps:      {summary['steps']['avg30']} avg/day (30d)")
    print(f"  VO2 Max:    {summary['vo2']['latest']}")
    print(f"  Workouts:   {len(workouts)} in last 90 days")
    print("\nDone. Refresh health-metrics.md in Cursor to see the full summary.")


if __name__ == "__main__":
    main()
