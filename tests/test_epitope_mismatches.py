import os
import pandas as pd

from pecc.epitope_comparison import compute_epitopic_charge
from pecc.output_type import OutputType
from tests.base_loading_for_tests import base_loading


def test_epitope_comparison_details() -> None:
    ## False Positives
    donordf, recipientdf, output_path = base_loading("False Pos")

    compute_epitopic_charge(
        donordf,
        recipientdf,
        output_path,
        OutputType.ONLY_DETAILS,
        True,
        True,
        False,
    )

    output_df: pd.DataFrame = pd.read_csv(f"{output_path}.csv", index_col="Index")

    assert output_df.at[1, "EpMismatches"] == "None"

    os.remove(f"{output_path}.csv")


    ## False Negatives
    donordf, recipientdf, output_path = base_loading("False Negs")

    compute_epitopic_charge(
        donordf,
        recipientdf,
        output_path,
        OutputType.ONLY_DETAILS,
        True,
        True,
        False,
    )

    output_df: pd.DataFrame = pd.read_csv(f"{output_path}.csv", index_col="Index")

    for index_ in range(5, 2146):
        assert output_df.at[index_, "EpMismatches"] == "None"

    list_mismatches: list[str] = output_df.at[1, "EpMismatches"].split(", ")
    assert ("rq26Y" in list_mismatches)
    # rq26Y is in DQB1*03:01 but not in DQB1*03:02 (can be checked by aligning the sequences on
    # https://www.ebi.ac.uk/ipd/imgt/hla/alignment/)
    # The prediction does not output rq26Y although it should
    # rq26Y is therefore a false negative
    assert ("rqp37YA" not in list_mismatches)
    # Both have this eplet
    assert ("rp37FV" not in list_mismatches)
    # The mismatch is a DQ mismatch and this is a DR / DP eplet

    os.remove(f"{output_path}.csv")


def test_epitope_comparison_count() -> None:
    donordf, recipientdf, output_path = base_loading("False Negs")

    compute_epitopic_charge(
        donordf,
        recipientdf,
        output_path,
        OutputType.COUNT,
        True,
        True,
        False,
    )

    output_df: pd.DataFrame = pd.read_csv(f"{output_path}.csv", index_col="Index")

    for index_ in range(5, 2146):
        assert output_df.at[index_, "Epitopic Charge"] == 0

    os.remove(f"{output_path}.csv")
