"""Tests for RadioToolButton module."""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

try:
    import gi

    gi.require_version("Gtk", "4.0")
    from gi.repository import Gtk

    GTK_AVAILABLE = True
except (ImportError, ValueError):
    GTK_AVAILABLE = False

if GTK_AVAILABLE:
    from sugar.graphics.radiotoolbutton import RadioToolButton
    from sugar.graphics.toolbutton import ToolButton


@unittest.skipUnless(GTK_AVAILABLE, "GTK4 not available")
class TestRadioToolButton(unittest.TestCase):
    """Test cases for RadioToolButton class."""

    def setUp(self):
        """Set up test fixtures."""
        if not Gtk.is_initialized():
            Gtk.init()

    def test_radio_tool_button_creation(self):
        """Test basic RadioToolButton creation."""
        button = RadioToolButton(icon_name="test-icon")
        self.assertIsInstance(button, ToolButton)
        self.assertFalse(button.get_active())
        self.assertEqual(len(button.get_group()), 1)

    def test_single_button_group(self):
        """Test single button behavior."""
        button = RadioToolButton(icon_name="test")

        button.set_active(True)
        self.assertTrue(button.get_active())

        button.set_active(False)
        self.assertFalse(button.get_active())

    def test_multiple_button_group(self):
        """Test multiple button radio group behavior."""
        button1 = RadioToolButton(icon_name="test1")
        button2 = RadioToolButton(icon_name="test2", group=button1)
        button3 = RadioToolButton(icon_name="test3", group=button1)

        self.assertEqual(len(button1.get_group()), 3)
        self.assertEqual(len(button2.get_group()), 3)
        self.assertEqual(len(button3.get_group()), 3)

        self.assertFalse(button1.get_active())
        self.assertFalse(button2.get_active())
        self.assertFalse(button3.get_active())

    def test_radio_group_exclusivity(self):
        """Test that only one button can be active in a group."""
        button1 = RadioToolButton(icon_name="test1")
        button2 = RadioToolButton(icon_name="test2", group=button1)
        button3 = RadioToolButton(icon_name="test3", group=button1)

        button1.set_active(True)
        self.assertTrue(button1.get_active())
        self.assertFalse(button2.get_active())
        self.assertFalse(button3.get_active())

        button2.set_active(True)
        self.assertFalse(button1.get_active())
        self.assertTrue(button2.get_active())
        self.assertFalse(button3.get_active())

        button3.set_active(True)
        self.assertFalse(button1.get_active())
        self.assertFalse(button2.get_active())
        self.assertTrue(button3.get_active())

    def test_toggled_signal(self):
        """Test toggled signal emission."""
        button1 = RadioToolButton(icon_name="test1")
        button2 = RadioToolButton(icon_name="test2", group=button1)

        signal_count = 0

        def on_toggled(button):
            nonlocal signal_count
            signal_count += 1

        button1.connect("toggled", on_toggled)
        button2.connect("toggled", on_toggled)

        button1.set_active(True)
        self.assertEqual(signal_count, 1)  # button1 toggled on

        button2.set_active(True)
        self.assertEqual(signal_count, 3)  # button1 toggled off, button2 toggled on

    def test_click_behavior(self):
        """Test click behavior."""
        button1 = RadioToolButton(icon_name="test1")
        button2 = RadioToolButton(icon_name="test2", group=button1)

        self.assertFalse(button1.get_active())
        button1.emit("clicked")
        self.assertTrue(button1.get_active())

        button1.emit("clicked")
        self.assertTrue(button1.get_active())

        button2.emit("clicked")
        self.assertFalse(button1.get_active())
        self.assertTrue(button2.get_active())

    def test_group_management(self):
        """Test radio group management."""
        button1 = RadioToolButton(icon_name="test1")
        button2 = RadioToolButton(icon_name="test2")
        button3 = RadioToolButton(icon_name="test3")

        self.assertEqual(len(button1.get_group()), 1)
        self.assertEqual(len(button2.get_group()), 1)

        button2.set_group(button1)
        self.assertEqual(len(button1.get_group()), 2)
        self.assertEqual(len(button2.get_group()), 2)

        button3.set_group(button1)
        self.assertEqual(len(button1.get_group()), 3)
        self.assertEqual(len(button2.get_group()), 3)
        self.assertEqual(len(button3.get_group()), 3)

    def test_active_property(self):
        """Test active property."""
        button = RadioToolButton(icon_name="test")

        self.assertFalse(button.active)

        button.active = True
        self.assertTrue(button.active)
        self.assertTrue(button.get_active())

    def test_visual_state_updates(self):
        """Test visual state updates."""
        button = RadioToolButton(icon_name="test")

        button.set_active(True)
        self.assertTrue(button.has_css_class("active"))

        button.set_active(False)
        self.assertFalse(button.has_css_class("active"))

    def test_separate_groups(self):
        """Test that separate groups work independently."""
        group1_btn1 = RadioToolButton(icon_name="g1b1")
        group1_btn2 = RadioToolButton(icon_name="g1b2", group=group1_btn1)

        group2_btn1 = RadioToolButton(icon_name="g2b1")
        group2_btn2 = RadioToolButton(icon_name="g2b2", group=group2_btn1)

        group1_btn1.set_active(True)
        group2_btn2.set_active(True)

        self.assertTrue(group1_btn1.get_active())
        self.assertTrue(group2_btn2.get_active())
        self.assertFalse(group1_btn2.get_active())
        self.assertFalse(group2_btn1.get_active())


class TestRadioToolButtonWithoutGTK(unittest.TestCase):
    """Test cases that work without GTK."""

    def test_radio_tool_button_import(self):
        """Test that RadioToolButton can be imported."""
        from sugar.graphics.radiotoolbutton import RadioToolButton

        self.assertTrue(hasattr(RadioToolButton, "__init__"))


if __name__ == "__main__":
    unittest.main()

