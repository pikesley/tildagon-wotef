from tools.encoder import encode_line


def test_line_encode():
    """Test."""
    assert encode_line("111") == [(0, 3)]
    assert encode_line("000111") == [(3, 3)]
    assert encode_line("111000111") == [(0, 3), (6, 3)]
