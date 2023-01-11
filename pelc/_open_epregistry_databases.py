import pandas as pd


def _open_epregistry_database(path_to_csv: str, ghost_allele: str, no_eplets: bool = False) -> pd.DataFrame:
    """
    :param path_to_csv: path to the csv EpRegistry database file
    :param ghost_allele: allele string to be used as a ghost allele (no eplets)

    :return: pandas.DataFrame with the EpRegistry database and the ghost allele
    """

    df_db: pd.DataFrame
    if no_eplets:
        df_db = pd.read_csv(path_to_csv, sep=";", usecols=[0]).set_index("allele")
        # add a row to an empty dataframe with concat
        df_db = pd.concat([df_db, pd.DataFrame(columns=[], index=[ghost_allele])])
    else:
        df_db = pd.read_csv(path_to_csv, sep=";").set_index("allele")
        # add row with nan values
        df_db.loc[ghost_allele] = float("nan")

    return df_db
