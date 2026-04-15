from pathlib import Path

from PIL import Image

left, top, width, height = 128, 330, 200, 106

for move in Path("sources/caps").glob("*"):
    # print(move)
    outdir = Path("sources/crops", move.name)
    outdir.mkdir(exist_ok=True, parents=True)

    for file in Path(move).glob("*"):
        img = Image.open(file)
        with Path.open(f"{outdir}/{file.name}", "wb") as f:
            img.crop((left, top, left + width, top + height)).save(f)
