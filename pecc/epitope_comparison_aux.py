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


def is_epitope_to_be_added(
        epitope: str,
        suffix: str,
        df_data: pd.DataFrame,
        verifiedonly: bool = False
) -> bool:
    locus_det: str
    if epitope[0] in ["r", "q", "p"]:
        locus_det = "i2"
    else:
        locus_det = suffix
    return (
        not verifiedonly
        or
        df_data[
            (df_data["eplet"] == epitope)
            &
            (df_data["locus"] == locus_det)
        ]["confirmation"].item() == "Yes"
    )



def _convert_to_epitopes(
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
    :param df_data: reference pandas.DataFrame with details about the eplets
    :param interlocus2: whether or not to take into account interlocus eplets for HLA of class II
    :param verifiedonly: whether or not to take into account only verified eplets

    :return: list of epitopes corresponding the allele
    """

    epitope_list: list[str] = []
    for epitope in df_ref.loc[allele].values:
        if not pd.isnull(epitope):
            if is_epitope_to_be_added(epitope, suffix, df_data, verifiedonly):
                if epitope[0] in ["r", "q", "p"]:
                    if interlocus2:
                        epitope_list.append(epitope)
                else:
                    epitope_list.append(f"{epitope}_{suffix}")

    return epitope_list



def _allele_df_to_epitopes_df(
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
    Transformation of the allele dataframe (index - alleles) into an epitope dataframe (index - epitopes)

    :param df: is the input dataframe of the donor or the recipient
    :param df_a: reference dataframe HLA A
    :param df_b: reference dataframe HLA B
    :param df_c: reference dataframe HLA C
    :param df_dr: reference dataframe HLA DRB1
    :param df_dq: reference dataframe HLA DQB1
    :param df_dp: reference dataframe HLA DPB1
    :param df_data: reference pandas.DataFrame with details about the eplets
    :param interlocus2: whether or not to take into account interlocus eplets for HLA of class II
    :param verifiedonly: whether or not to take into account only verified eplets

    :return: pd.DataFrame with epitopes for each patient, for each locus
    """

    epitope_per_allele_dataframe: pd.DataFrame = df.applymap(
        lambda allele:
        _convert_to_epitopes(
            allele,
            df_a,
            "ABC",
            df_data,
            interlocus2,
            verifiedonly
        )
        if allele[0] == "A"
        else (
            _convert_to_epitopes(
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
                _convert_to_epitopes(
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
                    _convert_to_epitopes(
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
                        _convert_to_epitopes(
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
                            _convert_to_epitopes(
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
    # epitope content of its allele.

    return epitope_per_allele_dataframe


def _extract_key_to_rank_eplets(eplet: str) -> float:
    """
    :param eplet: e.g. "9Y" or "26L"
    :return: the position but as a float so that sorting ain't gonna be done alphanumerically (9 or 26)

    If interlocus eplet, then return float('inf')
    """
    starts_with_number = re.search(r"^\d+", eplet)
    if starts_with_number:
        number = int(starts_with_number.group())
        return number
    else:
        return float('inf')  # inf will guarantee this comes last


def _transform_epitope_charge_detail(epitope_charge_detail: pd.Series) -> pd.Series:
    """
    :param epitope_charge_detail: pd.Series with the epitope charge details
    :return: pd.Series with the epitope charge details sorted
    """
    epitope_charge_detail = epitope_charge_detail.apply(list)
    epitope_charge_detail = epitope_charge_detail.apply(
        lambda list_: sorted(
            list_,
            key=_extract_key_to_rank_eplets
        )
    )
    epitope_charge_detail = epitope_charge_detail.astype(str)
    epitope_charge_detail = (
        epitope_charge_detail.replace("[]", "None")  # no regex no need to escape
        .replace("\\[", "", regex=True)
        .replace("\\]", "", regex=True)
        .replace("'", "", regex=True)
    )

    return epitope_charge_detail
