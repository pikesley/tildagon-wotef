import gzip
from pathlib import Path

import yaml

local_conf = yaml.safe_load(Path("conf.yaml").read_text(encoding="utf-8"))


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
            if current == 1:
                result.append([start_index, count])
            current = char
            count = 1
            start_index = index

    if current == 1:
        result.append([start_index, count])

    return result


def scale_encode_line(line, scale):
    """Encode with scale and offset."""
    return [[(e[0] - len(line) / 2) * scale, e[1] * scale] for e in encode_line(line)]


def encode_block(block):
    """Encode a block of text."""
    result = []

    for index, line in enumerate(block):
        result.extend([x + [index] for x in encode_line(line)])

    return result


def scale_encode_block(block, scale):
    """Scale-encode a block of text."""
    scaled_lines = [scale_encode_line(line, scale=scale) for line in block]
    result = []
    offset = len(scaled_lines) / 2

    for index, line in enumerate(scaled_lines):
        result.extend([item + [(index - offset) * scale] for item in line])

    return result


def encode(block, scale):
    """Encode."""
    return scale_encode_block(block, scale)


if __name__ == "__main__":
    import json
    from pathlib import Path

    from conf import pre_render_conf, root

    highest = 0
    lowest = 0

    frames = {}
    for frame in Path(root, "slimmed").glob("*"):
        data = json.loads(frame.read_text(encoding="utf-8"))
        encoded = encode(data, pre_render_conf["scale"])
        frames[frame.stem] = encoded

        tops = [i[-1] for i in encoded]
        lowest = max(lowest, *tops)
        highest = min(highest, *tops)

    Path(root, "frames.json.gz").write_bytes(
        gzip.compress(
            json.dumps(frames, separators=(",", ":")).encode("utf-8"), mtime=0
        )
    )

    Path(root, "frames.json").write_text(json.dumps(frames, indent=2))

    render_config = {
        "scale": pre_render_conf["scale"],
        "min-y": highest,
        "max-y": lowest,
    }

    Path(root, "config.json.gz").write_bytes(
        gzip.compress(
            json.dumps(render_config, separators=(",", ":")).encode("utf-8"), mtime=0
        )
    )
    Path(root, "config.json").write_text(json.dumps(render_config, indent=2))
