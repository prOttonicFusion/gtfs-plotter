import unittest
import pandas as pd
from ..util import generate_color_scale, clean_shapes


class Test_generate_color_scale(unittest.TestCase):
    def test_shouldReturnValidColorScale(self):
        routes_df = pd.DataFrame(
            {
                "agency_id": ["Foo Inc.", "Foo Inc."],
                "route_id": [100, "A1"],
                "route_color": ["aaabbb", "cccdddd"],
            }
        )
        scale = generate_color_scale(routes=routes_df, default_color="000")
        self.assertEqual(scale, {100: "#aaabbb", "A1": "#cccdddd"})


class Test_clean_shapes(unittest.TestCase):
    def test_shouldAddValidRouteIdCol(self):
        shapes_df = pd.DataFrame({"shape_id": ["X..Foo", "X.Bar", "12..200"]})
        clean = clean_shapes(shapes=shapes_df)
        self.assertEqual(clean["route_id"].loc[0], "X")
        self.assertEqual(clean["route_id"].loc[1], "X")
        self.assertEqual(clean["route_id"].loc[2], "12")
