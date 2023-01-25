import logging
import pandas as pd


def read_available_alleles(df_ref: pd.DataFrame) -> list[str]:
    """
    :param df_ref: reference dataframe
    :return: all known alleles in the reference dataframe (df_a, df_b, df_c, df_dr, df_dq, or df_dp)
    """
    list_ref: list[str] = list(df_ref.index.values)

    return list_ref


def delete_unexpected_alleles(
    df: pd.DataFrame,
    df_a: pd.DataFrame | None,
    df_b: pd.DataFrame | None,
    df_c: pd.DataFrame | None,
    df_dr: pd.DataFrame | None,
    df_dq: pd.DataFrame | None,
    df_dp: pd.DataFrame | None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    :param df: is the input dataframe of the donor or the recipient
    :param df_a: reference dataframe HLA A
    :param df_b: reference dataframe HLA B
    :param df_c: reference dataframe HLA C
    :param df_dr: reference dataframe HLA DRB1
    :param df_dq: reference dataframe HLA DQB1
    :param df_dp: reference dataframe HLA DPB1

    :return: df without the lines with unexpected alleles, df with only the lines with unexpected alleles
    """
    list_ref_a: list[str]  = read_available_alleles(df_a)
    list_ref_b: list[str]  = read_available_alleles(df_b)
    list_ref_c: list[str]  = read_available_alleles(df_c)
    list_ref_dr: list[str] = read_available_alleles(df_dr)
    list_ref_dq: list[str] = read_available_alleles(df_dq)
    list_ref_dp: list[str] = read_available_alleles(df_dp)

    list_ref: set[str] = set(
        list_ref_a + list_ref_b + list_ref_c + list_ref_dr + list_ref_dq + list_ref_dp
    )

    is_allowed: pd.Series = df.isin(list_ref).all(axis=1)

    df_filtered = df[is_allowed]
    df_removed  = df[~is_allowed]

    if len(df_removed) != 0:
        logging.warning(
            "Some alleles inputed by the user were not found in the EpRegistry database. "
            "They will be removed."
        )

    return df_filtered, df_removed


def remove_unexpected_other_individual(
    input_df_donor: pd.DataFrame,
    input_df_recipient: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    :param input_df_donor: Filtered Donor Dataframe
    :param input_df_recipient: Filtered Recipient Dataframe

    :return: those two filtered dataframes but further filtered (with only rows that weren't excluded in the other df)
    """
    input_df_donor = input_df_donor[input_df_donor.index.isin(input_df_recipient.index)]
    input_df_recipient = input_df_recipient[input_df_recipient.index.isin(input_df_donor.index)]

    return input_df_donor, input_df_recipient
