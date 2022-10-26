# PECC (Python Epitopic Charge Calculator)

### Overview



### Getting started
#### Install from PyPI (recommended)
To use `pecc`, run `pip install pecc` in your terminal.


#### Usage
Here is a minimal example with the file [Template.xlsx](https://github.com/MICS-Lab/pecc/raw/main/Template.xlsx) (click to download):
```py
import pandas as pd
import pecc


if __name__ == "__main__":
    input_path: str = "Template.xlsx"

    output_path: str
    for output_path, sheet_name in zip(
        [f"{input_path[:-5]}_pecc_fn", f"{input_path[:-5]}_pecc_fp"],
        ["False Negatives", "False Positives"],
    ):
        class_: str
        for class_ in ["CL1", "CL2", "all"]:
            input_df: pd.DataFrame = pd.read_excel(
                input_path, sheet_name=sheet_name, skiprows=[0], index_col="Index"
            )

            donordf: pd.DataFrame
            recipientdf: pd.DataFrame
            donordf, recipientdf = pecc.epitope_comparison_aux.split_dataframe(input_df)

            pecc.epitope_comparison.compute_epitopic_charge(
                donordf,
                recipientdf,
                f"{output_path}_{class_}",
                pecc.output_type.OutputType.DETAILS_AND_COUNT,
                class_ == "CL1" or class_ == "all",
                class_ == "CL2" or class_ == "all",
                False,
                exclude=[
                    423,
                    643,
                    928,
                    1317,
                    1490,
                    1550,
                    1612,
                    1638,
                    1796,
                    2114,
                ]
            )
```

#### Exit codes:
```
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
