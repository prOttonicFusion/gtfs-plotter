import unittest
import pandas as pd
from ..parser import map_shapes_to_route, filter_routes, Filter


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


class Test_map_shapes_to_route(unittest.TestCase):
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

    def test_shouldReturnMapped(self):
        mapped = map_shapes_to_route(
            shapes_df=self.shapes, trips_df=self.trips, routes_df=self.routes
        )
        self.assertEqual(mapped.shape[0], 2)
        self.assertEqual(mapped.iloc[0]["shape_id"], "A-1234")
        self.assertEqual(mapped.iloc[0]["route_id"], "A")

        self.assertEqual(mapped.iloc[1]["shape_id"], "C-8431")
        self.assertEqual(mapped.iloc[1]["route_id"], "C")
