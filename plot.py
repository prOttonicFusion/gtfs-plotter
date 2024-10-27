import argparse
from src.plotter import plot


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "gtfs_path", help="Path to a directory containing the GTFS files"
    )
    parser.add_argument(
        "--stops",
        action="store_true",
        default=False,
        help="Whether to show stations/stops",
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
        gtfs_path=args.gtfs_path,
        heigth=args.heigth,
        width=args.width,
        zoom=args.zoom,
        map_style=args.map_style,
        show_stops=args.stops,
        route_filter=(
            {"by": args.filter_routes_by, "values": args.filter_routes}
            if args.filter_routes
            else None
        ),
    )


if __name__ == "__main__":
    main()
