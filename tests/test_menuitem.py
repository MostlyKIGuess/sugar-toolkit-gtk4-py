"""Tests for MenuItem module."""

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

from sugar.graphics.menuitem import MenuItem, MenuSeparator
from sugar.graphics.xocolor import XoColor


@unittest.skipUnless(GTK_AVAILABLE, "GTK4 not available")
class TestMenuItem(unittest.TestCase):
    """Test cases for MenuItem class."""

    def setUp(self):
        """Set up test fixtures."""
        if not Gtk.is_initialized():
            Gtk.init()

    def test_menuitem_creation_text_only(self):
        """Test creating menu item with text only."""
        item = MenuItem(text_label="Test Item")
        self.assertIsInstance(item, Gtk.Button)
        self.assertEqual(item.get_text(), "Test Item")

    def test_menuitem_creation_with_icon(self):
        """Test creating menu item with icon."""
        item = MenuItem(text_label="Test Item", icon_name="document-new")
        self.assertEqual(item.get_text(), "Test Item")

        # Check that child contains both icon and label
        child = item.get_child()
        self.assertIsInstance(child, Gtk.Box)

    def test_menuitem_creation_with_xo_color(self):
        """Test creating menu item with XO color."""
        xo_color = XoColor("#FF0000,#00FF00")
        item = MenuItem(
            text_label="Colored Item",
            icon_name="emblem-favorite",
            xo_color=xo_color
        )
        self.assertEqual(item.get_text(), "Colored Item")

    def test_menuitem_creation_with_file(self):
        """Test creating menu item with file icon."""
        # This test might fail if file doesn't exist, but should not crash
        item = MenuItem(text_label="File Item", file_name="/nonexistent/file.png")
        self.assertEqual(item.get_text(), "File Item")

    def test_menuitem_text_maxlen(self):
        """Test text maximum length setting."""
        long_text = "This is a very long text that should be ellipsized"
        item = MenuItem(text_label=long_text, text_maxlen=20)
        self.assertEqual(item.get_text(), long_text)

    def test_menuitem_set_get_text(self):
        """Test setting and getting text."""
        item = MenuItem(text_label="Original")
        self.assertEqual(item.get_text(), "Original")

        item.set_text("Modified")
        self.assertEqual(item.get_text(), "Modified")

    def test_menuitem_no_text(self):
        """Test menu item without text."""
        item = MenuItem(icon_name="document-new")
        self.assertEqual(item.get_text(), "")

    def test_menuitem_accelerator(self):
        """Test accelerator setting and getting."""
        item = MenuItem(text_label="Test")

        # Initially no accelerator
        self.assertIsNone(item.get_accelerator())

        # Set accelerator
        item.set_accelerator("<Ctrl>s")
        self.assertEqual(item.get_accelerator(), "<Ctrl>s")

        # Change accelerator
        item.set_accelerator("<Ctrl>o")
        self.assertEqual(item.get_accelerator(), "<Ctrl>o")

        # Remove accelerator
        item.set_accelerator(None)
        self.assertIsNone(item.get_accelerator())

    def test_menuitem_clicked_signal(self):
        """Test clicked signal emission."""
        item = MenuItem(text_label="Test")
        clicked_called = []

        def on_clicked(widget):
            clicked_called.append(True)

        item.connect("clicked", on_clicked)
        item.emit("clicked")

        self.assertEqual(len(clicked_called), 1)

    def test_menuitem_styling(self):
        """Test that menu item has correct CSS classes."""
        item = MenuItem(text_label="Test")
        self.assertTrue(item.has_css_class("menuitem"))


@unittest.skipUnless(GTK_AVAILABLE, "GTK4 not available")
class TestMenuSeparator(unittest.TestCase):
    """Test cases for MenuSeparator class."""

    def setUp(self):
        """Set up test fixtures."""
        if not Gtk.is_initialized():
            Gtk.init()

    def test_menu_separator_creation(self):
        """Test menu separator creation."""
        separator = MenuSeparator()
        self.assertIsInstance(separator, Gtk.Separator)
        self.assertEqual(separator.get_orientation(), Gtk.Orientation.HORIZONTAL)

    def test_menu_separator_styling(self):
        """Test that separator has correct CSS class."""
        separator = MenuSeparator()
        self.assertTrue(separator.has_css_class("menu-separator"))


class TestMenuItemWithoutGTK(unittest.TestCase):
    """Test cases that work without GTK."""

    def test_menuitem_import(self):
        """Test that MenuItem can be imported."""
        from sugar.graphics.menuitem import MenuItem, MenuSeparator
        self.assertTrue(hasattr(MenuItem, '__init__'))
        self.assertTrue(hasattr(MenuSeparator, '__init__'))


if __name__ == "__main__":
    unittest.main()
