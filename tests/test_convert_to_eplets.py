import os
import pandas as pd

from pelc.batch_eplet_comp_aux import _convert_to_eplets  # noqa
from pelc._open_epregistry_databases import (  # noqa
    open_ep_data,
    _open_epregistry_database,  # noqa
)


def test_convert_to_eplets() -> None:
    """
    Test the _convert_to_eplets function.
    :return: Nothing
    """
    this_file_directory_path: str = os.path.dirname(os.path.realpath(__file__))
    df_ref: pd.DataFrame = _open_epregistry_database(
        f"{this_file_directory_path}{os.sep}..{os.sep}pelc{os.sep}data{os.sep}DQ.csv",
        ["DQB1*", "DQA1*"],
    )
    df_data: pd.DataFrame = open_ep_data(
        f"{this_file_directory_path}{os.sep}..{os.sep}pelc"
    )
    expected_list: list[str] = [
        "2D_DQ",
        "25YT_DQ",
        "40GR_DQ",
        "55R_DQ",
        "61FT_DQ",
        "66IL_DQ",
        "75S_DQ",
        "76L_DQ",
        "129H_DQ",
        "160A_DQ",
        "185I_DQ",
    ]
    output_list: list[str] = _convert_to_eplets(
        "DQA1*05:01", df_ref, "DQ", df_data, False, False
    )
    assert sorted(output_list) == sorted(expected_list)
