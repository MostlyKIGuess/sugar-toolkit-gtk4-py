#!/usr/bin/env python3
"""Tests for XoColor class."""

import unittest
import sys
import os

# src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from sugar.graphics.xocolor import XoColor


class TestXoColor(unittest.TestCase):
    """Test cases for XoColor functionality."""

    def test_basic_creation(self):
        """Test basic XoColor creation."""
        color = XoColor()
        self.assertIsInstance(color.get_stroke_color(), str)
        self.assertIsInstance(color.get_fill_color(), str)
        self.assertTrue(color.get_stroke_color().startswith("#"))
        self.assertTrue(color.get_fill_color().startswith("#"))

    def test_string_parsing(self):
        """Test color string parsing."""
        color = XoColor("#FF0000,#00FF00")
        self.assertEqual(color.get_stroke_color(), "#FF0000")
        self.assertEqual(color.get_fill_color(), "#00FF00")

    def test_white_color(self):
        """Test white color theme."""
        color = XoColor("white")
        self.assertEqual(color.get_stroke_color(), "#ffffff")
        self.assertEqual(color.get_fill_color(), "#414141")

    def test_insensitive_color(self):
        """Test insensitive color theme."""
        color = XoColor("insensitive")
        self.assertEqual(color.get_stroke_color(), "#ffffff")
        self.assertEqual(color.get_fill_color(), "#e2e2e2")

    def test_equality(self):
        """Test color equality."""
        color1 = XoColor("#FF0000,#00FF00")
        color2 = XoColor("#FF0000,#00FF00")
        color3 = XoColor("#00FF00,#FF0000")

        self.assertEqual(color1, color2)
        self.assertNotEqual(color1, color3)

    def test_to_string(self):
        """Test string conversion."""
        color = XoColor("#FF0000,#00FF00")
        self.assertEqual(color.to_string(), "#FF0000,#00FF00")

    def test_rgba_conversion(self):
        """Test RGBA tuple conversion."""
        color = XoColor("#FF0000,#00FF00")
        stroke_rgba, fill_rgba = color.to_rgba_tuple()

        # Red stroke
        self.assertAlmostEqual(stroke_rgba[0], 1.0)  # R
        self.assertAlmostEqual(stroke_rgba[1], 0.0)  # G
        self.assertAlmostEqual(stroke_rgba[2], 0.0)  # B
        self.assertAlmostEqual(stroke_rgba[3], 1.0)  # A

        # Green fill
        self.assertAlmostEqual(fill_rgba[0], 0.0)  # R
        self.assertAlmostEqual(fill_rgba[1], 1.0)  # G
        self.assertAlmostEqual(fill_rgba[2], 0.0)  # B
        self.assertAlmostEqual(fill_rgba[3], 1.0)  # A

    def test_from_string_classmethod(self):
        """Test from_string class method."""
        color = XoColor.from_string("#FF0000,#00FF00")
        self.assertEqual(color.get_stroke_color(), "#FF0000")
        self.assertEqual(color.get_fill_color(), "#00FF00")

    def test_random_color(self):
        """Test random color generation."""
        color = XoColor.get_random_color()
        self.assertIsInstance(color, XoColor)
        self.assertTrue(color.get_stroke_color().startswith("#"))
        self.assertTrue(color.get_fill_color().startswith("#"))

    def test_invalid_string(self):
        """Test invalid color string handling."""
        with self.assertRaises(ValueError):
            XoColor.from_string("invalid")

    def test_hash_and_set(self):
        """Test that XoColor can be used in sets and as dict keys."""
        color1 = XoColor("#FF0000,#00FF00")
        color2 = XoColor("#FF0000,#00FF00")
        color3 = XoColor("#00FF00,#FF0000")

        # Test in set
        color_set = {color1, color2, color3}
        self.assertEqual(len(color_set), 2)  # color1 and color2 are equal

        # Test as dict key
        color_dict = {color1: "red-green", color3: "green-red"}
        self.assertEqual(len(color_dict), 2)


if __name__ == "__main__":
    unittest.main()
