import gzip
import json
from hashlib import sha256
from itertools import batched
from pathlib import Path

from conf import clean, pre_render_conf, root
from PIL import Image

digest_length = 4

clean()

bitmap_dir = Path(root, "bitmaps")
bitmap_dir.mkdir(exist_ok=True, parents=True)

framesets = {}

for move in Path("sources/crops").glob("*"):
    # print(move)
    fs = []

    for file in sorted(Path(move).glob("*")):
        digest = sha256(file.read_bytes()).hexdigest()[0:digest_length]
        fs.append(digest)
        img = Image.open(file)
        width = img.width
        data = []

        for row in batched(img.get_flattened_data(), width):
            data.append([])
            for pixel in row:
                if pixel == (0, 0, 0):
                    data[-1].append(1)
                else:
                    data[-1].append(0)

        Path(bitmap_dir, f"{digest}.json").write_text(json.dumps(data))

    # append the first frame at the end
    intervals = pre_render_conf["moves"][move.stem]["intervals"] + [0, 0]
    ordering = pre_render_conf["moves"][move.stem]["order"] + [0, 0]

    framesets[move.stem] = {
        "frames": [(fs[i], intervals[i]) for i in ordering],
        "impact-frame": pre_render_conf["moves"][move.stem]["impact"],
    }


Path("framesets.json.gz").write_bytes(
    gzip.compress(json.dumps(framesets, separators=(",", ":")).encode("utf-8"), mtime=0)
)

Path(root, "framesets.json").write_text(json.dumps(framesets, indent=2))
