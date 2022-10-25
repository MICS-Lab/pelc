import os
import pandas as pd

from pecc.epitope_comparison import compute_epitopic_charge
from pecc.output_type import OutputType
from tests.base_loading_for_tests import base_loading


def test_unexpected_alleles() -> None:
    # No exclude
    donordf, recipientdf, output_path = base_loading("False Negs")

    compute_epitopic_charge(
        donordf,
        recipientdf,
        output_path,
        OutputType.FILTERED_OUT_TYPINGS,
        True,
        True,
        False,
    )

    removed_donors: pd.DataFrame = pd.read_csv(f"{output_path}_removed_donors.csv")
    removed_recipients: pd.DataFrame = pd.read_csv(f"{output_path}_removed_recipients.csv")

    assert (len(removed_donors) == 1)
    assert (len(removed_recipients) == 0)

    os.remove(f"{output_path}_removed_donors.csv")
    os.remove(f"{output_path}_removed_recipients.csv")

    # With exclude
    compute_epitopic_charge(
        donordf,
        recipientdf,
        output_path,
        OutputType.FILTERED_OUT_TYPINGS,
        True,
        True,
        False,
        [4]
    )

    removed_donors: pd.DataFrame = pd.read_csv(f"{output_path}_removed_donors.csv")
    removed_recipients: pd.DataFrame = pd.read_csv(f"{output_path}_removed_recipients.csv")

    assert (len(removed_donors) == 0)
    assert (len(removed_recipients) == 0)

    os.remove(f"{output_path}_removed_donors.csv")
    os.remove(f"{output_path}_removed_recipients.csv")
