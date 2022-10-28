# IMPORTS
import logging
import pandas as pd

# FUNCTIONS
def split_dataframe(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Splits input dataframe into two pandas.DataFrames according to column name.

    :param df: is the input dataframe

    :return: two pandas.DataFrames (donor DataFrame and recipient DataFrame)
    """
    return df.filter(regex='_D').copy(), df.filter(regex='_R').copy()


def _convert_to_epitopes(allele: str, df_ref: pd.DataFrame, suffix: str, interlocus2: bool) -> list[str]:
    """
    :param allele: allele to convert
    :param df_ref: reference pandas.DataFrame for the locus of the allele
    :param suffix: which locus the allele belongs to
    :param interlocus2: whether or not to take into account interlocus eplets for HLA of class II


    :return: list of epitopes corresponding the allele
    """

    epitope_list: list[str] = []
    for epitope in df_ref.loc[allele].values:
        if not pd.isnull(epitope):
            if epitope[0] in ["r", "q", "p"]:
                if interlocus2:
                    epitope_list.append(epitope)
            else:
                epitope_list.append(f"{epitope}_{suffix}")

    return epitope_list



def _allele_df_to_epitopes_df(df, df_a, df_b, df_c, df_dr, df_dq, df_dp, interlocus2: bool):
    """
    Extraction of the allele dataframe to transform it into an epitope dictionary

    :param df: is the input dataframe of the donor or the recipient
    :param df_a: reference dataframe HLA A
    :param df_b: reference dataframe HLA B
    :param df_c: reference dataframe HLA C
    :param df_dr: reference dataframe HLA DRB1
    :param df_dq: reference dataframe HLA DQB1
    :param df_dp: reference dataframe HLA DPB1
    :param interlocus2: whether or not to take into account interlocus eplets for HLA of class II
    """

    epitope_per_allele_dataframe: pd.DataFrame = df.applymap(
        lambda allele:
        _convert_to_epitopes(
            allele,
            df_a,
            "ABC",
            interlocus2
        )
        if allele[0] == "A"
        else (
            _convert_to_epitopes(
                allele,
                df_b,
                "ABC",
                interlocus2
            )
            if allele[0] == "B"
            else
            (
                _convert_to_epitopes(
                    allele,
                    df_c,
                    "ABC",
                    interlocus2
                )
                if allele[0] == "C"
                else
                (
                    _convert_to_epitopes(
                        allele,
                        df_dr,
                        "DR",
                        interlocus2
                    )
                    if allele[0:2] == "DR"
                    else
                    (
                        _convert_to_epitopes(
                            allele,
                            df_dq,
                            "DQ",
                            interlocus2
                        )
                        if allele[0:2] == "DQ"
                        else
                        (
                            _convert_to_epitopes(
                                allele,
                                df_dp,
                                "DP",
                                interlocus2
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
