from tools.encoder import (
    encode_block,
    encode_line,
    scale_encode_block,
    scale_encode_line,
)


def test_line_encode():
    """Test."""
    assert encode_line([1, 1, 1]) == [[0, 3]]
    assert encode_line([0, 0, 0, 1, 1, 1]) == [[3, 3]]
    assert encode_line([1, 1, 1, 0, 0, 0, 1, 1, 1]) == [[0, 3], [6, 3]]
    assert encode_line([1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0]) == [[0, 3], [6, 3]]


def test_block_encode():
    """Test."""
    fixture = [[0, 0, 0, 1, 1, 1, 0, 0, 0]]
    assert encode_block(fixture) == [[3, 3, 0]]

    fixture = [
        [1, 1, 1, 0, 0, 0, 1, 1, 1],
        [0, 0, 0, 1, 1, 1, 1, 1, 1],
        [1, 0, 1, 1, 1, 0, 0, 1, 0],
    ]
    assert encode_block(fixture) == [
        [0, 3, 0],
        [6, 3, 0],
        [3, 6, 1],
        [0, 1, 2],
        [2, 3, 2],
        [7, 1, 2],
    ]


def test_scaled_encoded_line():
    """Test."""
    assert scale_encode_line([1, 1], scale=1) == [[-1, 2]]
    assert scale_encode_line([1, 1, 1, 1], scale=1) == [[-2, 4]]

    assert scale_encode_line([1, 0, 0, 1], scale=1) == [[-2, 1], [1, 1]]
    assert scale_encode_line([1, 0, 0, 1], scale=2) == [[-4, 2], [2, 2]]


def test_scaled_endoded_block():
    """Test."""
    fixture = [
        [1, 0, 0, 1],
        [1, 0, 0, 1],
    ]

    assert scale_encode_block(fixture, scale=1) == [
        [-2, 1, -1],
        [1, 1, -1],
        [-2, 1, 0],
        [1, 1, 0],
    ]

    assert scale_encode_block(fixture, scale=2) == [
        [-4, 2, -2],
        [2, 2, -2],
        [-4, 2, 0],
        [2, 2, 0],
    ]
