import gzip
import json
from pathlib import Path

from colour_tools import rgb_from_hue
from conf import root
from map_value import map_value

frame = json.loads(next(iter(Path(root, "bitmaps").glob("*"))).read_text())
height = len(frame)

conf = json.loads(gzip.decompress(Path(root, "config.json.gz").read_bytes()))

rainbow = [
    [float(x) for x in rgb_from_hue((1 * i) / height) + [1]] for i in range(height)
]
mappings = [
    round(
        map_value(
            i,
            0,
            len(rainbow) - 1,
            conf["min-y"],
            conf["max-y"],
        ),
        2,
    )
    for i in range(len(rainbow))
]


data = {"rainbow": rainbow, "index-mappings": mappings}

Path(root, "rainbow.json.gz").write_bytes(
    gzip.compress(json.dumps(data, separators=(",", ":")).encode("utf-8"), mtime=0)
)
Path(root, "rainbow.json").write_text(json.dumps(data, indent=2))
