from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

FAKES = Path(__file__).resolve().parent / "fakes"
ROOT = Path(__file__).resolve().parents[1]


def test_cli_help():
    env = os.environ.copy()
    env["PYTHONPATH"] = str(FAKES) + os.pathsep + str(ROOT)
    cmd = [sys.executable, "-m", "livetranscriber.livetranscriber", "--help"]
    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    assert result.returncode == 0
    assert "usage:" in result.stdout
