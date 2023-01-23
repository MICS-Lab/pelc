import os
import pandas as pd

from pelc.simple_comparison import simple_comparison

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

    assert (len(pytest_a68_simple_comparison_no_abv) == 2)
    assert ("12M" in pytest_a68_simple_comparison_no_abv.loc["In A*68:02 but not in A*68:01"]["EpMismatches"])
    assert ("97R" in pytest_a68_simple_comparison_no_abv.loc["In A*68:02 but not in A*68:01"]["EpMismatches"])
    assert ("114H" in pytest_a68_simple_comparison_no_abv.loc["In A*68:02 but not in A*68:01"]["EpMismatches"])
    assert ("116Y" in pytest_a68_simple_comparison_no_abv.loc["In A*68:02 but not in A*68:01"]["EpMismatches"])

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
