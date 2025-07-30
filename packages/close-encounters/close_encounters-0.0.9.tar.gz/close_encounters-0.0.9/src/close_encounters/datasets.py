import pandas as pd
from importlib.resources import files

def load_sample_trajectories() -> pd.DataFrame:
    """
    Load the sample trajectories dataset bundled with the package.

    Returns:
        pd.DataFrame: A DataFrame containing sample flight trajectory data.
    """
    data_path = files("close_encounters.data").joinpath("sample_trajectories.parquet")
    with data_path.open("rb") as f:
        return pd.read_parquet(f)

def load_h3_edgelengths() -> pd.DataFrame:
    """
    Load the H3 edgelengths dataset bundled with the package.

    Returns:
        pd.DataFrame: A DataFrame containing H3 edgelengths data.
    """
    data_path = files('close_encounters.data').joinpath('h3_edgelengths.csv')
    with data_path.open("rb") as f:
        return pd.read_csv(f)