import pandas as pd
from os import path
from typing import TypedDict


class Filter(TypedDict):
    by: str
    values: list[str]


class Gtfs(TypedDict):
    shapes: pd.DataFrame
    routes: pd.DataFrame


def filter_routes(routes_df: pd.DataFrame, filter: Filter | None) -> pd.DataFrame:
    if filter:
        routes_df = routes_df[routes_df[filter["by"]].isin(filter["values"])]

    return routes_df


def map_shapes_to_route(
    shapes_df: pd.DataFrame, trips_df: pd.DataFrame, routes_df: pd.DataFrame
) -> pd.DataFrame:
    route_ids = routes_df["route_id"].unique()

    route_id_by_shape_id = {}
    for _, r in trips_df.drop_duplicates(subset=["route_id", "shape_id"]).iterrows():
        if r["route_id"] in route_ids:
            route_id_by_shape_id[r["shape_id"]] = r["route_id"]

    shapes_df["route_id"] = shapes_df.apply(
        lambda r: (
            route_id_by_shape_id[r["shape_id"]]
            if r["shape_id"] in route_id_by_shape_id
            else ""
        ),
        axis=1,
    )
    shapes_df = shapes_df[shapes_df["route_id"] != ""]
    return shapes_df


def parse_gtfs(gtfs_path: str, route_filter: Filter | None) -> Gtfs:
    shapes_df = pd.read_csv(path.join(gtfs_path, "shapes.txt"))
    routes_df = pd.read_csv(path.join(gtfs_path, "routes.txt"))
    trips_df = pd.read_csv(
        path.join(gtfs_path, "trips.txt"), usecols=["route_id", "shape_id"]
    )

    routes_df = filter_routes(routes_df, route_filter)
    shapes_df = map_shapes_to_route(shapes_df, trips_df, routes_df=routes_df)

    return {
        "shapes": shapes_df,
        "routes": routes_df,
    }
