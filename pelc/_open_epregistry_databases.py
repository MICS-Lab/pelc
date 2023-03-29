import os
import pandas as pd


def _open_epregistry_database(
        path_to_csv: str,
        ghost_alleles: str | list[str],
        no_eplets: bool = False
) -> pd.DataFrame:
    """
    :param path_to_csv: path to the csv EpRegistry database file
    :param ghost_alleles: allele(s) string(s) to be used as (a) ghost allele(s) (no eplets)

    :return: pandas.DataFrame with the EpRegistry database and the ghost allele
    """

    df_db: pd.DataFrame

    file_name_no_extension: str = path_to_csv.split('.csv')[0]
    suffix: str = ghost_alleles if isinstance(ghost_alleles, str) else ghost_alleles[0]
    pickle_file_name: str = f"{file_name_no_extension}_{no_eplets}_{suffix}.pickle"

    # replace * by _ in the pickle file name to avoid problems when * is in the file name
    pickle_file_name = pickle_file_name.replace('*', '_')

    # if pickle file exists, load it
    if os.path.exists(pickle_file_name):
        df_db = pd.read_pickle(pickle_file_name)
        return df_db
    # if pickle file does not exist, create it
    else:
        if no_eplets:
            df_db = pd.read_csv(path_to_csv, sep=";", usecols=[0]).set_index("allele")
            # add a row to an empty dataframe with concat
            for ghost_allele in ghost_alleles:
                df_db = pd.concat([df_db, pd.DataFrame(columns=[], index=[ghost_allele])])
        else:
            df_db = pd.read_csv(path_to_csv, sep=";").set_index("allele")
            for ghost_allele in ghost_alleles:
                # add row with nan values
                df_db.loc[ghost_allele] = float("nan")

        df_db.to_pickle(pickle_file_name)

    return df_db


def open_ep_data(eplet_comparison_file_directory_path: str) -> pd.DataFrame:
    """
    :return: pandas.DataFrame with the eplet informations database
    """

    df_ep_data: pd.DataFrame

    # if pickle file exists, load it
    if os.path.exists(f"{eplet_comparison_file_directory_path}/data/ep_data.pickle"):
        df_ep_data = pd.read_pickle(f"{eplet_comparison_file_directory_path}/data/ep_data.pickle")
        return df_ep_data
    # if pickle file does not exist, create it
    else:
        df_ep_data = pd.read_csv(f"{eplet_comparison_file_directory_path}/data/ep_data.csv", sep=";")
        df_ep_data.to_pickle(f"{eplet_comparison_file_directory_path}/data/ep_data.pickle")
        return df_ep_data
