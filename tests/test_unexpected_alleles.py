import pandas as pd
import os

from pecc.epitope_comparison_aux import split_dataframe
from pecc.epitope_comparison import compute_epitopic_charge
from pecc.output_type import OutputType


def test_unexpected_alleles() -> None:
    this_file_directory_path: str = os.path.dirname(os.path.realpath(__file__))

    input_path: str = f"{this_file_directory_path}/pytest.xlsx"
    # with extension because we are going to directly open it with pd.read_excel
    output_path: str = f"{this_file_directory_path}/output_pytest"
    # no extension because pecc.compute_epitopic_charge corresponding argument should not have an extension

    input_df: pd.DataFrame = pd.read_excel(
        input_path, sheet_name=0, skiprows=[0], index_col="Index"
    )

    donordf: pd.DataFrame
    recipientdf: pd.DataFrame
    donordf, recipientdf = split_dataframe(input_df)

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
