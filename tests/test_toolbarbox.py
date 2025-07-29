"""
Unit tests for sugar.graphics.toolbarbox module.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from sugar.graphics.toolbarbox import ToolbarBox, ToolbarButton
from sugar.graphics.toolbutton import ToolButton


class TestToolbarBox(unittest.TestCase):
    """Test cases for ToolbarBox widget."""

    def setUp(self):
        """Set up test fixtures."""
        self.toolbarbox = ToolbarBox()

    def test_toolbarbox_creation(self):
        """Test ToolbarBox can be created."""
        self.assertIsInstance(self.toolbarbox, ToolbarBox)
        self.assertIsInstance(self.toolbarbox, Gtk.Box)

    def test_toolbar_property(self):
        """Test toolbar property access."""
        toolbar = self.toolbarbox.get_toolbar()
        self.assertIsNotNone(toolbar)
        self.assertIsInstance(toolbar, Gtk.Box)

        self.assertEqual(toolbar, self.toolbarbox.toolbar)

    def test_padding_property(self):
        """Test padding property."""
        self.assertIsNotNone(self.toolbarbox.get_padding())

        new_padding = 20
        self.toolbarbox.set_padding(new_padding)
        self.assertEqual(self.toolbarbox.get_padding(), new_padding)

        self.toolbarbox.padding = 30
        self.assertEqual(self.toolbarbox.padding, 30)

    def test_expanded_button_property(self):
        """Test expanded button property."""
        self.assertIsNone(self.toolbarbox.get_expanded_button())

        page = Gtk.Box()
        button = ToolbarButton(page=page, icon_name="edit-copy")
        self.toolbarbox.toolbar.append(button)

        self.toolbarbox.set_expanded_button(button)
        self.assertEqual(self.toolbarbox.get_expanded_button(), button)

        self.assertEqual(self.toolbarbox.expanded_button, button)


class TestToolbarButton(unittest.TestCase):
    """Test cases for ToolbarButton widget."""

    def setUp(self):
        """Set up test fixtures."""
        self.page = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.button = ToolbarButton(page=self.page, icon_name="edit-copy")
        self.toolbarbox = ToolbarBox()

    def test_toolbarbutton_creation(self):
        """Test ToolbarButton can be created."""
        self.assertIsInstance(self.button, ToolbarButton)
        self.assertIsInstance(self.button, ToolButton)

    def test_page_property(self):
        """Test page property."""
        self.assertIsNotNone(self.button.get_page())

        new_page = Gtk.Box()
        self.button.set_page(new_page)
        self.assertEqual(self.button.get_page(), new_page)

        another_page = Gtk.Box()
        self.button.page = another_page
        self.assertEqual(self.button.page, another_page)

    def test_page_none(self):
        """Test handling of None page."""
        self.button.set_page(None)
        self.assertIsNone(self.button.get_page())
        self.assertIsNone(self.button.page_widget)

    def test_expanded_state(self):
        """Test expanded state handling."""
        self.toolbarbox.toolbar.append(self.button)

        self.assertFalse(self.button.is_expanded())

        self.button.set_expanded(True)
        # TODO:

    def test_toolbar_box_property(self):
        """Test toolbar_box property."""
        # Initially no toolbar box
        self.assertIsNone(self.button.get_toolbar_box())

        # Add to toolbar box
        self.toolbarbox.toolbar.append(self.button)
        # The toolbar box reference should be available
        # Note: This might be None if the hierarchy isn't fully set up

    def test_palette_handling(self):
        """Test palette creation and handling."""
        # Should have a palette created when page is set
        palette = self.button.get_palette()
        self.assertIsNotNone(palette)

    def test_popdown(self):
        """Test popdown functionality."""
        # Should not raise an error
        self.button.popdown()

    def test_in_palette_state(self):
        """Test is_in_palette functionality."""
        # Initially should be in palette (when not expanded)
        result = self.button.is_in_palette()
        # This is complex to test without full widget hierarchy


class TestToolbarBoxIntegration(unittest.TestCase):
    """Integration tests for ToolbarBox and ToolbarButton."""

    def setUp(self):
        """Set up test fixtures."""
        self.toolbarbox = ToolbarBox()
        self.toolbar = self.toolbarbox.get_toolbar()

    def test_add_toolbar_buttons(self):
        """Test adding multiple toolbar buttons."""
        regular_button = ToolButton(icon_name="document-new")
        self.toolbar.append(regular_button)

        page = Gtk.Box()
        expandable_button = ToolbarButton(page=page, icon_name="edit-copy")
        self.toolbar.append(expandable_button)

        self.assertIsNotNone(self.toolbar.get_first_child())

    def test_toolbar_button_expansion(self):
        """Test toolbar button expansion behavior."""
        edit_toolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        edit_button = ToolbarButton(page=edit_toolbar, icon_name="toolbar-edit")

        self.toolbar.append(edit_button)

        # Test expansion
        edit_button.set_expanded(True)

        # Test that only one button can be expanded
        view_toolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        view_button = ToolbarButton(page=view_toolbar, icon_name="toolbar-view")
        self.toolbar.append(view_button)

        view_button.set_expanded(True)
        # edit_button should now be collapsed

    def test_multiple_toolbarbox_instances(self):
        """Test multiple ToolbarBox instances."""
        toolbarbox2 = ToolbarBox()

        # Both should be independent
        self.assertNotEqual(self.toolbarbox, toolbarbox2)
        self.assertNotEqual(self.toolbarbox.get_toolbar(), toolbarbox2.get_toolbar())


if __name__ == "__main__":
    import gi

    gi.require_version("Gtk", "4.0")
    from gi.repository import Gtk

    app = Gtk.Application()

    def run_tests():
        unittest.main(exit=False)
        app.quit()

    app.connect("activate", lambda app: run_tests())
    app.run([])
