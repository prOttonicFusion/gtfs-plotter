import argparse
from src.plotter import plot


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-s", "--shapes-path", required=True, help="Path to the GTFS shapes.txt"
    )
    parser.add_argument(
        "-r", "--routes-path", required=True, help="Path to the GTFS routes.txt"
    )
    parser.add_argument(
        "--shape-id-regex",
        default=None,
        help="A regular expression for selecting the route ID from the shape_id column. E.g. for MTA's NYC subway this would be '^[^.]+'",
    )
    parser.add_argument(
        "--filter-routes-by",
        default="route_id",
        help="Column to filter routes by. E.g. route_id or agency_id. Defaults to no filtering.",
    )
    parser.add_argument(
        "--filter-routes",
        nargs="+",
        default=[],
        help="Route filter values. Defaults to no filtering.",
    )

    parser.add_argument(
        "--width", type=int, default=1000, help="The display width of the map"
    )
    parser.add_argument(
        "--heigth", type=int, default=1000, help="The display heigth of the map"
    )
    parser.add_argument("--zoom", type=int, default=10, help="The map zoom level")
    parser.add_argument(
        "--map-style",
        default="open-street-map",
        help="Name of the map style to use. Accepts most Plotly map stiles, e.g. carto-darkmatter, carto-positron, open-street-map, white-bg",
    )

    args = parser.parse_args()

    plot(
        shapes_path=args.shapes_path,
        routes_path=args.routes_path,
        shape_id_regex=args.shape_id_regex,
        heigth=args.heigth,
        width=args.width,
        zoom=args.zoom,
        map_style=args.map_style,
        route_filter=(
            {"by": args.filter_routes_by, "values": args.filter_routes}
            if args.filter_routes
            else None
        ),
    )


if __name__ == "__main__":
    main()
