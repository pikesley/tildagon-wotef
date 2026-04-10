def expand_frameset(frameset):
    """Turn it into a flat list."""
    flattened = []
    for frame, count in frameset:
        flattened.extend([frame] * (count + 1))
    return flattened
