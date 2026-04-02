from pathlib import Path

from PIL import Image

move = "roundhouse"

left, top, width, height = 128, 324, 200, 120
for file in Path("caps", move).glob("*"):
    img = Image.open(file)
    with Path.open(f"crops/{move}/{file.name}", "wb") as f:
        img.crop((left, top, left + width, top + height)).save(f)
