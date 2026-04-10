from lib.expand_frameset import expand_frameset


def test_expand_framset():
    """Test."""
    fixture = [["e39e", 0], ["b688", 0], ["8c11", 3], ["b688", 0]]
    assert expand_frameset(fixture) == [
        "e39e",
        "b688",
        "8c11",
        "8c11",
        "8c11",
        "8c11",
        "b688",
    ]
