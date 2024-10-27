import plotly.express as px
from .util import generate_color_scale
from .parser import parse_gtfs, Filter
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


def plot(
    gtfs_path: str,
    show_stops: bool,
    heigth: int,
    width: int,
    zoom: int,
    map_style: str,
    route_filter: Filter | None = None,
):
    gtfs = parse_gtfs(gtfs_path, route_filter, parse_stops=show_stops)
    color_scale = generate_color_scale(gtfs["routes"])

    fig = px.line_mapbox(
        gtfs["shapes"],
        line_group="shape_id",
        lat="shape_pt_lat",
        lon="shape_pt_lon",
        color="route_id",
        color_discrete_map=color_scale,
        zoom=zoom,
        width=width,
        height=heigth,
    )

    if show_stops:
        fig.add_scattermapbox(
            name="Stops",
            lat=gtfs["stops"]["stop_lat"],
            lon=gtfs["stops"]["stop_lon"],
            hovertext=gtfs["stops"]["stop_name"],
            marker={"color": "white", "size": 5},
        )

    fig.update_layout(mapbox_style=map_style)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    fig.show()
