#!/usr/bin/env python3
"""Publish the finished entry image.

Standard library only (no Pillow, no network): it copies the already-rendered
``entry.png`` next to this file into an output directory and reports where it
landed.

    python3 main.py                 # writes ./out/entry.png
    MAKEFUN_OUTPUT_DIR=/tmp/x python3 main.py
    python3 main.py /tmp/y          # an explicit directory wins over the env var

The destination is honoured as given: an absolute path is used as-is, a
relative path is resolved against the current working directory. Missing
parents are created. Running it twice overwrites, and the bytes are identical.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
NAME = "entry.png"


def destination(argv):
    """Precedence: first CLI argument, then $MAKEFUN_OUTPUT_DIR, then ./out."""
    if len(argv) > 1 and argv[1].strip():
        return argv[1]
    env = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    return env if env else "out"


def main(argv):
    if not os.path.isfile(SOURCE):
        sys.stderr.write("missing source image: %s\n" % SOURCE)
        return 1
    target = os.path.abspath(os.path.expanduser(destination(argv)))
    try:
        os.makedirs(target, exist_ok=True)
        out = os.path.join(target, NAME)
        shutil.copyfile(SOURCE, out)
    except OSError as exc:
        sys.stderr.write("could not write %s: %s\n" % (target, exc))
        return 1
    size = os.path.getsize(out)
    sys.stdout.write("wrote %s (%d bytes)\n" % (out, size))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
