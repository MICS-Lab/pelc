import pecc.epitope_comparison_aux


def test_extract_key_to_rank_eplets() -> None:
    # interlocus2 eplets
    assert 1037 == pecc.epitope_comparison_aux._extract_key_to_rank_eplets("rqp37YA")
    assert 1140 == pecc.epitope_comparison_aux._extract_key_to_rank_eplets("rq140TV")

    # ABC, DR, DQ or DP eplets
    assert 8 == pecc.epitope_comparison_aux._extract_key_to_rank_eplets("8L")
    assert 35 == pecc.epitope_comparison_aux._extract_key_to_rank_eplets("35FV")
