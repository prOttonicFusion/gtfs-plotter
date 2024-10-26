import argparse
import pandas as pd
import plotly.express as px

default_route_color = "000000"


def generate_color_scale(routes: pd.DataFrame) -> dict[str, str]:
    scale = {}
    for _, r in routes.iterrows():
        route_id = r["route_id"]
        route_hex_code = r["route_color"]
        if pd.isna(route_hex_code):
            route_hex_code = default_route_color

        scale[route_id] = f"#{route_hex_code}"

    return scale


def plot(shapes_path: str, routes_path: str):
    shapes_df = pd.read_csv(shapes_path)
    routes_df = pd.read_csv(routes_path)

    shapes_df["route_id"] = shapes_df.apply(
        lambda row: row["shape_id"].split(".")[0], axis=1
    )

    color_scale = generate_color_scale(routes_df)

    fig = px.line_mapbox(
        shapes_df,
        line_group="shape_id",
        lat="shape_pt_lat",
        lon="shape_pt_lon",
        color="route_id",
        color_discrete_map=color_scale,
        zoom=10,
        width=1000,
        height=1000,
    )

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 10, "t": 10, "l": 10, "b": 10})
    fig.show()


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-s", "--shapes-path", required=True, help="Path to the GTFS shapes.txt"
    )
    parser.add_argument(
        "-r", "--routes-path", required=True, help="Path to the GTFS routes.txt"
    )

    args = parser.parse_args()

    plot(shapes_path=args.shapes_path, routes_path=args.routes_path)


if __name__ == "__main__":
    main()
