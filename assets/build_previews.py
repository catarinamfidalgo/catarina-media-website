#!/usr/bin/env python3
"""Make the small looping clips the portfolio plays on hover.

A grid of still frames is a strange way for an editor to show work that is
made of motion. These are three seconds, silent, 960px wide, and around
270KB each. Nothing downloads until someone hovers, so the page itself costs
nothing; only the card you point at is fetched.

The masters in assets/video/ are gigabytes and stay out of the repo. These are
generated from them and committed, because they are small enough to be part of
the site.

    python3 assets/build_previews.py [--seek 5] [--len 3] [--force]

Skips anything already made, so re-running is cheap. Pass --force to redo.
"""
import argparse, pathlib, re, subprocess, sys

SRC_DIR = pathlib.Path("assets/video")
OUT_DIR = pathlib.Path("assets/preview")


def referenced_videos():
    """Every video the portfolio data points at, in order of appearance."""
    src = pathlib.Path("assets/source.html").read_text(encoding="utf-8")
    seen, out = set(), []
    for m in re.finditer(r"video:'(assets/video/([^']+))'", src):
        name = m.group(2)
        if name and name not in seen:
            seen.add(name)
            out.append(name)
    return out


def make(src, dst, seek, length):
    cmd = [
        "ffmpeg", "-y", "-ss", str(seek), "-t", str(length), "-i", str(src),
        "-an",                                  # silent: it autoplays on hover
        # The grid is full-bleed, so on a wide screen a card is around 460px
        # across — roughly 920 on a retina display. 480 was half what it needed
        # and looked it. 24fps because this is showing cutting, and motion that
        # stutters undersells the work.
        # Crop to the card's 4:3 before scaling. Without this a vertical reel
        # becomes 960x1700 — an enormous frame whose top and bottom the card
        # crops away regardless, which is how one three-second clip reached
        # 1.1MB. Every preview now lands on the same 960x720.
        "-vf", ("crop='min(iw,ih*4/3)':'min(ih,iw*3/4)',"
                "scale=960:720,fps=24"),
        "-c:v", "libx264", "-crf", "26", "-preset", "slow",
        "-pix_fmt", "yuv420p",                  # Safari refuses anything else
        "-movflags", "+faststart",              # first frame without the whole file
        str(dst),
    ]
    return subprocess.run(cmd, capture_output=True).returncode == 0


def main():
    p = argparse.ArgumentParser(description="Generate hover previews.")
    p.add_argument("--seek", type=float, default=5, help="seconds in to start")
    p.add_argument("--len", type=float, default=3, dest="length")
    p.add_argument("--force", action="store_true")
    a = p.parse_args()

    if not SRC_DIR.is_dir():
        sys.exit("no assets/video — the masters live on Catarina's Mac only")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    made = skipped = missing = 0
    total = 0

    for name in referenced_videos():
        src, dst = SRC_DIR / name, OUT_DIR / name
        if not src.exists():
            missing += 1
            continue
        if dst.exists() and not a.force:
            skipped += 1
            total += dst.stat().st_size
            continue
        if make(src, dst, a.seek, a.length):
            made += 1
            total += dst.stat().st_size
        else:
            print("  ! failed: %s" % name)

    print("  %d made, %d already there, %d masters missing" % (made, skipped, missing))
    if total:
        print("  %d previews, %.1f MB total" % (made + skipped, total / 1024 / 1024))


if __name__ == "__main__":
    main()
