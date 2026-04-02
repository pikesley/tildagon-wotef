from itertools import batched
from pathlib import Path

from PIL import Image

move = "roundhouse"
Path("bitmaps", move).mkdir(exist_ok=True, parents=True)

for file in Path("crops", move).glob("*"):
    img = Image.open(file)

    width = img.width
    data = []

    for row in batched(img.get_flattened_data(), width):
        data.append("")
        for pixel in row:
            if pixel == (0, 0, 0):
                data[-1] += "O"
            else:
                data[-1] += "_"

    Path("bitmaps", move, f"{file.stem}.txt").write_text("\n".join(data))
