from pathlib import Path

frames = {}

leading = 100
trailing = 100

move = "roundhouse"

for j in Path("bitmaps", move).glob("*"):
    frames[j.stem] = j.read_text(encoding="utf-8")

for data in frames.values():
    for row in data.split("\n"):
        l_counter = 0
        for pixel in row:
            if pixel != "_":
                if l_counter < leading:
                    leading = l_counter
                    break
            else:
                l_counter += 1

        r_counter = 0
        for pixel in reversed(row):
            if pixel != "_":
                if r_counter < trailing:
                    trailing = r_counter
                    break
            else:
                r_counter += 1

print(leading, trailing)

leading -= 1
trailing -= 1

for key, data in frames.items():
    slimmed = []
    for row in data.split("\n"):
        slimmed.append(row[leading:-trailing])

    Path("slimmed_bitmaps", move, f"{key}.txt").write_text("\n".join(slimmed))
