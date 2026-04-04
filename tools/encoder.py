import gzip
from pathlib import Path

import yaml

conf = yaml.safe_load(Path("conf.yaml").read_text(encoding="utf-8"))


def encode_line(line):
    """Encode just the `1`s from a line."""
    result = []

    current = line[0]
    count = 0
    start_index = 0

    for index, char in enumerate(line):
        if char == current:
            count += 1
        else:
            if current == "1":
                result.append([start_index, count])
            current = char
            count = 1
            start_index = index

    if current == "1":
        result.append([start_index, count])

    return result


def scale_encode_line(line, scale):
    """Encode with scale and offset."""
    return [[(e[0] - len(line) / 2) * scale, e[1] * scale] for e in encode_line(line)]


def encode_block(block):
    """Encode a block of text."""
    lines = block.split("\n")
    result = []

    for index, line in enumerate(lines):
        result.extend([x + [index] for x in encode_line(line)])

    return result


def scale_encode_block(block, scale):
    """Scale-encode a block of text."""
    scaled_lines = [scale_encode_line(line, scale=scale) for line in block.split("\n")]
    result = []
    offset = len(scaled_lines) / 2

    for index, line in enumerate(scaled_lines):
        result.extend([item + [(index - offset) * scale] for item in line])

    return result


def encode(block):
    """Encode."""
    return scale_encode_block(block, conf["scale"])


if __name__ == "__main__":
    import json
    from pathlib import Path

    outdir = Path(
        "sources/encoded",
    )
    outdir.mkdir(exist_ok=True, parents=True)

    for move in Path("sources/slimmed_bitmaps").glob("*"):
        print(move)
        # outdir = Path("sources/encoded", move.name)
        # outdir.mkdir(exist_ok=True, parents=True)

        frames = []

        for file in sorted(Path(move).glob("*")):
            data = file.read_text(encoding="utf-8")
            encoded = encode(data)

            frames.append(encoded)

            # Path(outdir, f"{file.stem}.json").write_text(
            #     json.dumps(encoded), encoding="utf-8"
            # )

        Path(outdir, f"{move.name}.json.gz").write_bytes(
            gzip.compress(json.dumps(frames).encode("utf-8"), mtime=None)
        )
