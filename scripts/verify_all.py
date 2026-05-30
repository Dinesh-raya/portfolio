# -*- coding: utf-8 -*-
"""Run static + optional UI verification."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(script: str) -> int:
    print(f"\n{'=' * 60}\nRunning {script}\n{'=' * 60}")
    result = subprocess.run([sys.executable, str(ROOT / "scripts" / script)], cwd=ROOT)
    return result.returncode


def main() -> int:
    code = run("verify.py")
    if code != 0:
        return code
    ui_code = run("verify_ui.py")
    return ui_code


if __name__ == "__main__":
    raise SystemExit(main())
