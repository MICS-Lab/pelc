import os
import pandas as pd

from pelc.batch_eplet_comp_aux import split_dataframe


def base_loading(file_name: str, sheet_name: str) -> tuple[pd.DataFrame, pd.DataFrame, str]:
    """
    :param file_name: with extension (.xlsx file)
    :param sheet_name: sheet_name of the excel file

    :return: two pandas dataframes (cf. split_dataframe) and the output path directory of the file without the extension
             because pelc.compute_epletic_load corresponding argument should not have an extension
    """
    this_file_directory_path: str = os.path.dirname(os.path.realpath(__file__))

    input_path: str = f"{this_file_directory_path}/{file_name}"
    # with extension because we are going to directly open it with pd.read_excel
    output_path: str = f"{this_file_directory_path}/output_pytest"
    # no extension because pelc.compute_epletic_load corresponding argument should not have an extension

    input_df: pd.DataFrame = pd.read_excel(
        input_path, sheet_name=sheet_name, skiprows=[0], index_col=0
    )

    donordf: pd.DataFrame
    recipientdf: pd.DataFrame
    donordf, recipientdf = split_dataframe(input_df)

    return donordf, recipientdf, output_path
