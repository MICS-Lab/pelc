[![DOI](https://zenodo.org/badge/555576588.svg)](https://zenodo.org/badge/latestdoi/555576588)
[![Downloads](https://pepy.tech/badge/pecc)](https://pepy.tech/project/pecc)
# PECC (Python Epitopic Charge Calculator)

### Overview
PECC is a Python package designed to calculate efficiently the HLA Epitopic Charge (based on the
[EpRegistry database](https://www.epregistry.com.br/)) between donors and recipients by loading in a pandas.DataFrame
in `epitope_comparison.compute_epitopic_charge`.  See minimal reproducible example for more details.


### Getting started
#### Install from PyPI (recommended)
To use `pecc`, run `pip install pecc` in your terminal.


#### Usage
Here is a minimal example with the file [Template.xlsx](https://github.com/MICS-Lab/pecc/raw/main/Template.xlsx) (click to download):
```py
import pandas as pd

from pecc import epitope_comparison, epitope_comparison_aux, output_type


if __name__ == "__main__":
    input_path: str = "Template.xlsx"

    output_path: str = "MyOutput"
    input_df: pd.DataFrame = pd.read_excel(
        input_path, sheet_name="My Sheet", index_col="Index"
    )

    donordf: pd.DataFrame
    recipientdf: pd.DataFrame
    donordf, recipientdf = epitope_comparison_aux.split_dataframe(input_df)

    epitope_comparison.compute_epitopic_charge(
        donordf,
        recipientdf,
        output_path,
        output_type.OutputType.DETAILS_AND_COUNT
    )
```

#### Exit codes:
```
None yet.
```


#### Unit tests
Tested on `Python 3.10.2` & `Python 3.11.0`.
```
platform win32 -- Python 3.10.2, pytest-7.2.0, pluggy-1.0.0
rootdir: C:\Users\lhott\Documents\Formation scolaire\These\Travail\pecc
plugins: mypy-0.10.0
collected 19 items                                                                                                                                     

unit_tests_mypy.py ..                                                               [ 10%]
unit_tests_simple.py .                                                              [ 15%] 
pecc\__init__.py .                                                                  [ 21%] 
pecc\_unexpected_alleles.py .                                                       [ 26%] 
pecc\epitope_comparison.py .                                                        [ 31%] 
pecc\epitope_comparison_aux.py .                                                    [ 36%] 
pecc\output_type.py .                                                               [ 42%] 
tests\__init__.py .                                                                 [ 47%] 
tests\base_loading_for_tests.py .                                                   [ 52%] 
tests\test_epitope_mismatches.py ......                                             [ 78%]
tests\test_pecc.py ..                                                               [ 89%] 
tests\test_unexpected_alleles.py ..                                                 [100%]
```
```
platform win32 -- Python 3.11.0, pytest-7.2.0, pluggy-1.0.0
plugins: mypy-0.10.0
collected 19 items

unit_tests_mypy.py ..                                                               [ 10%]
unit_tests_simple.py .                                                              [ 15%]
pecc\__init__.py .                                                                  [ 21%]
pecc\_unexpected_alleles.py .                                                       [ 26%]
pecc\epitope_comparison.py .                                                        [ 31%]
pecc\epitope_comparison_aux.py .                                                    [ 36%]
pecc\output_type.py .                                                               [ 42%]
tests\__init__.py .                                                                 [ 47%]
tests\base_loading_for_tests.py .                                                   [ 52%]
tests\test_epitope_mismatches.py ......                                             [ 78%]
tests\test_pecc.py ..                                                               [ 89%]
tests\test_unexpected_alleles.py ..                                                 [100%]
```



### About the source code
- Follows [PEP8](https://peps.python.org/pep-0008/) Style Guidelines.
- All functions are unit-tested with [pytest](https://docs.pytest.org/en/stable/).
- All variables are correctly type-hinted, reviewed with [static type checker](https://mypy.readthedocs.io/en/stable/)
`mypy`.
- All functions are documented with [docstrings](https://www.python.org/dev/peps/pep-0257/).



### Useful links:
- [Corresponding GitHub repository](https://github.com/MICS-Lab/pecc)
- [Corresponding PyPI page](https://pypi.org/project/pecc)



### Citation
If you use this software, please cite it as below.

- APA:
```
Lhotte, R., Usureau, C., & Taupin, J. (2022). Python Epitope Charge Calculator (Version 0.2.4) [Computer software].
https://doi.org/10.5281/zenodo.7254809
```

- BibTeX:
```
@software{Lhotte_Python_Epitope_Charge_2022,
    author = {Lhotte, Romain and Usureau, Cédric and Taupin, Jean-Luc},
    doi = {doi.org/10.5281/zenodo.7254809},
    month = {10},
    title = {{Python Epitope Charge Calculator}},
    version = {0.2.4},
    year = {2022}
}
```
