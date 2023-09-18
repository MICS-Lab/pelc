import pelc.batch_eplet_comp_aux


def test_extract_key_to_rank_eplets() -> None:
    # interlocus2 eplets
    assert 1037 == pelc.batch_eplet_comp_aux._extract_key_to_rank_eplets("RQP37YA")
    assert 1140 == pelc.batch_eplet_comp_aux._extract_key_to_rank_eplets("RQ140TV")

    # ABC, DR, DQ or DP eplets
    assert 8 == pelc.batch_eplet_comp_aux._extract_key_to_rank_eplets("8L")
    assert 35 == pelc.batch_eplet_comp_aux._extract_key_to_rank_eplets("35FV")
