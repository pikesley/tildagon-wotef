import json
from pathlib import Path

from conf import root

frames = {}

leading = 100
trailing = 100

for frame in Path(root, "bitmaps").glob("*"):
    frames[frame.stem] = json.loads(frame.read_text(encoding="utf-8"))

    for data in frames.values():
        for row in data:
            l_counter = 0
            for pixel in row:
                if pixel != 0:
                    if l_counter < leading:
                        leading = l_counter
                        break
                else:
                    l_counter += 1

            r_counter = 0
            for pixel in reversed(row):
                if pixel != 0:
                    if r_counter < trailing:
                        trailing = r_counter
                        break
                else:
                    r_counter += 1


outdir = Path(root, "slimmed")
outdir.mkdir(exist_ok=True, parents=True)

for digest, frame in frames.items():
    slimmed = [row[leading:-trailing] for row in frame]
    Path(outdir, f"{digest}.json").write_text(json.dumps(slimmed))
