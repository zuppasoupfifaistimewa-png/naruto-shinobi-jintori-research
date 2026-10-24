"""Fail-closed health policy for the adaptive Story Mode player monitor.

A skipped player run is not gameplay success. If it completed as skipped and
has no player evidence artifact, classify it as an intentional no-execution
/ NO-GO state rather than a monitor failure. All actual failures, suspicious
artifacts, and overdue active runs remain alerts.
"""
from __future__ import annotations

import argparse
import json
from typing import Any


def assess_monitor(
    *, status: str, conclusion: str | None, age_seconds: int, artifact_count: int
) -> dict[str, Any]:
    """Return an auditable monitor classification without conflating skip with success."""
    status = (status or "").strip().lower()
    conclusion = (conclusion or "").strip().lower() or None
    age_seconds = max(0, int(age_seconds))
    artifact_count = max(0, int(artifact_count))

    active = status in {"queued", "in_progress"}
    expected_gated_skip = (
        status == "completed" and conclusion == "skipped" and artifact_count == 0
    )
    active_warn = active and age_seconds > 900
    failure_warn = not active and not expected_gated_skip and conclusion != "success"
    artifact_warn = (
        status == "completed" and artifact_count < 1 and not expected_gated_skip
    )

    if expected_gated_skip:
        classification = "EXPECTED_GATED_SKIP_NO_GO"
    elif active_warn or failure_warn or artifact_warn:
        classification = "WARNING"
    else:
        classification = "OK"

    return {
        "classification": classification,
        "active_warn": bool(active_warn),
        "failure_warn": bool(failure_warn),
        "artifact_warn": bool(artifact_warn),
        "expected_gated_skip": bool(expected_gated_skip),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--status", required=True)
    parser.add_argument("--conclusion", default=None)
    parser.add_argument("--age-seconds", required=True, type=int)
    parser.add_argument("--artifact-count", required=True, type=int)
    args = parser.parse_args()
    print(json.dumps(assess_monitor(
        status=args.status,
        conclusion=args.conclusion,
        age_seconds=args.age_seconds,
        artifact_count=args.artifact_count,
    ), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
