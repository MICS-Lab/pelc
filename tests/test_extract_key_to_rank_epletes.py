import pecc.epitope_comparison_aux


def test_extract_key_to_rank_eplets() -> None:
    assert 1037 == pecc.epitope_comparison_aux._extract_key_to_rank_eplets("rqp37YA")
    assert 1140 == pecc.epitope_comparison_aux._extract_key_to_rank_eplets("rq140TV")
    assert 8 == pecc.epitope_comparison_aux._extract_key_to_rank_eplets("8L")
    assert 35 == pecc.epitope_comparison_aux._extract_key_to_rank_eplets("35FV")
