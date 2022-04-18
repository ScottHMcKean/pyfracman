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