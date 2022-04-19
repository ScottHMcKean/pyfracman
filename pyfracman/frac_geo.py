import pandas as pd
import numpy as np
from shapely.geometry import LineString
from sklearn.linear_model import LinearRegression
from .data import clean_columns
from pathlib import Path

# Module for geospatial analysis of fractures
def flatten_frac(vertices: np.ndarray, z_val: float = None) -> LineString:
    """Take the vertices of a single fracture and flatten it to
    a z value (assert this is within the range of z values). If
    no z value given, flatten to midpoint of fracture.

    Args:
        vertices (np.ndarray): Fracture vertices from fab.py module
        z_val (float, optional): Z value to interpolate. Defaults to None.

    Returns:
        Linestring: Flattened fracture plan
    """
    # set or check z value
    if z_val is None:
        z_val = vertices[2, :].mean()
    else:
        assert z_val > vertices[2, :].min()
        assert z_val < vertices[2, :].max()

    x_vals = vertices[0, :]

    # fit a 3D plane through vertices
    # valid for any number of vertices or fracture shape)
    X = np.transpose(vertices)[:, :2]
    y = np.transpose(vertices)[:, 2:].reshape(
        -1,
    )
    reg = LinearRegression().fit(X, y)

    # fit the y-values at the z value
    y_pred = (z_val - reg.intercept_ - reg.coef_[0] * x_vals) / reg.coef_[1]

    # make a linestring
    frac_line = LineString(list(zip(x_vals, y_pred)))

    return frac_line


def get_mid_z(vertices: np.array) -> float:
    """Calculate mid z value for each fracture

    Args:
        vertices (np.ndarray): Fracture vertices from fab.py module

    Returns:
        float: Midpoint
    """
    return vertices[2, :].mean()


def get_fracture_set_stats(fpath: Path, set_name: str, set_alias: str) -> pd.DataFrame:
    """Parse a connection export from FracMan to get the Fracture set statistics

    Args:
        fpath (Path): file path
        set_name (str): name of fracture set to summarize

    Returns:
        pd.DataFrame: Dataframe with statistics
    """
    conn = pd.read_csv(fpath, delim_whitespace=True).rename(
        columns={"Set_Name": "FractureSet"}
    )
    conn.columns = clean_columns(conn.columns)

    # get set ids
    set_ids = (
        conn.query("fractureset == @set_name").groupby("object")["fracid"].apply(list)
    )
    set_ids.name = set_alias + "_ids"

    # get set counts
    set_ct = conn.query("fractureset == @set_name").groupby("object").count().iloc[:, 0]
    set_ct.name = set_alias + "_count"

    # get stage counts
    stages = (
        conn.groupby("object")
        .count()
        .reset_index()
        .rename(columns={"FractureSet": "interactions"})
    )
    stages["stage_no"] = stages.object.str.split("_").str[-1]
    stages["well"] = stages.object.str.split("_").str[-3]
    stages = (
        stages[["stage_no", "well", "object"]]
        .merge(set_ids, left_on="object", right_index=True)
        .merge(set_ct, left_on="object", right_index=True)
    )

    return stages
