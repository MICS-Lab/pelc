[![DOI](https://zenodo.org/badge/555576588.svg)](https://zenodo.org/badge/latestdoi/555576588)
[![Downloads](https://pepy.tech/badge/pelc)](https://pepy.tech/project/pelc)
# PELC (Python Eplet Load Calculator)

### Overview
PELC is a Python package designed to calculate efficiently the HLA Eplet Load (based on the
[EpRegistry database](https://www.epregistry.com.br/)) between donors and recipients by loading in a pandas.DataFrame
in `eplet_comparison.compute_epletic_load` the recipients' and donors' typings.  See minimal reproducible example for
more details.


### Getting started
#### Install from PyPI (recommended)
To use `pelc`, run `pip install pelc` in your terminal.


#### Usage

##### a. Comparing two alleles
Here is a minimal example of how to use `pelc` to compare two alleles:
```py
from pelc.simple_comparison import simple_comparison

simple_comparison(
    "A*68:01",
    "A*68:02",
    "output",  # file will be saved as output.csv in the current directory
    verifiedonly=False,  # if True, only verified eplets will be considered, otherwise all eplets will be considered
    interlocus2=True  # doesn't matter for class I alleles
)
```
In the `output.csv` file created in the current directory, you will find two rows: "In A&ast;68:02 but not in 
A&ast;68:01" and "In A&ast;68:01 but not in A&ast;68:02".

##### b. Batch mode
Here is a minimal example with the file [Template.xlsx](https://github.com/MICS-Lab/pelc/raw/main/Template.xlsx)
(click to download):
```py
import pandas as pd

from pelc import batch_eplet_comp, batch_eplet_comp_aux, output_type

if __name__ == "__main__":
    input_path: str = "Template.xlsx"

    output_path: str = "MyOutput"
    input_df: pd.DataFrame = pd.read_excel(
        input_path,
        sheet_name="My Sheet",
        index_col="Index"
    )

    donordf: pd.DataFrame
    recipientdf: pd.DataFrame
    donordf, recipientdf = batch_eplet_comp_aux.split_dataframe(input_df)

    batch_eplet_comp.compute_epletic_load(
        donordf,
        recipientdf,
        output_path,
        output_type.OutputType.DETAILS_AND_COUNT,
        class_i=True,  # Compute class I eplets comparison?
        class_ii=True,  # Compute class II eplets comparison?
        verifiedonly=False,  # How should the epletic charge be computed? Verified eplets only? Or all eplets?
        exclude=None,  # list of indices to exclude
        interlocus2=True  # whether or not to take into account interlocus eplets for HLA of class II
    )
```
Note that if a typing is unknown, one can use `A*`, `B*`, ..., `DPB1*` as the allele name for **both** recipients and
donors. If the allele is unknown for only of the two individuals, it is necessary to use `A*`, `B*`, ..., `DPB1*` for
both individuals otherwise the eplet mismatch computation will not be performed for this donor / recipient pair.

#### Advanced usage:
##### a. Not taking into account all loci (if they are not typed for example)
If one wants to determine the eplet mismatches between a donor and a recipient but without taking into account
a certain locus, one can use `A*`, `B*`, ..., `DPB1*` as the allele name for both recipients and donors on this locus
and the eplet mismatch computation will only take into account the loci filled in.

##### b. Not creating a file but generating a pandas.DataFrame
If one wants to generate a `pandas.DataFrame` directly, the `output_path` argument of `simple_comparison` can be 
set to `None`. The `pandas.DataFrame` will be returned by the function. Same goes for `compute_epletic_load`.


#### Exit codes:
```
- 55: an eplet did not match the regular expression '^\d+' (ABC, DR, DQ or DP) and it also did not match the regular
expression '^.[pqr]*(\d+)' (interlocus2) either.
```


#### Unit tests
Tested on `Python 3.10.2` & `Python 3.11.1`.
```
platform win32 -- Python 3.10.2, pytest-7.2.0, pluggy-1.0.0
plugins: anyio-3.6.2, mypy-0.10.3
collected 34 items

unit_tests_mypy.py ..                                                    [  5%]
unit_tests_simple.py .                                                   [  8%]
pelc\__init__.py .                                                       [ 11%]
pelc\_open_epregistry_databases.py .                                     [ 14%]
pelc\_unexpected_alleles.py .                                            [ 17%]
pelc\batch_eplet_comp.py .                                               [ 20%]
pelc\batch_eplet_comp_aux.py .                                           [ 23%]
pelc\output_type.py .                                                    [ 26%]
pelc\simple_comparison.py .                                              [ 29%]
tests\__init__.py .                                                      [ 32%]
tests\base_loading_for_tests.py .                                        [ 35%]
tests\test_eplet_mismatches.py .......                                   [ 55%]
tests\test_extract_key_to_rank_epletes.py ..                             [ 61%]
tests\test_is_valid_allele.py ..                                         [ 67%]
tests\test_pelc.py ..                                                    [ 73%]
tests\test_same_locus.py ..                                              [ 79%]
tests\test_simple_comparison.py .....                                    [ 94%]
tests\test_unexpected_alleles.py ..                                      [100%]
 =================================== mypy =====================================

Success: no issues found in 18 source files
 ============================= 34 passed in 16.23s ============================
```
```
platform win32 -- Python 3.11.1, pytest-7.2.0, pluggy-1.0.0
plugins: anyio-3.6.2, mypy-0.10.3
collected 34 items

unit_tests_mypy.py ..                                                    [  5%]
unit_tests_simple.py .                                                   [  8%]
pelc\__init__.py .                                                       [ 11%]
pelc\_open_epregistry_databases.py .                                     [ 14%]
pelc\_unexpected_alleles.py .                                            [ 17%]
pelc\batch_eplet_comp.py .                                               [ 20%]
pelc\batch_eplet_comp_aux.py .                                           [ 23%]
pelc\output_type.py .                                                    [ 26%]
pelc\simple_comparison.py .                                              [ 29%]
tests\__init__.py .                                                      [ 32%]
tests\base_loading_for_tests.py .                                        [ 35%]
tests\test_eplet_mismatches.py .......                                   [ 55%]
tests\test_extract_key_to_rank_epletes.py ..                             [ 61%]
tests\test_is_valid_allele.py ..                                         [ 67%]
tests\test_pelc.py ..                                                    [ 73%]
tests\test_same_locus.py ..                                              [ 79%]
tests\test_simple_comparison.py .....                                    [ 94%]
tests\test_unexpected_alleles.py ..                                      [100%]
 =================================== mypy =====================================

Success: no issues found in 18 source files
 ============================= 34 passed in 14.95s ============================
```



### About the source code
- Follows [PEP8](https://peps.python.org/pep-0008/) Style Guidelines.
- All functions are unit-tested with [pytest](https://docs.pytest.org/en/stable/).
- All variables are correctly type-hinted, reviewed with [static type checker](https://mypy.readthedocs.io/en/stable/)
`mypy`.
- All functions are documented with [docstrings](https://www.python.org/dev/peps/pep-0257/).



### Useful links:
- [Corresponding GitHub repository](https://github.com/MICS-Lab/pelc)
- [Corresponding PyPI page](https://pypi.org/project/pelc)



### Citation
If you use this software, please cite it as below.

- APA:
```
If you use this software, please cite it as below. 

Lhotte, R., Clichet, V., Usureau, C. & Taupin, J. (2022). 
Python Eplet Load Calculator (PELC) package (Version 0.5.0) [Computer software].
https://doi.org/10.5281/zenodo.7254809
```

- BibTeX:
```
@software{lhotte_romain_2022_7526198,
  author       = {Lhotte, Romain and
                  Clichet, Valentin and
                  Usureau, Cédric and
                  Taupin, Jean-Luc},
  title        = {Python Eplet Load Calculator},
  month        = oct,
  year         = 2022,
  publisher    = {Zenodo},
  version      = {0.5.0},
  doi          = {10.5281/zenodo.7526198},
}
```
