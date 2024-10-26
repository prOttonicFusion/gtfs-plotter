import pandas as pd
import plotly.express as px
from typing import TypedDict
from .util import clean_shapes, generate_color_scale
import plotly.io as pio
import plotly.graph_objects as go

pio.templates["custom_theme"] = go.layout.Template(
    layout=dict(
        font=dict(
            color="#d6d6d6",
        ),
        paper_bgcolor="#1c1c1c",
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    ),
)
pio.templates.default = "plotly+custom_theme"


class Filter(TypedDict):
    by: str
    values: list[str]


def plot(
    shapes_path: str,
    routes_path: str,
    heigth: int,
    width: int,
    zoom: int,
    map_style: str,
    shape_id_regex: str | None = None,
    route_filter: Filter | None = None,
):
    shapes_df = pd.read_csv(shapes_path)
    shapes_df = clean_shapes(shapes_df, regex=shape_id_regex)

    routes_df = pd.read_csv(routes_path)

    if route_filter:
        shapes_df = shapes_df[
            shapes_df[route_filter["by"]].isin(route_filter["values"])
        ]

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
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    fig.show()
