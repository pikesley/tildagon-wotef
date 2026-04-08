import gzip
import json
from hashlib import sha256
from itertools import batched
from pathlib import Path

from conf import app_conf, clean, root
from PIL import Image

clean()

bitmap_dir = Path(root, "bitmaps")
bitmap_dir.mkdir(exist_ok=True, parents=True)

framesets = {}

for move in Path("sources/crops").glob("*"):
    print(move)
    fs = []

    for file in sorted(Path(move).glob("*")):
        digest = sha256(file.read_bytes()).hexdigest()
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

    framesets[move.stem] = [
        (fs[i], app_conf["moves"][move.stem]["intervals"][i])
        for i in app_conf["moves"][move.stem]["order"]
    ]


Path(root, "framesets.json.gz").write_bytes(
    gzip.compress(
        json.dumps(framesets, separators=(",", ":")).encode("utf-8"), mtime=None
    )
)

Path(root, "framesets.json").write_text(json.dumps(framesets, indent=2))
