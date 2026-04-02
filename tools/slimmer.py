from pathlib import Path

frames = {}

leading = 100
trailing = 100

for move in Path("sources/bitmaps").glob("*"):
    print(move)
    for j in Path(move).glob("*"):
        frames[j.stem] = j.read_text(encoding="utf-8")

    for data in frames.values():
        for row in data.split("\n"):
            l_counter = 0
            for pixel in row:
                if pixel != "0":
                    if l_counter < leading:
                        leading = l_counter
                        break
                else:
                    l_counter += 1

            r_counter = 0
            for pixel in reversed(row):
                if pixel != "0":
                    if r_counter < trailing:
                        trailing = r_counter
                        break
                else:
                    r_counter += 1

leading -= 1
trailing -= 1

for move in Path("sources/bitmaps").glob("*"):
    print(move)
    outdir = Path("sources/slimmed_bitmaps", move.name)
    outdir.mkdir(exist_ok=True, parents=True)
    for j in Path(move).glob("*"):
        frames[j.stem] = j.read_text(encoding="utf-8")

    for key, data in frames.items():
        slimmed = []
        for row in data.split("\n"):
            slimmed.append(row[leading:-trailing])

        Path(outdir, f"{key}.txt").write_text("\n".join(slimmed))
