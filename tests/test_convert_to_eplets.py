import os
import pandas as pd

from pelc.batch_eplet_comp_aux import _convert_to_eplets  # noqa
from pelc._open_epregistry_databases import (  # noqa
    _open_ep_data,  # noqa
    _open_epregistry_database,  # noqa
)


def test_convert_to_eplets_dqa1() -> None:
    """
    Test the _convert_to_eplets function on some DQA1 alleles.
    :return: Nothing
    """
    this_file_directory_path: str = os.path.dirname(os.path.realpath(__file__))
    df_ref: pd.DataFrame = _open_epregistry_database(
        f"{this_file_directory_path}{os.sep}..{os.sep}pelc{os.sep}data{os.sep}DQ.csv",
        ["DQB1*", "DQA1*"],
    )
    df_data: pd.DataFrame = _open_ep_data(
        f"{this_file_directory_path}{os.sep}..{os.sep}pelc"
    )
    expected_list: list[str] = [
        "2D_DQ",
        "25YT_DQ",
        "40GR_DQ",
        "61FT_DQ",
        "66IL_DQ",
        "75S_DQ",
        "76L_DQ",
        "129H_DQ",
        "160A_DQ"
    ]

    output_list_dqa05_01: list[str] = _convert_to_eplets(
        "DQA1*05:01", df_ref, "DQ", df_data, False, False
    )
    assert sorted(output_list_dqa05_01) == sorted(expected_list)

    output_list_dqa05_05: list[str] = _convert_to_eplets(
        "DQA1*05:05", df_ref, "DQ", df_data, False, False
    )
    assert sorted(output_list_dqa05_05) == sorted(expected_list)

def test_convert_to_eplets_dqb1() -> None:
    """
    Test the _convert_to_eplets function on a DQB1 allele.
    :return: Nothing
    """
    this_file_directory_path: str = os.path.dirname(os.path.realpath(__file__))
    df_ref: pd.DataFrame = _open_epregistry_database(
        f"{this_file_directory_path}{os.sep}..{os.sep}pelc{os.sep}data{os.sep}DQ.csv",
        ["DQB1*", "DQA1*"],
    )
    df_data: pd.DataFrame = _open_ep_data(
        f"{this_file_directory_path}{os.sep}..{os.sep}pelc"
    )

    output_list_dqb1_02_01: list[str] = _convert_to_eplets(
        "DQB1*02:01", df_ref, "DQ", df_data, False, False
    )
    assert "2D_DQ" not in output_list_dqb1_02_01
    assert "3S_DQ" in output_list_dqb1_02_01

def test_convert_to_eplets_rare_c() -> None:
    """
    Test the _convert_to_eplets function on a rare C allele.
    :return: Nothing
    """
    this_file_directory_path: str = os.path.dirname(os.path.realpath(__file__))
    df_ref: pd.DataFrame = _open_epregistry_database(
        f"{this_file_directory_path}{os.sep}..{os.sep}pelc{os.sep}data{os.sep}C.csv",
        ["C*"],
    )
    df_data: pd.DataFrame = _open_ep_data(
        f"{this_file_directory_path}{os.sep}..{os.sep}pelc"
    )

    output_list_c_18_24: list[str] = _convert_to_eplets(
        "C*18:24", df_ref, "ABC", df_data, False, False
    )
    assert "1C_ABC" in output_list_c_18_24
    assert "9F_ABC" not in output_list_c_18_24

def test_convert_to_eplets_questionable() -> None:
    """
    Test the `include_questionable` argument of the _convert_to_eplets function.
    :return: Nothing
    """
    this_file_directory_path: str = os.path.dirname(os.path.realpath(__file__))
    df_ref: pd.DataFrame = _open_epregistry_database(
        f"{this_file_directory_path}{os.sep}..{os.sep}pelc{os.sep}data{os.sep}DQ.csv",
        ["DQB1*", "DQA1*"],
    )
    df_data: pd.DataFrame = _open_ep_data(
        f"{this_file_directory_path}{os.sep}..{os.sep}pelc"
    )

    output_list_dqa03_02_all: list[str] = _convert_to_eplets(
        "DQA1*03:02", df_ref, "DQ", df_data, False, False, False
    )
    assert "160D_DQ" in output_list_dqa03_02_all

    output_list_dqa03_02_verified_only_no_questionable: list[str] = _convert_to_eplets(
        "DQA1*03:02", df_ref, "DQ", df_data, False, True, False
    )
    assert "160D_DQ" not in output_list_dqa03_02_verified_only_no_questionable

    output_list_dqa03_02_verified_only_questionable_too: list[str] = _convert_to_eplets(
        "DQA1*03:02", df_ref, "DQ", df_data, False, False, False
    )
    assert "160D_DQ" in output_list_dqa03_02_verified_only_questionable_too

    assert (
            len(output_list_dqa03_02_all)
            >=
            len(output_list_dqa03_02_verified_only_questionable_too)
            >=
            len(output_list_dqa03_02_verified_only_no_questionable)
    )
