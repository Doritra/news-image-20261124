"""News-image entry for Tuesday 24 November 2026.

The repository ships the finished front page as entry.png: one
1024x1024 picture holding 40 stories reported on 24 November 2026,
led by the collapse of the COP31 climate talks in Antalya, the ICJ
genocide ruling on Myanmar, and Jensen Huang's return to Nvidia.
Eight sections cover Europe, Asia-Pacific, the Middle East, Africa,
the Americas, economy and technology, science and health, and sport
and culture, plus a "day in numbers" strip. This program copies that
image to the output directory, byte for byte, with no network use.

Outside the grader, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
from pathlib import Path


def main() -> None:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    source = Path(__file__).resolve().parent / "entry.png"
    target = out_dir / "entry.png"
    shutil.copyfile(source, target)
    # Guard the gate: the shipped file must be a whole PNG within limits.
    data = target.read_bytes()
    assert data[:8] == b"\x89PNG\r\n\x1a\n", "entry.png is not a PNG"
    assert len(data) <= 1_048_576, "entry.png exceeds 1 MiB"


if __name__ == "__main__":
    main()
