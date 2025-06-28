"""Sugar GTK4 MenuItem Example - Complete Feature Demo."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gio

from sugar.activity import SimpleActivity
from sugar.graphics.menuitem import MenuItem, MenuSeparator
from sugar.graphics import style
from sugar.graphics.xocolor import XoColor


class MenuItemExampleActivity(SimpleActivity):
    """Example activity demonstrating Sugar GTK4 MenuItem features."""

    def __init__(self):
        super().__init__()
        self.set_title("Sugar GTK4 MenuItem Example")
        self._create_content()

    def _create_content(self):
        """Create the main content with menu examples."""
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=style.DEFAULT_SPACING)
        main_box.set_margin_start(style.DEFAULT_PADDING * 2)
        main_box.set_margin_end(style.DEFAULT_PADDING * 2)
        main_box.set_margin_top(style.DEFAULT_PADDING * 2)
        main_box.set_margin_bottom(style.DEFAULT_PADDING * 2)

        # Title
        title = Gtk.Label()
        title.set_markup("<big><b>Sugar GTK4 MenuItem Demo</b></big>")
        title.set_margin_bottom(style.DEFAULT_SPACING)
        main_box.append(title)

        # Create menu sections
        self._create_basic_menu_section(main_box)
        self._create_popover_menu_section(main_box)
        self._create_accelerator_section(main_box)

        # Status label
        self._status_label = Gtk.Label(label="Click menu items to see their actions")
        self._status_label.set_margin_top(style.DEFAULT_SPACING)
        main_box.append(self._status_label)

        self.set_canvas(main_box)
        self.set_default_size(600, 500)

        # Make all menu item text black with even more specific CSS
        css = """
button.menuitem, button.menuitem label,
button.menuitem:focus, button.menuitem:active, button.menuitem:hover,
button.menuitem:focus label, button.menuitem:active label, button.menuitem:hover label {
    color: #000000 !important;
}
"""
        style.apply_css_to_widget(self, css)

    def _create_basic_menu_section(self, container):
        """Create basic menu items section."""
        frame = Gtk.Frame(label="Basic Menu Items")
        frame.set_margin_bottom(style.DEFAULT_SPACING)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        vbox.set_margin_start(style.DEFAULT_PADDING)
        vbox.set_margin_end(style.DEFAULT_PADDING)
        vbox.set_margin_top(style.DEFAULT_PADDING)
        vbox.set_margin_bottom(style.DEFAULT_PADDING)

        # Text-only menu item
        text_item = MenuItem(text_label="Text Only Item")
        text_item.connect("clicked", self._on_menu_item_clicked, "Text Only Item")
        vbox.append(text_item)

        # Icon with text
        icon_item = MenuItem(text_label="New Document", icon_name="document-new")
        icon_item.connect("clicked", self._on_menu_item_clicked, "New Document")
        vbox.append(icon_item)

        # Icon with XO color
        xo_color = XoColor("#FF0000,#00FF00")
        colored_item = MenuItem(
            text_label="Colored Icon Item",
            icon_name="emblem-favorite",
            xo_color=xo_color
        )
        colored_item.connect("clicked", self._on_menu_item_clicked, "Colored Icon")
        vbox.append(colored_item)

        # Separator
        vbox.append(MenuSeparator())

        # Long text with ellipsizing
        long_item = MenuItem(
            text_label="This is a very long menu item text that should be ellipsized",
            icon_name="dialog-information",
            text_maxlen=30
        )
        long_item.connect("clicked", self._on_menu_item_clicked, "Long Text Item")
        vbox.append(long_item)

        frame.set_child(vbox)
        container.append(frame)

    def _create_popover_menu_section(self, container):
        """Create popover menu section."""
        frame = Gtk.Frame(label="Popover Menu")
        frame.set_margin_bottom(style.DEFAULT_SPACING)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        vbox.set_margin_start(style.DEFAULT_PADDING)
        vbox.set_margin_end(style.DEFAULT_PADDING)
        vbox.set_margin_top(style.DEFAULT_PADDING)
        vbox.set_margin_bottom(style.DEFAULT_PADDING)

        # Button to show popover
        label = Gtk.Label(label="Show Popover Menu")
        style.apply_css_to_widget(label, "label { color: #000000; }")
        popover_button = Gtk.MenuButton()
        popover_button.set_child(label)

        # Create popover with menu items
        popover = Gtk.Popover()
        popover_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        popover_box.set_margin_start(6)
        popover_box.set_margin_end(6)
        popover_box.set_margin_top(6)
        popover_box.set_margin_bottom(6)

        # Add menu items to popover
        items = [
            ("Open", "document-open"),
            ("Save", "document-save"),
            ("Save As", "document-save-as"),
            (None, None),  # Separator
            ("Preferences", "preferences-system"),
            ("About", "help-about"),
        ]

        for text, icon in items:
            if text is None:
                popover_box.append(MenuSeparator())
            else:
                item = MenuItem(text_label=text, icon_name=icon)
                item.connect("clicked", self._on_popover_item_clicked, text, popover)
                popover_box.append(item)

        popover.set_child(popover_box)
        popover_button.set_popover(popover)

        vbox.append(popover_button)
        frame.set_child(vbox)
        container.append(frame)

    def _create_accelerator_section(self, container):
        """Create accelerator demonstration section."""
        frame = Gtk.Frame(label="Keyboard Accelerators")

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        vbox.set_margin_start(style.DEFAULT_PADDING)
        vbox.set_margin_end(style.DEFAULT_PADDING)
        vbox.set_margin_top(style.DEFAULT_PADDING)
        vbox.set_margin_bottom(style.DEFAULT_PADDING)

        # Info label
        info_label = Gtk.Label()
        info_label.set_markup("<i>Try pressing the keyboard shortcuts:</i>")
        info_label.set_halign(Gtk.Align.START)
        vbox.append(info_label)

        # Menu items with accelerators
        accelerator_items = [
            ("New", "document-new", "<Ctrl>n"),
            ("Open", "document-open", "<Ctrl>o"),
            ("Save", "document-save", "<Ctrl>s"),
            ("Quit", "application-exit", "<Ctrl>q"),
        ]

        for text, icon, accel in accelerator_items:
            item = MenuItem(text_label=f"{text} ({accel})", icon_name=icon)
            item.set_accelerator(accel)
            item.connect("clicked", self._on_accelerator_item_clicked, text)
            vbox.append(item)

        frame.set_child(vbox)
        container.append(frame)

    def _on_menu_item_clicked(self, item, item_name):
        """Handle basic menu item clicks."""
        self._status_label.set_text(f"Clicked: {item_name}")

    def _on_popover_item_clicked(self, item, item_name, popover):
        """Handle popover menu item clicks."""
        self._status_label.set_text(f"Popover item clicked: {item_name}")
        popover.popdown()

    def _on_accelerator_item_clicked(self, item, item_name):
        """Handle accelerator menu item clicks."""
        self._status_label.set_text(f"Accelerator activated: {item_name}")
        if item_name == "Quit":
            self.close()


def main():
    """Run the MenuItem example activity."""
    # Create application with proper ID
    app = Gtk.Application(application_id='org.sugarlabs.MenuItemExample')

    def on_activate(app):
        activity = MenuItemExampleActivity()
        app.add_window(activity)
        activity.present()

    app.connect('activate', on_activate)
    return app.run()


if __name__ == "__main__":
    main()
