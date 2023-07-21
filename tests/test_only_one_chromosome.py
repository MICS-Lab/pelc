import os
import pandas as pd
import pytest

from pelc.batch_eplet_comp import compute_epletic_load
from pelc.output_type import OutputType
from tests.base_loading_for_tests import base_loading

def test_one_chromosome() -> None:
    """
    Test the epletic load calculation with only one chromosome. If only one chromosome is present, it has to be
    the first one, and it will mean it's a homozygote. Otherwise, _equal_amount_of_unknown_alleles will return False
    and compute_epletic_load will return None. No file will then be created.
    :return: None
    """

    # OK
    donordf, recipientdf, output_path = base_loading("pytest_only_one_chromosome_ok.xlsx", "Sheet 1")

    for class_1 in False, True:
        compute_epletic_load(
            donordf,
            recipientdf,
            output_path,
            OutputType.DETAILS_AND_COUNT,
            class_1,  # class_i
            True,  # class_ii
            False,  # abv_only
        )

        output_df: pd.DataFrame = pd.read_csv(f"{output_path}.csv", index_col="Index")

        assert output_df.at[8, "EpMismatches"] == "160S_DQ"
        assert output_df.at[8, "Eplet Load"] == 1

        os.remove(f"{output_path}.csv")

    # NOT OK
    donordf, recipientdf, output_path = base_loading("pytest_only_one_chromosome_not_ok.xlsx", "Sheet 1")

    for class_1 in False, True:
        # Make sure this raises a ValueError
        with pytest.raises(ValueError):
            compute_epletic_load(
                donordf,
                recipientdf,
                output_path,
                OutputType.DETAILS_AND_COUNT,
                class_1,  # class_i
                True,  # class_ii
                False,  # abv_only
            )

    # NOT OK2
    donordf, recipientdf, output_path = base_loading("pytest_only_one_chromosome_not_ok_2.xlsx", "Sheet 1")

    for class_1 in False, True:
        # Make sure this raises a ValueError
        with pytest.raises(ValueError):
            compute_epletic_load(
                donordf,
                recipientdf,
                output_path,
                OutputType.DETAILS_AND_COUNT,
                class_1,  # class_i
                True,  # class_ii
                False,  # abv_only
            )
