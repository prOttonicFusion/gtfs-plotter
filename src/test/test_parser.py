import unittest
import tempfile
import pandas as pd
import pandas.testing as pdt
from ..parser import (
    Filter,
    add_route_id_to_shapes,
    filter_routes,
    filter_stops_by_routes,
    read_gtfs_csv,
)


class Test_filter_routes(unittest.TestCase):
    routes = pd.DataFrame(
        {
            "agency_id": ["Foo Inc.", "Foo Inc.", "Foo Inc."],
            "route_id": ["A", "B", "C"],
            "route_color": ["red", "blue", "green"],
        }
    )

    def test_shouldReturnFilteredById(self):
        filtered = filter_routes(
            self.routes, Filter({"by": "route_id", "values": ["B"]})
        )
        self.assertEqual(filtered.shape[0], 1)
        self.assertEqual(filtered.iloc[0]["route_id"], "B")


class Test_add_route_id_to_shapes(unittest.TestCase):
    routes = pd.DataFrame(
        {"agency_id": ["Foo Inc.", "Foo Inc."], "route_id": ["A", "C"]}
    )
    shapes = pd.DataFrame(
        {
            "shape_id": ["A-1234", "B-456", "C-8431", "C-8833"],
            "shape_pt_lat": ["1.234", "4.567", "7.890", "8.919"],
            "shape_pt_lon": ["4.321", "7.654", "0.123", "0.234"],
        }
    )
    trips = pd.DataFrame(
        {
            "route_id": ["A", "B", "C"],
            "shape_id": ["A-1234", "B-456", "C-8431"],
            "direction_id": ["North-1", "South-1", "West-2"],
        }
    )

    def test_shouldReturnShapesWithRoutes(self):
        shapes = add_route_id_to_shapes(
            shapes=self.shapes, trips=self.trips, routes=self.routes
        )
        self.assertEqual(shapes.shape[0], 2)
        self.assertEqual(shapes.iloc[0]["shape_id"], "A-1234")
        self.assertEqual(shapes.iloc[0]["route_id"], "A")

        self.assertEqual(shapes.iloc[1]["shape_id"], "C-8431")
        self.assertEqual(shapes.iloc[1]["route_id"], "C")


class Test_filter_stops_by_routes(unittest.TestCase):
    routes = pd.DataFrame(
        {"agency_id": ["Foo Inc.", "Foo Inc."], "route_id": ["A", "C"]}
    )
    stops = pd.DataFrame(
        {
            "stop_id": ["Here", "There", "Nowhere"],
            "stop_pt_lat": ["1.234", "4.567", "7.890"],
            "stop_pt_lon": ["4.321", "7.654", "0.123"],
        }
    )
    stop_times = pd.DataFrame(
        {
            "trip_id": ["A-1234", "B-456", "C-8431", "A-1234"],
            "stop_id": ["Here", "There", "Nowhere", "Nowhere"],
            "arrival_time": ["10:32:00", "11:00:00", "12:45:00", "12:50:00"],
        }
    )
    trips = pd.DataFrame(
        {
            "trip_id": ["A-1234", "B-456", "C-8431"],
            "route_id": ["A", "B", "C"],
            "direction_id": ["North-1", "South-1", "West-2"],
        }
    )

    def test_shouldReturnFiltered(self):
        filtered = filter_stops_by_routes(
            stops=self.stops,
            stop_times=self.stop_times,
            routes=self.routes,
            trips=self.trips,
        )
        self.assertEqual(filtered.shape[0], 2)
        self.assertEqual(filtered.iloc[0]["stop_id"], "Here")
        self.assertEqual(filtered.iloc[1]["stop_id"], "Nowhere")


class Test_read_gtfs_csv(unittest.TestCase):
    def test_shouldCorrectlyParseCsvToDf(self):
        with tempfile.NamedTemporaryFile(mode="w+t", delete_on_close=False) as f:
            f.write("foo,bar\nHello,World!")
            f.close()

            df = read_gtfs_csv(f.name)
            pdt.assert_frame_equal(
                df, pd.DataFrame({"foo": ["Hello"], "bar": ["World!"]})
            )

    def test_shouldCorrectlyParseNumericalCols(self):
        with tempfile.NamedTemporaryFile(mode="w+t", delete_on_close=False) as f:
            f.write("f_id,f_lat,f_lon\nA,1.123,4.567\n1,8.910,0.123")
            f.close()

            df = read_gtfs_csv(f.name)
            pdt.assert_frame_equal(
                df,
                pd.DataFrame(
                    {
                        "f_id": ["A", "1"],
                        "f_lat": [1.123, 8.910],
                        "f_lon": [4.567, 0.123],
                    }
                ),
            )
