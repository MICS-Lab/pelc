import os
import pandas as pd

from pelc.batch_eplet_comp import compute_epletic_load
from pelc.output_type import OutputType
from tests.base_loading_for_tests import base_loading


def test_unexpected_alleles() -> None:
    # No exclude
    donordf, recipientdf, output_path = base_loading("pytest.xlsx", "False Negs")

    compute_epletic_load(
        donordf,
        recipientdf,
        output_path,
        OutputType.FILTERED_OUT_TYPINGS,
        True,
        True,
        False,
    )

    removed_donors_no_exclude: pd.DataFrame = pd.read_csv(f"{output_path}_removed_donors.csv")
    removed_recipients_no_exclude: pd.DataFrame = pd.read_csv(f"{output_path}_removed_recipients.csv")

    assert (len(removed_donors_no_exclude) == 1)
    assert (len(removed_recipients_no_exclude) == 0)

    os.remove(f"{output_path}_removed_donors.csv")
    os.remove(f"{output_path}_removed_recipients.csv")

    # With exclude
    compute_epletic_load(
        donordf,
        recipientdf,
        output_path,
        OutputType.FILTERED_OUT_TYPINGS,
        True,
        True,
        False,
        False,
        [4]
    )

    removed_donors_exclude: pd.DataFrame = pd.read_csv(f"{output_path}_removed_donors.csv")
    removed_recipients_exclude: pd.DataFrame = pd.read_csv(f"{output_path}_removed_recipients.csv")

    assert (len(removed_donors_exclude) == 0)
    assert (len(removed_recipients_exclude) == 0)

    os.remove(f"{output_path}_removed_donors.csv")
    os.remove(f"{output_path}_removed_recipients.csv")
