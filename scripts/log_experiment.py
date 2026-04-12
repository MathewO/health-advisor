#!/usr/bin/env python3
"""
log_experiment.py — Quick CLI helper to add a new experiment to experiments.md.

Usage:
  python scripts/log_experiment.py

Or just ask Claude: "Log this as an experiment" and it will edit experiments.md directly.
"""

from datetime import date
from pathlib import Path

EXPERIMENTS_MD = Path(__file__).parent.parent / "experiments" / "experiments.md"


def ask(prompt, default=None):
    suffix = f" [{default}]" if default else ""
    val = input(f"{prompt}{suffix}: ").strip()
    return val if val else default


def main():
    print("\n=== Log New Experiment ===\n")

    title = ask("Experiment title (short description)")
    hypothesis = ask("Hypothesis (what do you expect to happen and why?)")
    change = ask("What exactly will you change or add?")
    start = ask("Start date", date.today().isoformat())
    duration = ask("Duration (e.g. 4 weeks, 30 days)")
    metric = ask("How will you measure success?")
    evidence = ask("Evidence basis (URL or research/ file path)", optional=True) if False else ask("Evidence basis (URL or research/ file path, or press Enter to skip)", "")

    entry = f"""
### {title}

| Field | Detail |
|---|---|
| Hypothesis | {hypothesis} |
| Change made | {change} |
| Start date | {start} |
| Duration | {duration} |
| Status | Active |
| Evidence basis | {evidence or '_(to be added)_'} |
| Success metric | {metric} |

#### Check-ins

- _(Add weekly notes here as you go)_

#### Outcome

_(To be completed at end of experiment)_

---
"""

    content = EXPERIMENTS_MD.read_text()

    marker = "## Active Experiments"
    if marker in content:
        content = content.replace(
            f"{marker}\n\n_(None running yet)_",
            f"{marker}\n{entry}"
        )
        if "_(None running yet)_" not in content:
            # Already has active experiments, insert after marker
            content = content.replace(
                f"{marker}\n",
                f"{marker}\n{entry}",
                1
            )
    else:
        content += entry

    EXPERIMENTS_MD.write_text(content)
    print(f"\nExperiment logged to {EXPERIMENTS_MD}")
    print("Open experiments.md in Cursor to add check-in notes as you go.")


if __name__ == "__main__":
    main()
