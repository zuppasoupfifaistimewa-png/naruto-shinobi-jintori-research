#!/usr/bin/env python3
"""Inspect pinned tool CLI options before the reproducible Step 5 comparison."""
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe", required=True, help="output text file for command help")
    args = parser.parse_args()
    chunks: list[str] = []
    for command in (
        ["singleFileDisasm", "--help"],
        ["m2c", "--help"],
        ["python", "-m", "spimdisasm.singleFileDisasm", "--help"],
    ):
        chunks.append("$ " + " ".join(command))
        result = subprocess.run(
            command, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            check=False, timeout=30,
        )
        chunks.append(f"exit_code={result.returncode}")
        chunks.append(result.stdout or "(no output)")
    Path(args.probe).write_text("\n".join(chunks) + "\n", encoding="utf-8")
    if not any("usage:" in chunk.lower() or "options:" in chunk.lower() for chunk in chunks):
        raise SystemExit("Tool CLI probe produced no usage/help output.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
