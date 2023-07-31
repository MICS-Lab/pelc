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
        verifiedonly=False,
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
        verifiedonly=True,
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
            verifiedonly=False,
            interlocus2=True
        )


def test_wrong_allele_simple_comparison() -> None:
    # Check that the function raises a ValueError when one or several alleles are not in the correct format
    with pytest.raises(ValueError):
        simple_comparison(
            "A68:01",
            "DQB1*03:02",
            "tests/pytest_a68_simple_comparison_no_abv",
            verifiedonly=False,
            interlocus2=True
        )


def test_returning_dataframe() -> None:
    # Check that the function returns a dataframe
    simple_comparaison_return = simple_comparison(
        "A*68:01",
        "A*68:02",
        None,
        verifiedonly=False,
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
            verifiedonly=False,
            interlocus2=True
        )
