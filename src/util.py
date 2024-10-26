import pandas as pd


def generate_color_scale(routes: pd.DataFrame, default_color: str) -> dict[str, str]:
    scale = {}
    for _, r in routes.iterrows():
        route_id = r["route_id"]
        route_hex_code = r["route_color"]
        if pd.isna(route_hex_code):
            route_hex_code = default_color

        scale[route_id] = f"#{route_hex_code}"

    return scale


def clean_shapes(shapes: pd.DataFrame) -> pd.DataFrame:
    shapes["route_id"] = shapes.apply(lambda row: row["shape_id"].split(".")[0], axis=1)
    return shapes
