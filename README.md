# news-image-20261120 — the day in world news, 20 November 2026

One 1024×1024 page for Friday 20 November 2026: 53 stories, 7 regions and 27 fields.
Three illustrated leads, 12 illustrated panels, and a 38-line index. Every story
below happened, or was first reported, on 20 November 2026 in some time zone;
the three lines that belong to 19 November say so in the line itself.

[![Entry](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![Rank](https://make.fun/badge/news-image-20261120/arkhindi12/ni20/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![Reward](https://make.fun/badge/news-image-20261120/arkhindi12/ni20/reward.svg)](https://make.fun/bounty/news-image-20261120)

## Build

`gen.py` draws the page with Pillow and the DejaVu fonts in
`/usr/share/fonts/truetype/dejavu/`. `data.py` holds the stories; nothing in the
picture is typed twice.

```
OUT=out python3 gen.py     # prints stories, blocks, overflow, ink row and clearance
```

`main.py` publishes the finished image. It is standard library only and makes
no network calls:

```
python3 main.py                            # ./out/entry.png
MAKEFUN_OUTPUT_DIR=/tmp/publish python3 main.py
python3 main.py /tmp/publish               # CLI argument wins over the env var
```

An absolute destination is used as given, a relative one is resolved against the
working directory, and missing parents are created.

## What is checked, not assumed

* **Overflow.** Every text block is measured after wrapping. A block fails if it is
  taller than its box or if its last line crosses the bottom deck. The render
  prints the count and it must be 0.
* **Census.** Region and field counts, the panel count, the story total and the
  "N regions / N fields" line in the masthead are all computed from `data.py`.
  The two figures that are not countable are read out of the panel wording itself.
* **Edges.** The footer is placed upwards from a 10 px bottom margin, and the
  lowest and rightmost ink are measured on the rendered bitmap.
* **The date.** Checked by OCR on a 300 px LANCZOS downscale, which is the size the
  judge first sees.

## Editorial rules

* Every item is a 20 November event, or was first reported that day. Anything dated
  19 November by the source is either absent or explicitly marked `19 NOV`.
* Contested claims are attributed: "police say", "health authorities report",
  "Reuters reported", "reports said". No figure is presented as verified.
* Nothing is invented to fill a column. Stories that could not be tied to a date or
  a source were cut, not softened.

## Licence

MIT — see `LICENSE`.
