import pandas as pd
import re


def parse_color(color_str: str) -> str:
    if color_str.startswith("#"):
        return color_str
    if re.fullmatch(r"([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})", color_str):
        return f"#{color_str}"
    return color_str


def generate_color_scale(routes: pd.DataFrame) -> dict[str, str]:
    scale = {}
    for _, r in routes.iterrows():
        route_id = r["route_id"]
        route_color = None

        if "route_color" in r and not pd.isna(r["route_color"]):
            route_color = parse_color(r["route_color"])

        scale[route_id] = route_color

    return scale


def get_route_id_from_shape_id(shapes_df: pd.Series, regex: str) -> str:
    match = re.match(regex, shapes_df["shape_id"])
    if not match:
        raise Exception(
            f"Unable to find match for route id in shape_id '{shapes_df['shape_id']}' using regex '{regex}'"
        )
    return match.group(0)


def clean_shapes(shapes: pd.DataFrame, regex: str | None = None) -> pd.DataFrame:
    if not regex:
        shapes["route_id"] = shapes["shape_id"]
    else:

        shapes["route_id"] = shapes.apply(
            get_route_id_from_shape_id, args=(regex,), axis=1
        )
    return shapes
