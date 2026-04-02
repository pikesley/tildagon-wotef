from itertools import batched
from pathlib import Path

from PIL import Image

for move in Path("sources/crops").glob("*"):
    print(move)
    outdir = Path("sources/bitmaps", move.name)
    outdir.mkdir(exist_ok=True, parents=True)
    for file in Path(move).glob("*"):
        img = Image.open(file)

        width = img.width
        data = []

        for row in batched(img.get_flattened_data(), width):
            data.append("")
            for pixel in row:
                if pixel == (0, 0, 0):
                    data[-1] += "1"
                else:
                    data[-1] += "0"

        Path(outdir, f"{file.stem}.txt").write_text("\n".join(data))
