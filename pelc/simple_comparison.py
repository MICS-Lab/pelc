import pandas as pd

from pelc.output_type import OutputType
from pelc.batch_eplet_comp import compute_epletic_load


def _is_valid_allele(allele: str) -> bool:
    """
    :param allele: allele to check
    :return: whether or not the allele is valid
    """
    return "*" in allele and ":" in allele


def _same_locus(allele1: str, allele2: str) -> bool:
    """
    :param allele1: First allele to compare
    :param allele2: Second allele to compare

    :return: whether or not the alleles are of the same locus
    """
    prefix_allele1 = allele1.split("*")[0]
    prefix_allele2 = allele2.split("*")[0]
    if prefix_allele1 == prefix_allele2:
        # A*01:01 and A*68:01 are of the same locus
        return True
    else:
        if "DRB" in prefix_allele1 and "DRB" in prefix_allele2:
            # DRB1*01:01 and DRB3*01:01 are of the same locus
            return True
        else:
            # A*01:01 and B*07:02 are not of the same locus
            return False


def simple_comparison(
        allele1: str,
        allele2: str,
        output_path: str | None,
        verifiedonly: bool = False,
        interlocus2: bool = True
) -> None | pd.DataFrame:
    """
    :param allele1: First allele to compare
    :param allele2: Second allele to compare
    :param output_path: Output path without the extension. If None, the output will be returned as a pandas.DataFrame.
    :param verifiedonly: How should the epletic charge be computed? Verified eplets only? Or all eplets?
    :param interlocus2: whether or not to take into account interlocus eplets (only relevant for HLA of class II)

    :return: None or a pandas.DataFrame with the results according to output_path
    """

    # Check if the alleles are valid
    if not _is_valid_allele(allele1) or not _is_valid_allele(allele2):
        raise ValueError("The alleles are not valid")
    else:
        # Check if the alleles are of the same locus
        if not _same_locus(allele1, allele2):
            raise ValueError("The alleles are not of the same locus")
        else:
            # Create a pandas DataFrame with the two alleles
            input_df_donor = pd.DataFrame(
                data={
                    "Donor": [allele1, allele2]
                },
                index=[
                    f"In {allele1} but not in {allele2}",
                    f"In {allele2} but not in {allele1}"
                ]
            )
            input_df_recipient = pd.DataFrame(
                data={
                    "Recipient": [allele2, allele1]
                },
                index=[
                    f"In {allele1} but not in {allele2}",
                    f"In {allele2} but not in {allele1}"
                ]
            )

            # Compute the epletic load
            return compute_epletic_load(  # type: ignore # we know that the output is a pandas.DataFrame or None
                input_df_donor,
                input_df_recipient,
                output_path,
                OutputType.DETAILS_AND_COUNT,
                verifiedonly=verifiedonly,
                interlocus2=interlocus2,
                simple_comparison=True
            )
