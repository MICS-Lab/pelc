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
In the `output.csv` file created in the current directory, you will find two rows: "In A\*68:02 but not in A\*68:01" and
"In A\*68:01 but not in A\*68:02"

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
Tested on `Python 3.10.2` & `Python 3.11.0`.
```
platform win32 -- Python 3.10.2, pytest-7.2.0, pluggy-1.0.0
plugins: mypy-0.10.0
collected 19 items                                                                                                                                     

unit_tests_mypy.py ..                                                               [ 10%]
unit_tests_simple.py .                                                              [ 15%] 
pelc\__init__.py .                                                                  [ 21%] 
pelc\_unexpected_alleles.py .                                                       [ 26%] 
pelc\epitope_comparison.py .                                                        [ 31%] 
pelc\epitope_comparison_aux.py .                                                    [ 36%] 
pelc\output_type.py .                                                               [ 42%] 
tests\__init__.py .                                                                 [ 47%] 
tests\base_loading_for_tests.py .                                                   [ 52%] 
tests\test_epitope_mismatches.py ......                                             [ 78%]
tests\test_pelc.py ..                                                               [ 89%] 
tests\test_unexpected_alleles.py ..                                                 [100%]
```
```
platform win32 -- Python 3.11.0, pytest-7.2.0, pluggy-1.0.0
plugins: mypy-0.10.0
collected 19 items

unit_tests_mypy.py ..                                                               [ 10%]
unit_tests_simple.py .                                                              [ 15%]
pelc\__init__.py .                                                                  [ 21%]
pelc\_unexpected_alleles.py .                                                       [ 26%]
pelc\epitope_comparison.py .                                                        [ 31%]
pelc\epitope_comparison_aux.py .                                                    [ 36%]
pelc\output_type.py .                                                               [ 42%]
tests\__init__.py .                                                                 [ 47%]
tests\base_loading_for_tests.py .                                                   [ 52%]
tests\test_epitope_mismatches.py ......                                             [ 78%]
tests\test_pelc.py ..                                                               [ 89%]
tests\test_unexpected_alleles.py ..                                                 [100%]
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
If you use this software, please cite it as below. Lhotte, R., Clichet, V., Usureau, C. & Taupin, J. (2022). 
Python Eplet Load Calculator (PELC) package (Version 0.4.1) [Computer software]. https://doi.org/10.5281/zenodo.7254809
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
  version      = {0.4.1},
  doi          = {10.5281/zenodo.7526198},
}
```
