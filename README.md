# PECC (Python Epitopic Charge Calculator)

### Overview



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
```
```



### About the source code
- Follows [PEP8](https://peps.python.org/pep-0008/) Style Guidelines.
- All variables are correctly type-hinted, reviewed with [static type checker](https://mypy.readthedocs.io/en/stable/)
`mypy`.



### Useful links:
- [Corresponding GitHub repository](https://github.com/MICS-Lab/pecc)
- [Corresponding PyPI page]()



### Citation
If you use this software, please cite it as below.

- APA:
```
Lhotte, R., Usureau, C., & Taupin, J. (2022). Python Epitope Charge Calculator (Version 0.2.0) [Computer software].
https://doi.org/doi.org/10.5281/zenodo.7254809
```

- BibTeX:
```
@software{Lhotte_Python_Epitope_Charge_2022,
author = {Lhotte, Romain and Usureau, Cédric and Taupin, Jean-Luc},
doi = {doi.org/10.5281/zenodo.7254809},
month = {10},
title = {{Python Epitope Charge Calculator}},
version = {0.2.0},
year = {2022}
}
```

### References
