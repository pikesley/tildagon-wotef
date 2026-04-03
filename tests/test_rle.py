from tools.rle import run_length_encode


def test_easy_case():
    """Test."""
    assert run_length_encode("aaa") == [("a", 3)]
    assert run_length_encode("aaabbb") == [("a", 3), ("b", 3)]
    assert run_length_encode("aaabbbccc") == [("a", 3), ("b", 3), ("c", 3)]
    assert run_length_encode("aaabbbcccaaaa") == [
        ("a", 3),
        ("b", 3),
        ("c", 3),
        ("a", 4),
    ]
