#!/usr/bin/env python3
"""
parse_apple_health.py — Parse an Apple Health export and write a summary to health-metrics.md.

How to export from iPhone:
  1. Open the Health app
  2. Tap your profile photo (top right)
  3. Scroll down → Export All Health Data
  4. AirDrop or share the export.zip to your Mac
  5. Place export.zip in the health-advisor/data/ folder
  6. Run: python scripts/parse_apple_health.py

The script extracts key metrics and updates profile/health-metrics.md.
"""

import xml.etree.ElementTree as ET
import zipfile
import statistics
from datetime import datetime, date, timedelta
from pathlib import Path
from collections import defaultdict

DATA_DIR = Path(__file__).parent.parent / "data"
METRICS_MD = Path(__file__).parent.parent / "profile" / "health-metrics.md"

RECORD_TYPES = {
    "HKQuantityTypeIdentifierHeartRateVariabilitySDNN": "hrv",
    "HKQuantityTypeIdentifierRestingHeartRate": "resting_hr",
    "HKQuantityTypeIdentifierStepCount": "steps",
    "HKQuantityTypeIdentifierActiveEnergyBurned": "active_calories",
    "HKQuantityTypeIdentifierAppleExerciseTime": "exercise_minutes",
    "HKQuantityTypeIdentifierAppleStandHour": "stand_hours",
    "HKQuantityTypeIdentifierBodyMass": "weight",
    "HKQuantityTypeIdentifierVO2Max": "vo2max",
}

# These metrics are recorded by multiple sources (iPhone, third-party apps, Watch).
# Restrict to Apple Watch only to avoid double-counting.
WATCH_ONLY_KEYS = {"steps", "active_calories"}


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
            raw_date = record.get("startDate", "")
            # Normalise timezone offset format so fromisoformat handles it
            import re as _re
            raw_date = _re.sub(r" ([+-]\d{2})(\d{2})$", r" \1:\2", raw_date)
            dt = datetime.fromisoformat(raw_date).date()
        except (ValueError, TypeError):
            continue

        data[key].append((dt, val))

    # Parse sleep separately (it uses CategorySamples)
    sleep_data = []
    for sample in root.iter("Record"):
        if sample.get("type") != "HKCategoryTypeIdentifierSleepAnalysis":
            continue
        val = sample.get("value", "")
        if "Asleep" not in val:
            continue
        try:
            import re as _re
            raw_start = _re.sub(r" ([+-]\d{2})(\d{2})$", r" \1:\2", sample.get("startDate", ""))
            raw_end = _re.sub(r" ([+-]\d{2})(\d{2})$", r" \1:\2", sample.get("endDate", ""))
            start = datetime.fromisoformat(raw_start)
            end = datetime.fromisoformat(raw_end)
            hours = (end - start).total_seconds() / 3600
            if 0.05 < hours < 14:
                # Assign sleep to the morning date (end date), so a night starting
                # at 11pm and ending at 7am is grouped under the 7am date
                sleep_data.append((end.date(), hours))
        except (ValueError, TypeError):
            continue

    return data, sleep_data, cutoff_30, cutoff_90


def avg(values):
    return round(statistics.mean(values), 1) if values else None


def trend(recent, older):
    if not recent or not older:
        return "—"
    diff = avg(recent) - avg(older)
    if abs(diff) < 1:
        return "Stable"
    return f"{'↑' if diff > 0 else '↓'} {abs(round(diff, 1))}"


def summarise(data, sleep_data, cutoff_30, cutoff_90):
    def split(key):
        all_vals = data.get(key, [])
        r30 = [v for d, v in all_vals if d >= cutoff_30]
        r90 = [v for d, v in all_vals if cutoff_90 <= d < cutoff_30]
        return r30, r90

    def split_sleep():
        # Aggregate segments to daily totals first, then split by window.
        # Exclude dates with < 3 hrs total — these represent nights the watch wasn't worn,
        # not genuine short sleep, and would skew the average downward.
        by_day = defaultdict(float)
        for d, v in sleep_data:
            by_day[d] += v
        tracked_nights = {d: v for d, v in by_day.items() if v >= 3.0}
        r30 = [v for d, v in tracked_nights.items() if d >= cutoff_30]
        r90 = [v for d, v in tracked_nights.items() if cutoff_90 <= d < cutoff_30]
        return r30, r90

    sleep30, sleep90 = split_sleep()
    hrv30, hrv90 = split("hrv")
    rhr30, rhr90 = split("resting_hr")
    steps30, steps90 = split("steps")

    # Steps are per-entry, aggregate to daily
    def daily_sum(key):
        by_day = defaultdict(float)
        for d, v in data.get(key, []):
            by_day[d] += v
        r30 = [v for d, v in by_day.items() if d >= cutoff_30]
        r90 = [v for d, v in by_day.items() if cutoff_90 <= d < cutoff_30]
        return r30, r90

    steps30, steps90 = daily_sum("steps")
    cal30, cal90 = daily_sum("active_calories")
    ex30, ex90 = daily_sum("exercise_minutes")

    weight_vals = sorted(data.get("weight", []), key=lambda x: x[0])
    latest_weight = weight_vals[-1][1] if weight_vals else None
    prev_weight = weight_vals[-30][1] if len(weight_vals) >= 30 else (weight_vals[0][1] if weight_vals else None)

    vo2_vals = sorted(data.get("vo2max", []), key=lambda x: x[0])
    latest_vo2 = vo2_vals[-1][1] if vo2_vals else None

    return {
        "sleep": {"avg30": avg(sleep30), "avg90": avg(sleep90), "trend": trend(sleep30, sleep90)},
        "hrv": {"avg30": avg(hrv30), "avg90": avg(hrv90), "trend": trend(hrv30, hrv90)},
        "rhr": {"avg30": avg(rhr30), "avg90": avg(rhr90), "trend": trend(rhr30, rhr90)},
        "steps": {"avg30": avg(steps30), "avg90": avg(steps90), "trend": trend(steps30, steps90)},
        "calories": {"avg30": avg(cal30), "avg90": avg(cal90), "trend": trend(cal30, cal90)},
        "exercise": {"avg30": avg(ex30), "avg90": avg(ex90), "trend": trend(ex30, ex90)},
        "weight": {"latest": latest_weight, "trend": f"{'↑' if latest_weight and prev_weight and latest_weight > prev_weight else '↓' if latest_weight and prev_weight and latest_weight < prev_weight else 'Stable'}"},
        "vo2": {"latest": latest_vo2},
    }


def write_metrics_md(s):
    def fmt(val, unit=""):
        return f"{val}{unit}" if val is not None else "—"

    today = date.today().isoformat()
    md = f"""# Health Metrics

> Auto-generated from Apple Health export. Do not edit manually.
> To update: export from iPhone Health app, place `export.zip` in `data/`, run `python scripts/parse_apple_health.py`

---

## Last Updated

{today}

---

## Sleep

| Metric | 30-day avg | 90-day avg | Trend |
|---|---|---|---|
| Total sleep | {fmt(s['sleep']['avg30'], ' hrs')} | {fmt(s['sleep']['avg90'], ' hrs')} | {s['sleep']['trend']} |

---

## Heart Rate & HRV

| Metric | 30-day avg | 90-day avg | Trend |
|---|---|---|---|
| Resting heart rate | {fmt(s['rhr']['avg30'], ' bpm')} | {fmt(s['rhr']['avg90'], ' bpm')} | {s['rhr']['trend']} |
| HRV (SDNN) | {fmt(s['hrv']['avg30'], ' ms')} | {fmt(s['hrv']['avg90'], ' ms')} | {s['hrv']['trend']} |

---

## Activity

| Metric | 30-day avg | 90-day avg | Trend |
|---|---|---|---|
| Steps | {fmt(s['steps']['avg30'])} | {fmt(s['steps']['avg90'])} | {s['steps']['trend']} |
| Active calories | {fmt(s['calories']['avg30'], ' kcal')} | {fmt(s['calories']['avg90'], ' kcal')} | {s['calories']['trend']} |
| Exercise minutes | {fmt(s['exercise']['avg30'], ' min')} | {fmt(s['exercise']['avg90'], ' min')} | {s['exercise']['trend']} |

---

## Body

| Metric | Latest | Source |
|---|---|---|
| Weight | See `profile/weight-log.md` | Self-reported morning weight — not pulled from Apple Health |

---

## VO2 Max

| Metric | Latest |
|---|---|
| VO2 Max (estimated) | {fmt(s['vo2']['latest'], ' mL/kg/min')} |
"""

    with open(METRICS_MD, "w") as f:
        f.write(md)
    print(f"\nWritten to {METRICS_MD}")


def main():
    DATA_DIR.mkdir(exist_ok=True)
    xml_path = find_export()
    if not xml_path:
        return

    data, sleep_data, cutoff_30, cutoff_90 = parse_records(xml_path)
    summary = summarise(data, sleep_data, cutoff_30, cutoff_90)
    write_metrics_md(summary)

    print("\nKey metrics:")
    print(f"  Sleep:    {summary['sleep']['avg30']} hrs avg (30d), trend: {summary['sleep']['trend']}")
    print(f"  HRV:      {summary['hrv']['avg30']} ms avg (30d), trend: {summary['hrv']['trend']}")
    print(f"  Resting HR: {summary['rhr']['avg30']} bpm avg (30d)")
    print(f"  Steps:    {summary['steps']['avg30']} avg/day (30d)")
    print(f"  Weight:   {summary['weight']['latest']} kg")
    print(f"  VO2 Max:  {summary['vo2']['latest']}")
    print("\nDone. Refresh health-metrics.md in Cursor to see the full summary.")


if __name__ == "__main__":
    main()
