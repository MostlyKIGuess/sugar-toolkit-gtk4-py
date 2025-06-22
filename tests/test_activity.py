#!/usr/bin/env python3
"""Tests for Activity class."""

import unittest
import sys
import os

# src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

try:
    import gi

    gi.require_version("Gtk", "4.0")
    from gi.repository import Gtk

    GTK_AVAILABLE = True
except (ImportError, ValueError):
    GTK_AVAILABLE = False

if GTK_AVAILABLE:
    from sugar.activity.activity import Activity, SimpleActivity


@unittest.skipUnless(GTK_AVAILABLE, "GTK4 not available")
class TestActivity(unittest.TestCase):
    """Test cases for Activity functionality."""

    def setUp(self):
        """Set up test fixtures."""
        # Initialize GTK if not already done
        if not Gtk.is_initialized():
            Gtk.init()

    def test_activity_creation(self):
        """Test basic Activity creation."""
        activity = Activity()
        self.assertIsNotNone(activity.get_id())
        self.assertIsInstance(activity.get_id(), str)
        self.assertEqual(activity.get_title(), "Sugar Activity")
        self.assertTrue(activity.get_active())

    def test_simple_activity_creation(self):
        """Test SimpleActivity creation."""
        activity = SimpleActivity()
        self.assertIsNotNone(activity.get_id())
        self.assertIsInstance(activity.get_id(), str)

    def test_activity_metadata(self):
        """Test activity metadata handling."""
        activity = Activity()
        metadata = activity.get_metadata()
        self.assertIsInstance(metadata, dict)
        self.assertIn("title", metadata)
        self.assertIn("activity_id", metadata)

    def test_activity_title(self):
        """Test activity title setting."""
        activity = Activity()
        activity.set_title("Test Activity")
        self.assertEqual(activity.get_title(), "Test Activity")

    def test_activity_active_state(self):
        """Test activity active state."""
        activity = Activity()
        self.assertTrue(activity.get_active())

        activity.set_active(False)
        self.assertFalse(activity.get_active())

    def test_canvas_operations(self):
        """Test canvas setting and getting."""
        activity = Activity()

        # Initially no canvas
        self.assertIsNone(activity.get_canvas())

        # then set the canvas
        label = Gtk.Label(label="Test Canvas")
        activity.set_canvas(label)
        self.assertEqual(activity.get_canvas(), label)

    def test_sharing_state(self):
        """Test activity sharing state."""
        activity = Activity()
        self.assertFalse(activity.get_shared())

        activity.share()
        self.assertTrue(activity.get_shared())

    def test_can_close(self):
        """Test activity close permission."""
        activity = Activity()
        self.assertTrue(activity.can_close())


class TestActivityWithoutGTK(unittest.TestCase):
    """Test cases that don't require GTK."""

    def test_utility_functions(self):
        """Test utility functions."""
        from sugar.activity.activity import (
            get_bundle_name,
            get_bundle_path,
            get_activity_root,
        )

        # These should return strings
        self.assertIsInstance(get_bundle_name(), str)
        self.assertIsInstance(get_bundle_path(), str)
        self.assertIsInstance(get_activity_root(), str)


if __name__ == "__main__":
    unittest.main()
