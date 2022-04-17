# Module with geospatial functions for wells, stages, etc. (i.e. not fractures)
from pathlib import Path
import pandas as pd
from shapely.geometry import LineString
import geopandas as gpd


def load_survey_export(well_path: Path) -> pd.DataFrame:
    """Load Fracman survey exports into a clean csv file

    Args:
        well_path (Path): Path to a single well file for the survey

    Returns:
        pd.Dataframe: Cleaned survey with md, x, y, and z
    """
    return pd.read_csv(
        well_path,
        skiprows=13,
        sep="\s{2,}",
        engine="python",
        header=None,
        names=["md", "x", "y", "z"],
    ).assign(well=well_path.name.split("_")[0])


def load_stage_location(stg_loc_path: Path) -> pd.DataFrame:
    """Load stage locations from Fracman export

    Args:
        stage_loc_path (Path): Path to a well stage location file

    Returns:
        pd.DataFrame: cleaned stage locations
    """
    stage_loc = (
        pd.read_csv(stg_loc_path, sep="\s{2,}", engine="python")
        .assign(well=stg_loc_path.name.split("_")[0])
        .drop(["Well", "IntervalSet", "Index", "ParentWell"], axis=1)
    )
    stage_loc["Interval"] = (
        stage_loc.Interval.str.replace('"', "", regex=True).replace("", 0).astype(int)
    )
    stage_loc.columns = (
        stage_loc.columns.str.replace("[", "_", regex=True)
        .str.replace("]", "", regex=True)
        .str.lower()
    )
    stage_loc = stage_loc.rename(columns={"interval": "stage"}).query("stage > 0")
    return stage_loc


# Make linestrings
def well_surveys_to_linestrings(surveys: pd.DataFrame) -> gpd.GeoDataFrame:
    """Convert a DataFrame of well surveys into a flattened linestring

    Args:
        surveys (pd.DataFrame): Well surveys with md, x, y, z, and well

    Returns:
        gpd.GeoDataFrame: Well and linestring in geodataframe
    """
    gdf = gpd.GeoDataFrame(
        surveys, geometry=gpd.points_from_xy(surveys["x"], surveys["y"])
    )

    line_gdf = (
        gdf.sort_values(by=["well", "md"])
        .groupby(["well"])["geometry"]
        .apply(lambda x: LineString(x.tolist()))
    )
    return gpd.GeoDataFrame(line_gdf, geometry="geometry")
