"""
Module for point pattern analysis of FracMan simulated
microseismic or induced seismicity events
"""
import pandas as pd


def read_ors_file(filename: str) -> pd.DataFrame:
    """Read an ORS file

    Args:
        filename (str): .ors filename with suffix (e.g. events.ors)

    Returns:
        pd.DataFrame: Parsed dataframe with original column names
    """
    with open(filename) as f:
        cols = f.readline()
    columns = [s.strip() for s in cols.replace("\t", " ").split(" ") if s]
    return pd.read_csv(
        filename,
        skiprows=1,
        index_col=False,
        sep="\s{2,}",
        names=columns,
        engine="python",
    )


def read_asc_file(filename: str) -> pd.DataFrame:
    """Read an ASC file, preferred for point exports due to better precision

    Args:
        filename (str): asc filename with suffix (e.g. events.ors)

    Returns:
        pd.DataFrame: Parsed dataframe with original column names
    """
    filename = "InducedEvents_1_pt.asc"
    with open(filename) as f:
        lines = f.readlines()
    ncols = int(lines[2].split()[0])
    columns = [l.split()[0] for l in lines[3 : 3 + ncols]]
    data = [l.split() for l in lines[3 + ncols :]]
    return pd.DataFrame(data, columns=columns).apply(pd.to_numeric)
