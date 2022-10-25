import os
import pandas as pd

from pecc._epitope_comparison_aux import split_dataframe


def base_loading(sheet_name: str) -> tuple[pd.DataFrame, pd.DataFrame, str]:
    this_file_directory_path: str = os.path.dirname(os.path.realpath(__file__))

    input_path: str = f"{this_file_directory_path}/pytest.xlsx"
    # with extension because we are going to directly open it with pd.read_excel
    output_path: str = f"{this_file_directory_path}/output_pytest"
    # no extension because pecc.compute_epitopic_charge corresponding argument should not have an extension

    input_df: pd.DataFrame = pd.read_excel(
        input_path, sheet_name=sheet_name, skiprows=[0], index_col="Index"
    )

    donordf: pd.DataFrame
    recipientdf: pd.DataFrame
    donordf, recipientdf = split_dataframe(input_df)

    return donordf, recipientdf, output_path
