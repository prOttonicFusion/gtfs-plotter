import pandas as pd
from os import path
from typing import TypedDict


class Filter(TypedDict):
    by: str
    values: list[str]


class Gtfs(TypedDict):
    shapes: pd.DataFrame
    routes: pd.DataFrame
    stops: pd.DataFrame


def filter_routes(routes_df: pd.DataFrame, filter: Filter | None) -> pd.DataFrame:
    if filter:
        routes_df = routes_df[routes_df[filter["by"]].isin(filter["values"])]

    return routes_df


def add_route_id_to_shapes(
    shapes: pd.DataFrame, trips: pd.DataFrame, routes: pd.DataFrame
) -> pd.DataFrame:
    route_ids = routes["route_id"].unique()

    route_id_by_shape_id = {}
    for _, r in trips.drop_duplicates(subset=["route_id", "shape_id"]).iterrows():
        if r["route_id"] in route_ids:
            route_id_by_shape_id[r["shape_id"]] = r["route_id"]

    shapes["route_id"] = shapes.apply(
        lambda r: (
            route_id_by_shape_id[r["shape_id"]]
            if r["shape_id"] in route_id_by_shape_id
            else ""
        ),
        axis=1,
    )
    shapes = shapes[shapes["route_id"] != ""]
    return shapes


def filter_stops_by_routes(
    stops: pd.DataFrame,
    stop_times: pd.DataFrame,
    trips: pd.DataFrame,
    routes: pd.DataFrame,
) -> pd.DataFrame:
    route_ids = routes["route_id"].unique()
    trips_filtered = trips[trips["route_id"].isin(route_ids)]
    stop_times_filtered = stop_times[
        stop_times["trip_id"].isin(trips_filtered["trip_id"])
    ]
    stops = stops[stops["stop_id"].isin(stop_times_filtered["stop_id"])]
    return stops


def parse_gtfs(gtfs_path: str, route_filter: Filter | None) -> Gtfs:
    shapes_df = pd.read_csv(path.join(gtfs_path, "shapes.txt"))
    routes_df = pd.read_csv(path.join(gtfs_path, "routes.txt"))
    stop_times_df = pd.read_csv(
        path.join(gtfs_path, "stop_times.txt"), usecols=["trip_id", "stop_id"]
    )
    stops_df = pd.read_csv(
        path.join(gtfs_path, "stops.txt"),
        usecols=["stop_id", "stop_lon", "stop_lat", "stop_name"],
    )
    trips_df = pd.read_csv(
        path.join(gtfs_path, "trips.txt"), usecols=["trip_id", "route_id", "shape_id"]
    )

    routes_df = filter_routes(routes_df, route_filter)
    shapes_df = add_route_id_to_shapes(shapes_df, trips_df, routes=routes_df)
    stops_df = filter_stops_by_routes(
        stops=stops_df, stop_times=stop_times_df, trips=trips_df, routes=routes_df
    )

    return {
        "shapes": shapes_df,
        "routes": routes_df,
        "stops": stops_df,
    }
