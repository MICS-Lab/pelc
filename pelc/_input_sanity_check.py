import pandas as pd


def _equal_amount_of_unknown_alleles(
    input_df_donor: pd.DataFrame, input_df_recipient: pd.DataFrame
) -> bool:
    """
    :param input_df_donor: Input pandas.DataFrame with the donor alleles
    :param input_df_recipient: Input pandas.DataFrame with the recipient alleles

    :return: True if the amount of unknown alleles is equal in both dataframes, False otherwise

    Also tests if the unknown alleles are either for both the alleles of the locus or for none of them
    """

    unknown_alleles: list[str] = [
        "A*",
        "B*",
        "C*",
        "DRB1*",
        # No DRB345 because it is ok for them to have Nops
        "DQA1*",
        "DQB1*",
        "DPA1*",
        "DPB1*",
    ]

    # Check if the amount of unknown alleles is equal in both dataframes
    for (_, row_d), (_, row_r) in zip(
        input_df_donor.iterrows(), input_df_recipient.iterrows()
    ):
        allele: str
        for allele in unknown_alleles:
            locus: str = allele[:-1]
            locus_donor_1: str = f"{locus}1_D"
            locus_donor_2: str = f"{locus}2_D"
            locus_recipient_1: str = f"{locus}1_R"
            locus_recipient_2: str = f"{locus}2_R"

            if allele in [row_d[locus_donor_1], row_d[locus_donor_2]]:
                if not (
                    allele
                    ==
                    row_r[locus_recipient_1]
                    ==
                    row_r[locus_recipient_2]
                    ==
                    row_d[locus_donor_1]
                    ==
                    row_d[locus_donor_2]
                ):
                    return False

    return True
