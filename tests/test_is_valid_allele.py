from pelc.simple_comparison import _is_valid_allele

def test_is_valid_allele() -> None:
    assert _is_valid_allele("A*01:01") is True
    assert _is_valid_allele("A*01") is False
    assert _is_valid_allele("A01:01") is False
