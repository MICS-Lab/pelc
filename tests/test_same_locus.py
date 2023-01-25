from pelc.simple_comparison import _same_locus

def test_same_locus() -> None:
    assert _same_locus("A*01:01", "A*68:01") is True
    assert _same_locus("A*01:01", "B*07:02") is False
    assert _same_locus("DRB1*01:01", "DRB3*01:01") is True
    assert _same_locus("DRB1*01:01", "DRB5*01:01") is True
