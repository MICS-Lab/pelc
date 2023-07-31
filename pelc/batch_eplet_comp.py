# IMPORTS
import csv
import logging
import os
import pandas as pd

from pelc._input_sanity_check import _equal_amount_of_unknown_alleles
from pelc._open_epregistry_databases import (
    _open_epregistry_database,
    open_ep_data,
)
from pelc._unexpected_alleles import (
    _delete_unexpected_alleles,
    _remove_unexpected_other_individual,
)
from pelc.batch_eplet_comp_aux import (
    _allele_df_to_eplets_df,
    _replace_null_alleles,
    _transform_eplet_load_detail,
)
from pelc.output_type import OutputType


# MAIN
def compute_epletic_load(
    input_df_donor: pd.DataFrame,
    input_df_recipient: pd.DataFrame,
    output_path: str | None,
    output_type: OutputType,
    class_i: bool = True,
    class_ii: bool = True,
    verifiedonly: bool = False,
    exclude: list[int | str] | None = None,
    interlocus2: bool = True,
    simple_comparison: bool = False,
) -> None | pd.DataFrame | pd.Series | tuple[pd.DataFrame, pd.DataFrame]:
    """
    :param input_df_donor: Input Donors Typing (pandas.DataFrame)
    :param input_df_recipient: Input Recipients Typing (pandas.DataFrame)
    :param output_path: Output path without the extension. If None, the output will be returned as a pandas.DataFrame.
    :param output_type: What is gonna be in the output file
    :param class_i: Compute class I eplets comparison?
    :param class_ii: Compute class II eplets comparison?
    :param verifiedonly: How should the epletic charge be computed? Verified eplets only? Or all eplets?
    :param exclude: list of indices to exclude
    :param interlocus2: whether or not to take into account interlocus eplets for HLA of class II
    :param simple_comparison: whether or not it's a simple allele to allele comparison in which case, the function
    _equal_amount_of_unknown_alleles is not called (checks are already made in simple_comparison.py and would not
    pass here given the column names).

    :return: None (if output_type is not None, the result will be saved on disk as a csv), or pandas.DataFrame
             (OutputType.COUNT_AND_DETAILS) or pandas.Series (OutputType.COUNT, or OutputType.ONLY_DETAILS) or
             tuple[pandas.DataFrame, pandas.DataFrame] (OutputType.FILTERED_TYPINGS)

    :raises ValueError: if the number of unknown alleles is different for one donor and recipient pair or one allele is
                        unknown whilst the other of the same locus isn't. Obviously doesn't raise anything if user
                        inputs a homozygous like this: donor: A*01:01 A* and recipient: A*01:01 A*11:01.
    """
    if not class_i and not class_ii:
        logging.error(
            "User did not request class I eplet comparison nor did they request class II eplet comparison."
        )

    if exclude is not None:
        input_df_donor.drop(exclude, axis=0, inplace=True)
        input_df_recipient.drop(exclude, axis=0, inplace=True)

    if len(input_df_donor) != len(input_df_recipient):
        logging.error(
            "The number of donors is different from the number of recipients."
        )
        return None

    if not simple_comparison:
        if not _equal_amount_of_unknown_alleles(input_df_donor, input_df_recipient):
            # unknown alleles are the ones that were inputted as "A*", "B*", "C*", "DRB1*", "DRB345*", "DQA1*", "DQB1*",
            # "DPA1*" and/or "DPB1*". Here we are not talking about the alleles that are unknown to the database.
            logging.error(
                "Either the number of unknown alleles is different for one donor and recipient pair or one allele is "
                "unknown whilst the other of the same locus isn't."
            )
            raise ValueError(
                "Either the number of unknown alleles is different for one donor and recipient pair or one allele is "
                "unknown whilst the other of the same locus isn't."
            )


    df_a: pd.DataFrame
    df_b: pd.DataFrame
    df_c: pd.DataFrame
    df_dr: pd.DataFrame
    df_dq: pd.DataFrame
    df_dp: pd.DataFrame
    df_data: pd.DataFrame
    """
    df_data sums up the properties of each amino acid
    """

    this_file_directory_path: str = os.path.dirname(os.path.realpath(__file__))
    if class_i and class_ii:
        df_a = _open_epregistry_database(f"{this_file_directory_path}/data/A.csv", ["A*"])
        df_b = _open_epregistry_database(f"{this_file_directory_path}/data/B.csv", ["B*"])
        df_c = _open_epregistry_database(f"{this_file_directory_path}/data/C.csv", ["C*"])
        df_dr = _open_epregistry_database(f"{this_file_directory_path}/data/DR.csv", ["DRB1*", "DRB345*"])
        df_dq = _open_epregistry_database(f"{this_file_directory_path}/data/DQ.csv", ["DQB1*", "DQA1*"])
        df_dp = _open_epregistry_database(f"{this_file_directory_path}/data/DP.csv", ["DPB1*", "DPA1*"])
    else:
        if class_i:
            df_a = _open_epregistry_database(f"{this_file_directory_path}/data/A.csv", ["A*"])
            df_b = _open_epregistry_database(f"{this_file_directory_path}/data/B.csv", ["B*"])
            df_c = _open_epregistry_database(f"{this_file_directory_path}/data/C.csv", ["C*"])
            # we don't want to load .csv files if they are not needed
            df_dr = _open_epregistry_database(
                f"{this_file_directory_path}/data/DR.csv", ["DRB1*", "DRB345*"], no_eplets=True
            )
            df_dq = _open_epregistry_database(
                f"{this_file_directory_path}/data/DQ.csv", ["DQB1*", "DQA1*"], no_eplets=True
            )
            df_dp = _open_epregistry_database(
                f"{this_file_directory_path}/data/DP.csv", ["DPB1*", "DPA1*"], no_eplets=True
            )
        else:
            df_dr = _open_epregistry_database(f"{this_file_directory_path}/data/DR.csv", ["DRB1*", "DRB345*"])
            df_dq = _open_epregistry_database(f"{this_file_directory_path}/data/DQ.csv", ["DQB1*", "DQA1*"])
            df_dp = _open_epregistry_database(f"{this_file_directory_path}/data/DP.csv", ["DPB1*", "DPA1*"])
            # we don't want to load .csv files if they are not needed
            df_a = _open_epregistry_database(
                f"{this_file_directory_path}/data/A.csv", ["A*"], no_eplets=True
            )
            df_b = _open_epregistry_database(
                f"{this_file_directory_path}/data/B.csv", ["B*"], no_eplets=True
            )
            df_c = _open_epregistry_database(
                f"{this_file_directory_path}/data/C.csv", ["C*"], no_eplets=True
            )


    df_data = open_ep_data(this_file_directory_path)

    # Replace Null alleles with ghost alleles in input_df_donors and input_df_recipients
    _replace_null_alleles(input_df_donor)
    _replace_null_alleles(input_df_recipient)

    # Delete unexpected alleles (those who are not found in the EpRegistry database)
    input_df_donor, removed_donors = _delete_unexpected_alleles(
        input_df_donor, df_a, df_b, df_c, df_dr, df_dq, df_dp
    )
    input_df_recipient, removed_recipients = _delete_unexpected_alleles(
        input_df_recipient, df_a, df_b, df_c, df_dr, df_dq, df_dp
    )

    if len(removed_donors) + len(removed_recipients) > 0:
        logging.warning(
            "Some alleles inputted by the user were not found in the EpRegistry database. "
            "They will be removed. "
            "To find out what typings were removed, please run compute_epletic_load with the output_type argument "
            "set to OutputType.FILTERED_TYPINGS."
        )

    if output_type == OutputType.FILTERED_OUT_TYPINGS:
        if output_path is None:
            return removed_donors, removed_recipients
        else:
            removed_donors.to_csv(f"{output_path}_removed_donors.csv")
            removed_recipients.to_csv(f"{output_path}_removed_recipients.csv")
    else:
        input_df_donor, input_df_recipient = _remove_unexpected_other_individual(input_df_donor, input_df_recipient)

        donors_eplets_per_allele: pd.DataFrame = _allele_df_to_eplets_df(
            input_df_donor, df_a, df_b, df_c, df_dr, df_dq, df_dp, df_data, interlocus2, verifiedonly
        )
        recipients_eplets_per_allele: pd.DataFrame = _allele_df_to_eplets_df(
            input_df_recipient, df_a, df_b, df_c, df_dr, df_dq, df_dp, df_data, interlocus2, verifiedonly
        )

        # Concatenate all loci
        donor_all_eplets: pd.Series = donors_eplets_per_allele.sum(axis=1).rename("Donors' eplets")
        recipient_all_eplets: pd.Series = recipients_eplets_per_allele.sum(axis=1).rename("Recipients' eplets")

        # Eliminate eplet doublons
        donor_all_eplets = donor_all_eplets.apply(lambda x: set(x))
        recipient_all_eplets = recipient_all_eplets.apply(lambda x: set(x))

        # Return eplets that are present on the donor's HLA molecules but not on the recipient's ones
        both_all_eplets: pd.DataFrame = pd.concat(
            [donor_all_eplets, recipient_all_eplets],
            axis=1
        )

        eplet_load_detail: pd.Series = (
                both_all_eplets["Donors' eplets"] - both_all_eplets["Recipients' eplets"]
        ).rename("EpMismatches")
        if output_type == OutputType.DETAILS_AND_COUNT or output_type == OutputType.COUNT:
            eplet_load: pd.Series = eplet_load_detail.apply(len).rename("Eplet Load")
            if output_type == OutputType.DETAILS_AND_COUNT:
                eplet_load_detail = _transform_eplet_load_detail(eplet_load_detail)
                eplet_load_and_detail = pd.concat(
                    [eplet_load, eplet_load_detail],
                    axis=1
                )
                if output_path is None:
                    return eplet_load_and_detail
                else:
                    eplet_load_and_detail.to_csv(f"{output_path}.csv", quoting=csv.QUOTE_NONNUMERIC)
            else:  # OutputType.COUNT
                if output_path is None:
                    return eplet_load
                else:
                    eplet_load.to_csv(f"{output_path}.csv")
        elif output_type == OutputType.ONLY_DETAILS:
            eplet_load_detail = _transform_eplet_load_detail(eplet_load_detail)
            if output_path is None:
                return eplet_load_detail
            else:
                eplet_load_detail.to_csv(f"{output_path}.csv", quoting=csv.QUOTE_NONNUMERIC)

    return None
