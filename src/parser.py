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


def filter_routes(routes: pd.DataFrame, filter: Filter | None) -> pd.DataFrame:
    if filter:
        routes = routes[routes[filter["by"]].isin(filter["values"])]

    return routes


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


def read_gtfs_csv(file_path: str, usecols: list[str] | None = None) -> pd.DataFrame:
    df = pd.read_csv(file_path, dtype=str, keep_default_na=False, usecols=usecols)

    for col in df.columns:
        if col.endswith("_lat") or col.endswith("_lon"):
            df[col] = df[col].astype(float)

    return df


def parse_gtfs(
    gtfs_path: str, route_filter: Filter | None = None, parse_stops=True
) -> Gtfs:
    shapes = read_gtfs_csv(path.join(gtfs_path, "shapes.txt"))
    routes = read_gtfs_csv(path.join(gtfs_path, "routes.txt"))
    trips = read_gtfs_csv(
        path.join(gtfs_path, "trips.txt"), usecols=["trip_id", "route_id", "shape_id"]
    )

    routes = filter_routes(routes, route_filter)
    shapes = add_route_id_to_shapes(shapes, trips, routes=routes)

    stops = pd.DataFrame()
    if parse_stops:
        stops = pd.read_csv(
            path.join(gtfs_path, "stops.txt"),
            usecols=["stop_id", "stop_lon", "stop_lat", "stop_name"],
            dtype=str,
            keep_default_na=False,
        )
        stop_times = pd.read_csv(
            path.join(gtfs_path, "stop_times.txt"),
            usecols=["trip_id", "stop_id"],
            dtype=str,
            keep_default_na=False,
        )
        stops = filter_stops_by_routes(
            stops=stops, stop_times=stop_times, trips=trips, routes=routes
        )

    return {"shapes": shapes, "routes": routes, "stops": stops}
