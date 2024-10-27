import unittest
import pandas as pd
from ..util import generate_color_scale, parse_color


class Test_generate_color_scale(unittest.TestCase):
    def test_shouldReturnValidColorScale(self):
        routes = pd.DataFrame(
            {
                "agency_id": ["Foo Inc.", "Foo Inc."],
                "route_id": [100, "A1"],
                "route_color": ["aaabbb", "cyan"],
            }
        )
        scale = generate_color_scale(routes=routes)
        self.assertEqual(scale, {100: "#aaabbb", "A1": "cyan"})

    def test_shouldUseNoneOnMissingValue(self):
        routes = pd.DataFrame(
            {
                "agency_id": ["Foo Inc.", "Foo Inc."],
                "route_id": [100, "A1"],
                "route_color": ["111", None],
            }
        )
        scale = generate_color_scale(routes=routes)
        self.assertEqual(scale, {100: "#111", "A1": None})

    def test_shouldUseNoneOnMissingColumn(self):
        routes = pd.DataFrame(
            {
                "agency_id": ["Foo Inc.", "Foo Inc."],
                "route_id": [100, "A1"],
            }
        )
        scale = generate_color_scale(routes=routes)
        self.assertEqual(scale, {100: None, "A1": None})


class Test_parse_color(unittest.TestCase):
    def test_shouldCorrectlyParseHexColors(self):
        self.assertEqual(parse_color("#000"), "#000")
        self.assertEqual(parse_color("000"), "#000")
        self.assertEqual(parse_color("#123abc"), "#123abc")
        self.assertEqual(parse_color("123abc"), "#123abc")

    def test_shouldReturnNonHexColorsAsIs(self):
        self.assertEqual(parse_color("12G45A"), "12G45A")
        self.assertEqual(parse_color("red"), "red")
