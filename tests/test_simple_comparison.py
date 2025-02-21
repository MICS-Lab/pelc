import numpy as np
import os
import pandas as pd
import pytest

from pelc.simple_comparison import simple_comparison


def in_a6802_but_not_in_a6801(df: pd.DataFrame) -> None:
    assert (len(df) == 2)

    assert ("12M" in df.loc["In A*68:02 but not in A*68:01"]["EpMismatches"])
    assert ("97R" in df.loc["In A*68:02 but not in A*68:01"]["EpMismatches"])
    assert ("114H" in df.loc["In A*68:02 but not in A*68:01"]["EpMismatches"])
    assert ("116Y" in df.loc["In A*68:02 but not in A*68:01"]["EpMismatches"])


def test_simple_comparison_a68() -> None:
    # All eplets
    simple_comparison(
        "A*68:01",
        "A*68:02",
        "tests/pytest_a68_simple_comparison_no_abv",
        verified_only=False,
        interlocus2=True
    )

    pytest_a68_simple_comparison_no_abv = pd.read_csv(
        "tests/pytest_a68_simple_comparison_no_abv.csv"
    )
    pytest_a68_simple_comparison_no_abv.set_index("Unnamed: 0", inplace=True)

    in_a6802_but_not_in_a6801(pytest_a68_simple_comparison_no_abv)

    # Antibody verified only
    simple_comparison(
        "A*68:01",
        "A*68:02",
        "tests/pytest_a68_simple_comparison_abv",
        verified_only=True,
        interlocus2=True
    )

    pytest_a68_simple_comparison_abv = pd.read_csv(
        "tests/pytest_a68_simple_comparison_abv.csv"
    )
    pytest_a68_simple_comparison_abv.set_index("Unnamed: 0", inplace=True)

    assert (len(pytest_a68_simple_comparison_abv) == 2)

    assert (pytest_a68_simple_comparison_abv.loc["In A*68:01 but not in A*68:02"]["Eplet Load"] == 0)
    assert (pytest_a68_simple_comparison_abv.loc["In A*68:02 but not in A*68:01"]["Eplet Load"] == 0)

    # delete files
    os.remove("tests/pytest_a68_simple_comparison_no_abv.csv")
    os.remove("tests/pytest_a68_simple_comparison_abv.csv")


def test_wrong_locus_simple_comparison() -> None:
    # Check that the function raises a ValueError when the loci are different
    with pytest.raises(ValueError):
        simple_comparison(
            "A*68:01",
            "DQB1*03:02",
            "tests/pytest_a68_simple_comparison_no_abv",
            verified_only=False,
            interlocus2=True
        )


def test_wrong_allele_simple_comparison() -> None:
    # Check that the function raises a ValueError when one or several alleles are not in the correct format
    with pytest.raises(ValueError):
        simple_comparison(
            "A68:01",
            "DQB1*03:02",
            "tests/pytest_a68_simple_comparison_no_abv",
            verified_only=False,
            interlocus2=True
        )


def test_returning_dataframe() -> None:
    # Check that the function returns a dataframe
    simple_comparaison_return = simple_comparison(
        "A*68:01",
        "A*68:02",
        None,
        verified_only=False,
        interlocus2=True
    )

    assert (isinstance(simple_comparaison_return, pd.DataFrame))

    in_a6802_but_not_in_a6801(simple_comparaison_return)


def test_empty_allele_simple_comparison() -> None:
    # Check that the function raises a ValueError when a ghost allele is provided
    with pytest.raises(ValueError):
        simple_comparison(
            "A*01:01",
            "A*",
            "output",
            verified_only=False,
            interlocus2=True
        )


def test_simple_comparison_175E() -> None:
    # Antibody Verified no Questionable
    simple_comparison(
        "DQA1*06:01",
        "DQA1*05:01",
        "tests/pytest_175E_simple_comparison_abv",
        verified_only=True,
        include_questionable=False,
        interlocus2=True
    )

    pytest_175E_simple_comparison_abv = pd.read_csv(
        "tests/pytest_175E_simple_comparison_abv.csv"
    )
    pytest_175E_simple_comparison_abv.set_index("Unnamed: 0", inplace=True)

    assert (len(pytest_175E_simple_comparison_abv) == 2)
    assert (
            np.isnan(
                pytest_175E_simple_comparison_abv.loc[
                    "In DQA1*05:01 but not in DQA1*06:01"
                ]["EpMismatches"]
            )
    )
    # There are no Antibody Verified Eplets in DQA1*05:01 that are not in DQA1*06:01 (only 75S but 75S is
    # questionable)
    assert (
            "175E" not in pytest_175E_simple_comparison_abv.loc[
                "In DQA1*06:01 but not in DQA1*05:01"
            ]["EpMismatches"]
    )

    # Antibody Verified no Questionable
    simple_comparison(
        "DQA1*06:01",
        "DQA1*05:01",
        "tests/pytest_175E_simple_comparison_abv_questionable",
        verified_only=True,
        include_questionable=True,
        interlocus2=True
    )

    pytest_175E_simple_comparison_abv_questionable = pd.read_csv(
        "tests/pytest_175E_simple_comparison_abv_questionable.csv"
    )
    pytest_175E_simple_comparison_abv_questionable.set_index("Unnamed: 0", inplace=True)

    assert (len(pytest_175E_simple_comparison_abv_questionable) == 2)
    assert (
            "175E" not in pytest_175E_simple_comparison_abv_questionable.loc[
                "In DQA1*05:01 but not in DQA1*06:01"
            ]["EpMismatches"]
    )
    assert (
            "75S" in pytest_175E_simple_comparison_abv_questionable.loc[
                "In DQA1*05:01 but not in DQA1*06:01"
            ]["EpMismatches"]
    )
    assert (
            "175E" in pytest_175E_simple_comparison_abv_questionable.loc[
                "In DQA1*06:01 but not in DQA1*05:01"
            ]["EpMismatches"]
    )

    # delete files
    os.remove("tests/pytest_175E_simple_comparison_abv.csv")
    os.remove("tests/pytest_175E_simple_comparison_abv_questionable.csv")
