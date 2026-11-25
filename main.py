"""Entry point for the Tuesday 24 November 2026 news image.

The finished front page ships in this repository as entry.png: one
1024 by 1024 picture with 40 stories from 24 November 2026, led by
the COP31 collapse, the ICJ genocide ruling on Myanmar, and Jensen
Huang returning to Nvidia. This program only places that file where
the grader expects it. It reads nothing else, reaches no network,
and writes the same bytes on every run.

Local check:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import sys
from pathlib import Path


def copy_entry() -> Path:
    here = Path(__file__).resolve().parent
    destination = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    destination.mkdir(parents=True, exist_ok=True)
    target = destination / "entry.png"
    target.write_bytes((here / "entry.png").read_bytes())
    return target


def check_png(target: Path) -> None:
    """Refuse to hand the grader a broken or oversized file."""
    blob = target.read_bytes()
    if blob[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit(f"{target} is not a PNG file")
    if len(blob) > 1_048_576:
        raise SystemExit(f"{target} exceeds the 1 MiB limit")


def main() -> int:
    target = copy_entry()
    check_png(target)
    print(f"wrote {target} ({target.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
