# gtfs-plotter

A tool for reading public transit routes from [GTFS](https://gtfs.org/) files and plotting them on a map

## Usage

Install dependencies:
```sh
pip3 install -r requirements.txt
# OR
make dep
```

View the usage instructions:
```
python3 plot.py --help
```

## Development

Linting and running tests:
```
make lint
make typecheck
make test
```