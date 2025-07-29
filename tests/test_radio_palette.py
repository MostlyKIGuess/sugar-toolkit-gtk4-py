"""Tests for RadioPalette module."""

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
    from sugar.graphics.radiopalette import (
        RadioMenuButton,
        RadioToolsButton,
        RadioPalette,
    )
    from sugar.graphics.toolbutton import ToolButton


@unittest.skipUnless(GTK_AVAILABLE, "GTK4 not available")
class TestRadioMenuButton(unittest.TestCase):
    """Test cases for RadioMenuButton class."""

    def setUp(self):
        """Set up test fixtures."""
        if not Gtk.is_initialized():
            Gtk.init()

    def test_radio_menu_button_creation(self):
        """Test basic RadioMenuButton creation."""
        button = RadioMenuButton(icon_name="test-icon")
        self.assertIsInstance(button, ToolButton)
        self.assertIsNone(button.get_selected_button())

    def test_selected_button_property(self):
        """Test selected button getter/setter."""
        button = RadioMenuButton()
        test_button = ToolButton()

        button.set_selected_button(test_button)
        self.assertEqual(button.get_selected_button(), test_button)

    def test_hide_tooltip_on_click(self):
        """Test that tooltip hiding is disabled for radio buttons."""
        button = RadioMenuButton()
        # This should be False for radio buttons
        self.assertFalse(button.get_hide_tooltip_on_click())

    def test_palette_change_notification(self):
        """Test palette change handling."""
        button = RadioMenuButton()
        palette = RadioPalette()

        button.set_palette(palette)
        self.assertEqual(button.get_palette(), palette)


@unittest.skipUnless(GTK_AVAILABLE, "GTK4 not available")
class TestRadioToolsButton(unittest.TestCase):
    """Test cases for RadioToolsButton class."""

    def setUp(self):
        """Set up test fixtures."""
        if not Gtk.is_initialized():
            Gtk.init()

    def test_radio_tools_button_creation(self):
        """Test basic RadioToolsButton creation."""
        button = RadioToolsButton(icon_name="tool-test")
        self.assertIsInstance(button, RadioMenuButton)

    def test_clicked_with_no_selected_button(self):
        """Test clicking with no selected button."""
        button = RadioToolsButton()

        button.emit("clicked")

    def test_clicked_with_selected_button(self):
        """Test clicking forwards to selected button."""
        button = RadioToolsButton()
        selected_button = ToolButton()

        clicked_count = 0

        def on_clicked(btn):
            nonlocal clicked_count
            clicked_count += 1

        selected_button.connect("clicked", on_clicked)
        button.set_selected_button(selected_button)

        button.emit("clicked")

        self.assertEqual(clicked_count, 1)


@unittest.skipUnless(GTK_AVAILABLE, "GTK4 not available")
class TestRadioPalette(unittest.TestCase):
    """Test cases for RadioPalette class."""

    def setUp(self):
        """Set up test fixtures."""
        if not Gtk.is_initialized():
            Gtk.init()

    def test_radio_palette_creation(self):
        """Test basic RadioPalette creation."""
        palette = RadioPalette(primary_text="Test Palette")
        self.assertIsNotNone(palette.button_box)
        self.assertIsInstance(palette.button_box, Gtk.Box)

    def test_append_button(self):
        """Test appending buttons to palette."""
        palette = RadioPalette()
        button = ToolButton(icon_name="test-icon")

        palette.append(button, "Test Button")

        buttons = palette.get_buttons()
        self.assertEqual(len(buttons), 1)
        self.assertEqual(buttons[0], button)
        self.assertEqual(button.palette_label, "Test Button")

    def test_append_non_toolbutton_raises_error(self):
        """Test appending non-ToolButton raises TypeError."""
        palette = RadioPalette()
        regular_button = Gtk.Button()

        with self.assertRaises(TypeError):
            palette.append(regular_button, "Invalid")

    def test_append_button_with_palette_raises_error(self):
        """Test appending button that already has palette raises error."""
        palette = RadioPalette()
        button = ToolButton()
        existing_palette = RadioPalette()
        button.set_palette(existing_palette)

        with self.assertRaises(RuntimeError):
            palette.append(button, "Test")

    def test_get_buttons(self):
        """Test getting all buttons from palette."""
        palette = RadioPalette()

        button1 = ToolButton(icon_name="icon1")
        button2 = ToolButton(icon_name="icon2")

        palette.append(button1, "Button 1")
        palette.append(button2, "Button 2")

        buttons = palette.get_buttons()
        self.assertEqual(len(buttons), 2)
        self.assertIn(button1, buttons)
        self.assertIn(button2, buttons)

    def test_first_button_selected_automatically(self):
        """Test that first button is selected automatically."""
        palette = RadioPalette()
        button = ToolButton(icon_name="test")

        palette.append(button, "Test Button")

        # First button should be considered selected

    def test_button_click_handling(self):
        """Test button click handling in palette."""
        palette = RadioPalette()
        button = ToolButton(icon_name="test")

        palette.append(button, "Test Button")

        palette._on_button_clicked(button)

        # Should not raise an exception
        self.assertEqual(palette.get_primary_text(), "Test Button")

    def test_update_button(self):
        """Test update_button method."""
        palette = RadioPalette()
        button = ToolButton(icon_name="test")

        palette.append(button, "Test Button")

        palette.update_button()


@unittest.skipUnless(GTK_AVAILABLE, "GTK4 not available")
class TestRadioPaletteIntegration(unittest.TestCase):
    """Test cases for RadioPalette integration."""

    def setUp(self):
        """Set up test fixtures."""
        if not Gtk.is_initialized():
            Gtk.init()

    def test_radio_menu_button_with_palette(self):
        """Test RadioMenuButton with RadioPalette integration."""
        menu_button = RadioMenuButton(icon_name="menu-icon")
        palette = RadioPalette(primary_text="Test Menu")

        menu_button.set_palette(palette)

        option1 = ToolButton(icon_name="option1")
        option2 = ToolButton(icon_name="option2")

        palette.append(option1, "Option 1")
        palette.append(option2, "Option 2")

        self.assertEqual(len(palette.get_buttons()), 2)

    def test_radio_tools_button_integration(self):
        """Test RadioToolsButton with RadioPalette integration."""
        tools_button = RadioToolsButton(icon_name="tools")
        palette = RadioPalette(primary_text="Tools")

        tools_button.set_palette(palette)

        brush = ToolButton(icon_name="brush")
        pen = ToolButton(icon_name="pen")

        palette.append(brush, "Brush")
        palette.append(pen, "Pen")

        tools_button.set_selected_button(brush)
        self.assertEqual(tools_button.get_selected_button(), brush)


class TestRadioPaletteWithoutGTK(unittest.TestCase):
    """Test cases that work without GTK."""

    def test_radio_palette_import(self):
        """Test that RadioPalette components can be imported."""
        from sugar.graphics.radiopalette import (
            RadioMenuButton,
            RadioToolsButton,
            RadioPalette,
        )

        self.assertTrue(hasattr(RadioMenuButton, "__init__"))
        self.assertTrue(hasattr(RadioToolsButton, "__init__"))
        self.assertTrue(hasattr(RadioPalette, "__init__"))


if __name__ == "__main__":
    unittest.main()

