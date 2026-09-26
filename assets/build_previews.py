#!/usr/bin/env python3
"""Make the small looping clips the portfolio plays on hover.

A grid of still frames is a strange way for an editor to show work that is
made of motion. These are three seconds, silent, 960px wide, and a little heavier each. Nothing downloads until someone hovers, so the page itself costs
nothing; only the card you point at is fetched.

The masters in assets/video/ are gigabytes and stay out of the repo. These are
generated from them and committed, because they are small enough to be part of
the site.

    python3 assets/build_previews.py [--seek 5] [--len 3] [--force]

Skips anything already made, so re-running is cheap. Pass --force to redo.
"""
import argparse, pathlib, re, subprocess, sys

# Hand-picked start times, in seconds, for clips where the automatic choice
# lands badly — on a static slide, mid-transition, or on a moment that does not
# represent the piece. Scene detection finds cuts; it cannot tell which moment
# is the one worth showing.
OVERRIDES = {
    "aischool-lesson-3-3.mp4": 30,              # the host to camera; graphics start at 36
    "thinkshop.mp4": 5,                         # the animated title sequence
    "espanita.mp4": 131,                        # at the bar, bottle and skyline in frame
    "fiveoaks.mp4": 33,                         # photos animating in, no talking head
    "thetaray.mp4": 1.5,                        # the kinetic type open
    "kaust-testimonials.mp4": 135,              # one interview, held; no lower-third across it
    "fatbrands-highlight-reel.mp4": 104,        # beer pour into the food shots
    "99bitcoins-saudi-arabia.mp4": 29,          # the mBridge diagram assembling
    "fairmont-3.mp4": 11,                       # the third reel, her in the bedroom
    "feamaero.mp4": 14.2,                       # the whole map build; the dots land at 19 and it is still after
    "danone-meet-the-board.mp4": 8,             # talking heads with their name cards
    "similarweb.mp4": 285,                      # three seconds later than it chose
    "snowlodge.mp4": 35,                        # later, once the room is full
    "savage-4-investigative-errors.mp4": 18,    # the host beside the bars building
}

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


def duration(src):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(src)], capture_output=True, text=True).stdout.strip()
    try:
        return float(out)
    except ValueError:
        return 0.0


def in_point(src, length):
    """Where to start, so the clip opens on a cut rather than mid-dissolve.

    A fixed offset lands on title cards, logo stings and black just often
    enough to look careless. This finds the real cuts and takes the first one
    past the opening, which is where the piece is usually doing something.
    Scene detection has to run over the whole file — seeking first leaves the
    filter without a previous frame to compare against, and it reports nothing.
    """
    dur = duration(src)
    if dur < length + 2:
        return 0.0
    earliest, latest = dur * 0.15, dur - length - 0.5
    out = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(src),
         "-vf", "select='gt(scene,0.25)',metadata=print:file=-", "-an", "-f", "null", "-"],
        capture_output=True, text=True)
    cuts = [float(m) for m in re.findall(r"pts_time:([0-9.]+)", out.stdout + out.stderr)]
    for t in cuts:
        if earliest <= t <= latest:
            return round(t, 2)
    return round(min(max(earliest, dur * 0.20), max(latest, 0.0)), 2)


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
        "-c:v", "libx264", "-crf", "22", "-preset", "slow",
        "-pix_fmt", "yuv420p",                  # Safari refuses anything else
        "-movflags", "+faststart",              # first frame without the whole file
        str(dst),
    ]
    return subprocess.run(cmd, capture_output=True).returncode == 0


def main():
    p = argparse.ArgumentParser(description="Generate hover previews.")
    p.add_argument("--seek", type=float, default=None,
                   help="fixed start; omitted, the first cut past the opening is used")
    p.add_argument("--len", type=float, default=5, dest="length")
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
        seek = (a.seek if a.seek is not None
                else OVERRIDES.get(name, None))
        if seek is None:
            seek = in_point(src, a.length)
        if make(src, dst, seek, a.length):
            made += 1
            total += dst.stat().st_size
        else:
            print("  ! failed: %s" % name)

    print("  %d made, %d already there, %d masters missing" % (made, skipped, missing))
    if total:
        print("  %d previews, %.1f MB total" % (made + skipped, total / 1024 / 1024))


if __name__ == "__main__":
    main()
