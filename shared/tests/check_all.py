#!/usr/bin/env python3
"""Run static checks and unit tests for every mod in this repository."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MOD_ROOTS = (ROOT / "mods" / "owned", ROOT / "mods" / "patches")

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_mod import check_mod  # noqa: E402


def mod_dirs() -> list[Path]:
    return sorted(
        path
        for root in MOD_ROOTS
        if root.is_dir()
        for path in root.iterdir()
        if path.is_dir() and not path.name.startswith(".")
    )


def run_tests(mod: Path) -> tuple[int, str]:
    tests = mod / "Tests"
    if not tests.is_dir():
        return 0, ""
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", str(tests), "-q"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    output = (result.stdout + result.stderr).strip()
    return result.returncode, output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    results: dict[str, dict[str, object]] = {}
    failed = False
    for mod in mod_dirs():
        errors = check_mod(mod)
        test_code, test_output = run_tests(mod)
        results[mod.name] = {
            "static_errors": errors,
            "unit_test_exit": test_code,
            "unit_test_output": test_output,
        }
        if errors or test_code != 0:
            failed = True

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        if not results:
            print("No mods found.")
        for name, result in results.items():
            static_errors = result["static_errors"]
            unit_code = result["unit_test_exit"]
            print(f"{'FAIL' if static_errors or unit_code else 'OK  '} {name}")
            for error in static_errors:  # type: ignore[union-attr]
                print(f"  static: {error}")
            if unit_code:
                print(f"  unit tests exit {unit_code}")
                if result["unit_test_output"]:
                    print(str(result["unit_test_output"]))
        print("all checks passed" if not failed else "FAILED")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
