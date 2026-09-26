#!/usr/bin/env python3
"""Record the shape of every portfolio video, so the player can match it.

The modal is a fixed 16:10 box. A square ad or a 9:16 reel played inside it
gets black bars down both sides, and for the YouTube embeds that is the
embed's own letterboxing, which no CSS on our side can reach. Either way the
fix is the same: size the box to the clip instead of the clip to the box.

The player cannot measure a YouTube embed, and for a local file it would only
know the size after loading, which means the box would jump. So the shapes are
measured here, from the masters, and shipped as a small JSON file.

    python3 assets/build_aspects.py

Needs assets/video/, which is gigabytes and lives only on Catarina's Mac, so
this is run by hand like build_previews.py rather than from build.sh. The
output is committed.
"""
import json, pathlib, re, subprocess, sys

SRC_DIR = pathlib.Path("assets/video")
OUT = pathlib.Path("assets/aspect.json")


def referenced():
    src = pathlib.Path("assets/source.html").read_text(encoding="utf-8")
    return list(dict.fromkeys(re.findall(r"video:'assets/video/([^']+)'", src)))


def shape(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True).stdout.strip()
    try:
        w, h = [int(x) for x in out.split(",")[:2]]
        return w, h
    except ValueError:
        return None


def main():
    if not SRC_DIR.is_dir():
        sys.exit("no assets/video — the masters live on Catarina's Mac only")

    shapes, missing = {}, 0
    for name in referenced():
        f = SRC_DIR / name
        if not f.exists():
            missing += 1
            continue
        s = shape(f)
        if not s:
            continue
        w, h = s
        # Two decimals is far finer than a reader can see and keeps the file
        # small enough to be worth loading up front.
        shapes[name] = round(w / h, 3)

    OUT.write_text(json.dumps(shapes, indent=0, sort_keys=True) + "\n", encoding="utf-8")
    kinds = {}
    for r in shapes.values():
        k = "wide" if r > 1.5 else ("square" if r > 0.9 else "vertical")
        kinds[k] = kinds.get(k, 0) + 1
    print("  %d clips measured, %d masters missing" % (len(shapes), missing))
    print("  " + ", ".join("%s %d" % (k, n) for k, n in sorted(kinds.items())))


if __name__ == "__main__":
    main()
