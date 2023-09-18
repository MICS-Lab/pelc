# IMPORTS
import logging
import pandas as pd
import re

# FUNCTIONS
def split_dataframe(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Splits input dataframe into two pandas.DataFrames according to column name.

    :param df: is the input dataframe

    :return: two pandas.DataFrames (donor DataFrame and recipient DataFrame)
    """
    return df.filter(regex='_D').copy(), df.filter(regex='_R').copy()


def _is_eplet_to_be_added(
        eplet: str,
        suffix: str,
        df_data: pd.DataFrame,
        verifiedonly: bool = False
) -> bool:
    """
    Checks whether the eplet should be added
    :param eplet: is it the correct eplet
    :param suffix: is it the correct gene (needed because for example 26L is a DR eplet but also a DQ eplet)
    :param df_data: reference pandas.DataFrame with details about the eplets
    :param verifiedonly: whether or not to take into account only verified eplets

    :return: whether or not the eplet should be added to the list of eplets
    """

    if not verifiedonly:
        # if verified only is False, then we don't care about the 'confirmation' column
        return True

    locus_det: str
    if eplet[0] in ["r", "q", "p"]:
        locus_det = "i2"
    else:
        locus_det = suffix

    return (
        df_data[
            (df_data["eplet"] == eplet)
            &
            (df_data["locus"] == locus_det)
        ]["confirmation"].item() == "Yes"
    )



def _convert_to_eplets(
        allele: str,
        df_ref: pd.DataFrame,
        suffix: str,
        df_data: pd.DataFrame,
        interlocus2: bool,
        verifiedonly: bool = False
) -> list[str]:
    """
    :param allele: allele to convert
    :param df_ref: reference pandas.DataFrame for the locus of the allele
    :param suffix: which locus the allele belongs to
    :param df_data: reference pandas.DataFrame with details about all the eplets (ep_data.csv)
    :param interlocus2: whether or not to take into account interlocus eplets for HLA of class II
    :param verifiedonly: whether or not to take into account only verified eplets

    :return: list of eplets corresponding the allele
    """

    eplet_list: list[str] = []
    for eplet in df_ref.loc[allele].values:
        if not pd.isnull(eplet):
            if _is_eplet_to_be_added(eplet, suffix, df_data, verifiedonly):
                if eplet[0] in ["r", "q", "p"]:
                    if interlocus2:
                        eplet_list.append(eplet)
                else:
                    eplet_list.append(f"{eplet}_{suffix}")

    return eplet_list



def _allele_df_to_eplets_df(
        df: pd.DataFrame,
        df_a: pd.DataFrame,
        df_b: pd.DataFrame,
        df_c: pd.DataFrame,
        df_dr: pd.DataFrame,
        df_dq: pd.DataFrame,
        df_dp: pd.DataFrame,
        df_data: pd.DataFrame,
        interlocus2: bool,
        verifiedonly: bool = False
) -> pd.DataFrame:
    """
    Transformation of the allele dataframe (index + alleles) into an eplet dataframe (index + eplets)

    :param df: is the input dataframe of the donor or the recipient
    :param df_a: reference dataframe HLA A
    :param df_b: reference dataframe HLA B
    :param df_c: reference dataframe HLA C
    :param df_dr: reference dataframe HLA DRB1
    :param df_dq: reference dataframe HLA DQB1
    :param df_dp: reference dataframe HLA DPB1
    :param df_data: reference pandas.DataFrame with details about all the eplets (ep_data.csv)
    :param interlocus2: whether or not to take into account interlocus eplets for HLA of class II
    :param verifiedonly: whether or not to take into account only verified eplets

    :return: pd.DataFrame with eplets for each patient, for each locus
    """

    eplets_per_allele_dataframe: pd.DataFrame = df.map(
        lambda allele:
        _convert_to_eplets(
            allele,
            df_a,
            "ABC",
            df_data,
            interlocus2,
            verifiedonly
        )
        if allele[0] == "A"
        else (
            _convert_to_eplets(
                allele,
                df_b,
                "ABC",
                df_data,
                interlocus2,
                verifiedonly
            )
            if allele[0] == "B"
            else
            (
                _convert_to_eplets(
                    allele,
                    df_c,
                    "ABC",
                    df_data,
                    interlocus2,
                    verifiedonly
                )
                if allele[0] == "C"
                else
                (
                    _convert_to_eplets(
                        allele,
                        df_dr,
                        "DR",
                        df_data,
                        interlocus2,
                        verifiedonly
                    )
                    if allele[0:2] == "DR"
                    else
                    (
                        _convert_to_eplets(
                            allele,
                            df_dq,
                            "DQ",
                            df_data,
                            interlocus2,
                            verifiedonly
                        )
                        if allele[0:2] == "DQ"
                        else
                        (
                            _convert_to_eplets(
                                allele,
                                df_dp,
                                "DP",
                                df_data,
                                interlocus2,
                                verifiedonly
                            )
                            if allele[0:2] == "DP"
                            else
                            (
                                logging.error(f"Allele {allele} belongs to an undefined locus")
                            )
                        )
                    )
                )
            )
        )
    )
    # Keep this dataframe in case we would want the user to be able to hover over one of the alleles and to get the
    # eplet content of its allele.

    return eplets_per_allele_dataframe


def _extract_key_to_rank_eplets(eplet: str) -> int:
    """
    :param eplet: e.g. "9Y" or "26L"
    :return: the position but as a float so that sorting ain't gonna be done alphanumerically (9 or 26)

    If interlocus eplet, then return 1000 + position (e.g. 1037 for rqp37YA)
    """
    starts_with_number = re.search(r"^\d+", eplet)
    if starts_with_number:
        number = int(starts_with_number.group())
        return number
    else:
        extract_number = re.search(r"^.[pqr]*(\d+)", eplet)
        if extract_number:
            return 1000 + int(extract_number.group(1))  # 1000 will guarantee this comes last
        else:
            logging.error(f"Eplet {eplet} does not have the expected format")
            exit(55)


def _transform_eplet_load_detail(eplet_load_detail: pd.Series) -> pd.Series:
    """
    :param eplet_load_detail: pd.Series with the eplet load details
    :return: pd.Series with the eplet load details sorted and cleaned up
    """
    eplet_load_detail = eplet_load_detail.apply(list)
    eplet_load_detail = eplet_load_detail.apply(
        lambda list_: sorted(
            list_,
            key=_extract_key_to_rank_eplets
        )
    )
    eplet_load_detail = eplet_load_detail.astype(str)
    eplet_load_detail = (
        eplet_load_detail.replace("[]", "None")  # no regex no need to escape
        .replace("\\[", "", regex=True)
        .replace("\\]", "", regex=True)
        .replace("'", "", regex=True)
    )

    return eplet_load_detail


def _replace_null_alleles(df: pd.DataFrame) -> None:
    """
    :param df: pd.DataFrame with the typing details
    :return: None, the dataframe is modified inplace
    """
    df.replace(
        r'^(.*\*).*N$',
        r"\1",
        regex=True,
        inplace=True
    )
