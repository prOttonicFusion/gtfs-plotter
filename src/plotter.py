import pandas as pd
import plotly.express as px
from .util import clean_shapes, generate_color_scale


def plot(
    shapes_path: str,
    routes_path: str,
    shape_id_regex: str | None,
    heigth: int,
    width: int,
    zoom: int,
    map_style: str,
):
    shapes_df = pd.read_csv(shapes_path)
    routes_df = pd.read_csv(routes_path)

    shapes_df = clean_shapes(shapes_df, regex=shape_id_regex)
    color_scale = generate_color_scale(routes_df)

    fig = px.line_mapbox(
        shapes_df,
        line_group="shape_id",
        lat="shape_pt_lat",
        lon="shape_pt_lon",
        color="route_id",
        color_discrete_map=color_scale,
        zoom=zoom,
        width=width,
        height=heigth,
    )

    fig.update_layout(mapbox_style=map_style)
    fig.update_layout(margin={"r": 10, "t": 10, "l": 10, "b": 10})
    fig.show()
