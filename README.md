[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/Doritra/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/Doritra/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

# news-image-20261124 — The World in One Day

One 1024x1024 front page summing up the world's news of
**Tuesday 24 November 2026**: 40 stories, led by the COP31 climate
talks collapsing in Antalya, the ICJ ruling that Myanmar committed
genocide against the Rohingya, and Jensen Huang's return as Nvidia
chief executive. Eight sections span Europe, Asia-Pacific, the
Middle East, Africa, the Americas, economy and technology, science
and health, and sport and culture, plus a "day in numbers" strip.

## Files

- `entry.png` — the finished front page (1024x1024, under 1 MiB).
- `main.py` — the entrypoint: copies `entry.png` to the output
  directory, byte for byte. Standard library only, no network.
- `build_image.py` — the renderer used to draw `entry.png` with
  Pillow from the story lists (deterministic: two runs write
  identical bytes). Build-time only; the grader runs `main.py`.
- `LICENSE` — MIT.

## Check locally

```sh
python3 build_image.py        # re-render entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```
