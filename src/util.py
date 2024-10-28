import re
import pandas as pd


def parse_color(color_str) -> str | None:
    if not color_str:
        return None
    if color_str.startswith("#"):
        return color_str
    if re.fullmatch(r"([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})", color_str):
        return f"#{color_str}"
    return color_str


def generate_color_scale(routes: pd.DataFrame) -> dict[str, str]:
    scale = {}
    for _, row in routes.iterrows():
        route_id = row["route_id"]
        route_color = None

        if "route_color" in row and not pd.isna(row.loc["route_color"]):
            route_color = parse_color(row.loc["route_color"])

        scale[route_id] = route_color

    return scale
