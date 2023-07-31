import pandas as pd

from pelc.simple_comparison import simple_comparison
from pelc.batch_eplet_comp_aux import _replace_null_alleles


def test_replace_null_alleles() -> None:
    data = {
        'A1_R': ['A*01:04N', 'A*01:15N'],
        'A2_R': ['A*02:01', 'A*02:01'],
        'C1_R': ['C*01:224N', 'C*02:38N'],
        'C2_R': ['C*04:01', 'C*04:09N'],
    }
    input_df_recipient = pd.DataFrame(data)
    _replace_null_alleles(input_df_recipient)

    expected_data = {
        'A1_R': ['A*', 'A*'],
        'A2_R': ['A*02:01', 'A*02:01'],
        'C1_R': ['C*', 'C*'],
        'C2_R': ['C*04:01', 'C*'],
    }
    expected_df_recipient = pd.DataFrame(expected_data)

    assert input_df_recipient.equals(expected_df_recipient)


def test_null_allele() -> None:
    simple_comparison(
        "A*01:01",
        "A*01:15N",
        "output",
        verifiedonly=False,
        interlocus2=True
    )

    # Open output.csv
    output_df = pd.read_csv("output.csv")

    # Check that there are two rows, with index "In A*01:01 but not in A*01:15N" and "In A*01:15N but not in A*01:01"
    assert output_df.shape[0] == 2
    assert output_df.iloc[0, 0] == "In A*01:01 but not in A*01:15N"
    assert output_df.iloc[1, 0] == "In A*01:15N but not in A*01:01"

    # Make sure there are 35 eplets in the first row and 0 in the second
    assert output_df.iloc[0, 1] == 35
    assert output_df.iloc[1, 1] == 0
