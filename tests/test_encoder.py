from tools.encoder import encode_block, encode_line, scale_encode_line


def test_line_encode():
    """Test."""
    assert encode_line("111") == [[0, 3]]
    assert encode_line("000111") == [[3, 3]]
    assert encode_line("111000111") == [[0, 3], [6, 3]]
    assert encode_line("111000111000") == [[0, 3], [6, 3]]


def test_block_encode():
    """Test."""
    fixture = """000111000"""
    assert encode_block(fixture) == [[3, 3, 0]]

    fixture = """111000111
000111111
101110010"""
    assert encode_block(fixture) == [
        [0, 3, 0],
        [6, 3, 0],
        [3, 6, 1],
        [0, 1, 2],
        [2, 3, 2],
        [7, 1, 2],
    ]


def test_scaled_encode_line():
    """Test."""
    assert scale_encode_line("11", scale=1) == [[-1, 2]]
    assert scale_encode_line("1111", scale=1) == [[-2, 4]]
