def run_length_encode(line):
    """RLE."""
    data = []

    current = line[0]
    count = 0

    for char in line:
        if char == current:
            count += 1
        else:
            data.append((current, count))
            current = char
            count = 1

    data.append((current, count))
    return data


if __name__ == "__main__":
    import json
    from pathlib import Path

    for move in Path("sources/slimmed_bitmaps").glob("*"):
        print(move)
        outdir = Path("sources/rle", move.name)
        outdir.mkdir(exist_ok=True, parents=True)

        for file in Path(move).glob("*"):
            data = file.read_text(encoding="utf-8").split("\n")
            encoded = [run_length_encode(line) for line in data]

            Path(outdir, f"{file.stem}.json").write_text(
                json.dumps(encoded), encoding="utf-8"
            )
