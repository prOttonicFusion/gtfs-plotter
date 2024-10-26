# gtfs-plotter
![Python version](https://img.shields.io/badge/python-v3.11+-blue)

A tool for reading public transit routes from [GTFS](https://gtfs.org/) files and plotting them on a map

## Usage

First, install the required dependencies
```sh
pip3 install -r requirements.txt
# OR
make dep
```
After this you can run
```
python3 plot.py --help
```
to see the available commands.

## Development

Linting and running tests:
```sh
make lint && make typecheck && make test
```

## Examples

### New York City Subway

Assuming the GTFS data has been exported to `./data/mta_subway`:
```sh
python3 plot.py data/mta_subway --map-style carto-darkmatter --heigth 820 --width 1000 --zoom 10
```
<img src="./docs/nyc_subway.jpg" width="800px" />

### Helsinki Metro:

```sh
python3 plot.py data/hsl --map-style carto-darkmatter --filter-routes 31M2 31M1 --width 1000 --heigth 500 --zoom 10
```
<img src="./docs/helsinki_metro.jpg" width="800px" />

### Los Angeles Metro Rail:

```sh
python3 plot.py data/la_metro_rail --map-style carto-darkmatter --heigth 820 --width 1000 --zoom 10
```
<img src="./docs/la_metro_rail.jpg" width="800px" />