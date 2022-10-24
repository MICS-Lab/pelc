# IMPORTS
import logging
import os
import pandas as pd

from pecc.epitope_comparison_aux import allele_df_to_epitopes_df
from pecc.output_type import OutputType
from pecc.unexpected_alleles import delete_unexpected_alleles, remove_unexpected_other_individual


# MAIN
def compute_epitopic_charge(
    input_df_donor: pd.DataFrame,
    input_df_recipient: pd.DataFrame,
    output_path: str,
    output_type: OutputType,
    class_i: bool = True,
    class_ii: bool = True,
    verifiedonly: bool = False,
) -> None:
    """
    :param input_df_donor: Input Donors Typing pandas.DataFrame
    :param input_df_recipient: Input Recipients Typing pandas.DataFrame
    :param output_path: Output path without the extension
    :param output_type: What is gonna be in the output file
    :param class_i: Compute class I epitopes comparison?
    :param class_ii: Compute class II epitopes comparison?
    :param verifiedonly: How should the peitopic charge be computed Verified epitopes only? Or all epitopes?

    :return: None
    """
    if not class_i and not class_ii:
        logging.error(
            "User did not request class I epitope comparison nor did they request class II epitope comparison."
        )

    df_a: pd.DataFrame | None
    df_b: pd.DataFrame | None
    df_c: pd.DataFrame | None
    df_dr: pd.DataFrame | None
    df_dq: pd.DataFrame | None
    df_dp: pd.DataFrame | None
    df_data: pd.DataFrame
    """
    df_data sums up the properties of each amino acid
    """

    this_file_directory_path: str = os.path.dirname(os.path.realpath(__file__))
    if class_i:
        df_a = pd.read_csv(f"{this_file_directory_path}/data/A.csv").set_index("allele")
        df_b = pd.read_csv(f"{this_file_directory_path}/data/B.csv").set_index("allele")
        df_c = pd.read_csv(f"{this_file_directory_path}/data/C.csv").set_index("allele")
    else:
        # we don't want to load .csv files if they are not needed
        df_a, df_b, df_c = None, None, None
    if class_ii:
        df_dr = pd.read_csv(f"{this_file_directory_path}/data/DR.csv").set_index("allele")
        df_dq = pd.read_csv(f"{this_file_directory_path}/data/DQ.csv").set_index("allele")
        df_dp = pd.read_csv(f"{this_file_directory_path}/data/DP.csv").set_index("allele")
    else:
        # we don't want to load .csv files if they are not needed
        df_dr, df_dq, df_dp = None, None, None
    df_data = pd.read_csv(f"{this_file_directory_path}/data/ep_data.csv")

    input_df_donor, removed_donors = delete_unexpected_alleles(
        input_df_donor, df_a, df_b, df_c, df_dr, df_dq, df_dp
    )
    input_df_recipient, removed_recipients = delete_unexpected_alleles(
        input_df_recipient, df_a, df_b, df_c, df_dr, df_dq, df_dp
    )

    if output_type == OutputType.FILTERED_OUT_TYPINGS:
        removed_donors.to_csv(f"{output_path}_removed_donors.csv")
        removed_recipients.to_csv(f"{output_path}_removed_recipients.csv")
    else:
        input_df_donor, input_df_recipient = remove_unexpected_other_individual(input_df_donor, input_df_recipient)

        donors_epitopes_per_allele: pd.DataFrame = allele_df_to_epitopes_df(
            input_df_donor, df_a, df_b, df_c, df_dr, df_dq, df_dp
        )
        recipients_epitopes_per_allele: pd.DataFrame = allele_df_to_epitopes_df(
            input_df_recipient, df_a, df_b, df_c, df_dr, df_dq, df_dp
        )

        # Concatenate all loci
        donor_all_epitopes: pd.Series = donors_epitopes_per_allele.sum(axis=1).rename("Donors' epitopes")
        recipient_all_epitopes: pd.Series = recipients_epitopes_per_allele.sum(axis=1).rename("Recipients' epitopes")

        # Eliminate epitope doublons
        donor_all_epitopes = donor_all_epitopes.apply(set)
        recipient_all_epitopes = recipient_all_epitopes.apply(set)

        # Return epitopes that are present on the donor's HLA molecules but not on the recipient's ones
        both_all_epitopes: pd.DataFrame = pd.concat(
            [donor_all_epitopes, recipient_all_epitopes],
            axis=1
        )

        epitope_charge_detail: pd.Series = (
                both_all_epitopes["Donors' epitopes"] - both_all_epitopes["Recipients' epitopes"]
        ).rename("Epitopic Charge")
        if output_type == OutputType.DETAILS_AND_COUNT or output_type == OutputType.COUNT:
            epitope_charge: pd.Series = epitope_charge_detail.apply(len)
            if output_type == OutputType.DETAILS_AND_COUNT:
                epitope_charge_detail = epitope_charge_detail.astype(str)
                epitope_charge_detail = (
                    epitope_charge_detail.replace("set()", "None")
                                         .replace("{", "", regex=True)
                                         .replace("}", "", regex=True)
                                         .replace("'", "", regex=True)
                )
                pd.concat(
                    [epitope_charge, epitope_charge_detail],
                    axis=1
                ).to_csv(f"{output_path}.csv")
            else:  # OutputType.COUNT
                epitope_charge.to_csv(f"{output_path}.csv")
        elif output_type == OutputType.ONLY_DETAILS:
            epitope_charge_detail = epitope_charge_detail.astype(str)
            epitope_charge_detail = (
                epitope_charge_detail.replace("set()", "None")
                                     .replace("{", "", regex=True)
                                     .replace("}", "", regex=True)
                                     .replace("'", "", regex=True)
            )
            epitope_charge_detail.to_csv(f"{output_path}.csv")
