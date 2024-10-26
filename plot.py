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

    args = parser.parse_args()

    plot(shapes_path=args.shapes_path, routes_path=args.routes_path)


if __name__ == "__main__":
    main()
