"""
Functions to process data exported from FracMan
"""
import pandas as pd

def clean_columns(df_cols: pd.core.indexes.base.Index) -> pd.core.indexes.base.Index:
    """Clean up dataframe columns into something python

    Args:
        df_cols (pd.core.indexes.base.Index): raw columns

    Returns:
        pd.core.indexes.base.Index: cleaned columns
    """
    return (df_cols
        .str.replace("[m]","", regex=False)
        .str.replace("[\[\]!&]","", regex=False)
        .str.lower()
        )

def read_ors(filename: str) -> pd.DataFrame:
    """Reads an ASCII space delimited column file

    Args:
        filename (str): relative file path

    Returns:
        pd.DataFrame: dataframe of point data
    """
    df = pd.read_csv(filename, delim_whitespace=True)
    df.columns = clean_columns(df.columns)
    return df

def read_f2d_trace_file(filepath: str) -> pd.DataFrame:
    """Read an f2d file to get trace information, grouping by TraceID
    Takes the average of the lengths
    returns the length, strike and dip only for now

    Args:
        filepath (str): filepath

    Returns:
        pd.DataFrame: length, strike, and dip per trace
    """
    columns = (
        pd.read_csv(str(filepath), skiprows=1, nrows=1, header=None)
        .iloc[0, 0]
        .replace("#", "")
        .replace("\t", "  ")
        .split()
    )
    rows = pd.read_csv(filepath, skiprows=[0, 1], header=None)
    fault_info = rows[0].str.replace("\t", " ").str.split(expand=True)
    fault_info.columns = columns

    fault_info = fault_info.apply(pd.to_numeric, errors="coerce")
    fault_info = fault_info[fault_info["len[m]"] > 0]

    if "Seg_Strike[deg]" not in columns:
        fault_info["Seg_Strike[deg]"] = fault_info["Seg_Trend[deg]"] - 90

    fault_info = (
        fault_info.groupby("TraceID")
        .mean()[["totlen[m]", "Seg_Strike[deg]", "Seg_VerticalDev[deg]"]]
        .reset_index(drop=True)
    )
    fault_info.columns = ["length", "strike", "dip"]
    return fault_info
