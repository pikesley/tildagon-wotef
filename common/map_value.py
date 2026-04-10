# https://stackoverflow.com/a/76115938
from random import random


def map_value(value, start_a, stop_a, start_b=120, stop_b=-120):
    """`map` from `p5js`."""
    return (value - start_a) / (stop_a - start_a) * (stop_b - start_b) + start_b


def scaled_random(lower, upper):
    """Scaled random number."""
    return map_value(random(), 0, 1, lower, upper)
