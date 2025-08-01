"""Sugar GTK4 RadioToolButton Example."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from sugar.activity import SimpleActivity
from sugar.graphics.radiotoolbutton import RadioToolButton
from sugar.graphics.toolbutton import ToolButton
from sugar.graphics import style

PROJECT_ROOT = os.path.join(os.path.dirname(__file__), "..")
SUGAR_ICONS_PATH = os.path.join(PROJECT_ROOT, "sugar-artwork", "icons", "scalable", "actions")
CURSOR_ICONS_PATH = os.path.join(PROJECT_ROOT, "sugar-artwork", "cursor", "sugar", "pngs")


def get_valid_icon(icon_path, fallback="document-generic.svg"):
    if os.path.exists(icon_path):
        return icon_path
    else:
        # Try fallback in mimetypes directory
        fallback_path = os.path.join(PROJECT_ROOT, "sugar-artwork", "icons", "scalable", "mimetypes", fallback)
        if os.path.exists(fallback_path):
            return fallback_path
        # Fallback to actions directory if mimetypes fallback missing
        return os.path.join(SUGAR_ICONS_PATH, fallback)


class RadioToolButtonExampleActivity(SimpleActivity):
    """Example activity demonstrating Sugar GTK4 RadioToolButton features."""

    def __init__(self):
        super().__init__()
        self.set_title("Sugar GTK4 RadioToolButton Example")
        self._create_content()

    def _create_content(self):
        """Create the main content showing radio tool button features."""
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=style.DEFAULT_SPACING)
        main_box.set_margin_start(style.DEFAULT_PADDING * 2)
        main_box.set_margin_end(style.DEFAULT_PADDING * 2)
        main_box.set_margin_top(style.DEFAULT_PADDING * 2)
        main_box.set_margin_bottom(style.DEFAULT_PADDING * 2)

        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(b".background { background-color: #e0e0e0; }")
        main_box.get_style_context().add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        main_box.get_style_context().add_class("background")

        # Title
        title = Gtk.Label()
        title.set_markup("<big><b>RadioToolButton Demo</b></big>")
        title.set_margin_bottom(style.DEFAULT_SPACING)
        main_box.append(title)

        # Description
        desc = Gtk.Label()
        desc.set_markup("Radio buttons work in groups - only one can be selected at a time.")
        desc.set_margin_bottom(style.DEFAULT_SPACING)
        main_box.append(desc)

        # Drawing tools section
        self._create_tools_section(main_box)

        # View modes section  
        self._create_modes_section(main_box)

        # Status label
        self._status_label = Gtk.Label(label="Select a tool to see its action")
        self._status_label.set_margin_top(style.DEFAULT_SPACING)
        main_box.append(self._status_label)

        self.set_canvas(main_box)
        self.set_default_size(500, 350)

    def _create_tools_section(self, container):
        """Create drawing tools radio button section."""
        frame = Gtk.Frame(label="Drawing Tools")
        frame.set_margin_bottom(style.DEFAULT_SPACING)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        vbox.set_margin_start(style.DEFAULT_PADDING)
        vbox.set_margin_end(style.DEFAULT_PADDING)
        vbox.set_margin_top(style.DEFAULT_PADDING)
        vbox.set_margin_bottom(style.DEFAULT_PADDING)

        # Create toolbar for tools
        toolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        toolbar.set_halign(Gtk.Align.CENTER)

        # Drawing tools with file paths
        tools = [
            ("Brush", os.path.join(CURSOR_ICONS_PATH, "paintbrush.png")),
            ("Pencil", os.path.join(CURSOR_ICONS_PATH, "pencil.png")),
            ("Eraser", os.path.join(CURSOR_ICONS_PATH, "eraser.png")),
            ("Text", get_valid_icon(os.path.join(SUGAR_ICONS_PATH, "format-text-bold.svg"))),
        ]

        first_tool = None
        for i, (name, icon_path) in enumerate(tools):
            if i == 0:
                tool_button = RadioToolButton(icon_name=icon_path)
                first_tool = tool_button
                tool_button.set_active(True)
            else:
                tool_button = RadioToolButton(icon_name=icon_path, group=first_tool)
            
            tool_button.set_tooltip(name)
            tool_button.connect('toggled', self._on_tool_toggled, name)
            toolbar.append(tool_button)

        vbox.append(toolbar)
        frame.set_child(vbox)
        container.append(frame)

    def _create_modes_section(self, container):
        """Create view modes section."""
        frame = Gtk.Frame(label="View Modes")
        frame.set_margin_bottom(style.DEFAULT_SPACING)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        vbox.set_margin_start(style.DEFAULT_PADDING)
        vbox.set_margin_end(style.DEFAULT_PADDING)
        vbox.set_margin_top(style.DEFAULT_PADDING)
        vbox.set_margin_bottom(style.DEFAULT_PADDING)

        toolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        toolbar.set_halign(Gtk.Align.CENTER)

        # View modes with file paths
        modes = [
            ("List", get_valid_icon(os.path.join(SUGAR_ICONS_PATH, "view-list.svg"))),
            ("Grid", get_valid_icon(os.path.join(SUGAR_ICONS_PATH, "view-box.svg"))),
            ("Details", get_valid_icon(os.path.join(SUGAR_ICONS_PATH, "view-details.svg"))),
        ]

        first_mode = None
        for i, (name, icon_path) in enumerate(modes):
            if i == 0:
                mode_button = RadioToolButton(icon_name=icon_path)
                first_mode = mode_button
                mode_button.set_active(True)
            else:
                mode_button = RadioToolButton(icon_name=icon_path, group=first_mode)
            
            mode_button.set_tooltip(f"{name} View")
            mode_button.connect('toggled', self._on_mode_toggled, name)
            toolbar.append(mode_button)

        vbox.append(toolbar)
        frame.set_child(vbox)
        container.append(frame)

    def _on_tool_toggled(self, button, tool_name):
        """Handle drawing tool toggle."""
        if button.get_active():
            self._status_label.set_text(f"Selected tool: {tool_name}")

    def _on_mode_toggled(self, button, mode_name):
        """Handle view mode toggle."""
        if button.get_active():
            self._status_label.set_text(f"Selected view: {mode_name}")


def main():
    """Run the RadioToolButton example activity."""
    app = Gtk.Application(application_id='org.sugarlabs.RadioToolButtonExample')

    def on_activate(app):
        activity = RadioToolButtonExampleActivity()
        app.add_window(activity)
        activity.present()

    app.connect('activate', on_activate)
    return app.run(sys.argv)


if __name__ == "__main__":
    main()