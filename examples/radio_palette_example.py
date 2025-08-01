"""Sugar GTK4 RadioPalette Example."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from sugar.activity import SimpleActivity
from sugar.graphics.radiopalette import RadioMenuButton, RadioPalette
from sugar.graphics.palette import Palette
from sugar.graphics.toolbutton import ToolButton

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


class RadioPaletteExampleActivity(SimpleActivity):
    """Simple example showing RadioPalette buttons."""

    def __init__(self):
        super().__init__()
        self.set_title("Sugar GTK4 RadioPalette Example")
        self._create_content()

    def _create_content(self):
        """Create the main content."""
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        main_box.set_margin_start(40)
        main_box.set_margin_end(40)
        main_box.set_margin_top(40)
        main_box.set_margin_bottom(40)

        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(b".background { background-color: #e0e0e0; }")
        main_box.get_style_context().add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        main_box.get_style_context().add_class("background")

        # Title
        title = Gtk.Label()
        title.set_markup("<big><b>RadioPalette Demo</b></big>")
        main_box.append(title)

        # Description
        desc = Gtk.Label()
        desc.set_markup("Click the buttons below to see palette dropdowns:")
        main_box.append(desc)

        # Toolbar with buttons
        toolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        toolbar.set_halign(Gtk.Align.CENTER)

        tools_button = RadioMenuButton(
            icon_name=os.path.join(CURSOR_ICONS_PATH, "paintbrush.png"),
            tooltip="Drawing Tools"
        )
        
        # Create the RadioPalette for drawing tools
        tools_palette = RadioPalette(primary_text="Drawing Tools")
        tools_palette.set_secondary_text("Choose your drawing tool")
        
        brush_btn = ToolButton(icon_name=os.path.join(CURSOR_ICONS_PATH, "paintbrush.png"))
        tools_palette.append(brush_btn, "Brush")

        pen_btn = ToolButton(icon_name=os.path.join(CURSOR_ICONS_PATH, "pencil.png"))
        tools_palette.append(pen_btn, "Pencil")

        eraser_btn = ToolButton(icon_name=os.path.join(CURSOR_ICONS_PATH, "eraser.png"))
        tools_palette.append(eraser_btn, "Eraser")

        tools_button.set_palette(tools_palette)
        toolbar.append(tools_button)

        shapes_button = RadioMenuButton(
            icon_name=get_valid_icon(os.path.join(SUGAR_ICONS_PATH, "view-box.svg")),
            tooltip="Shapes"
        )
        shapes_palette = RadioPalette(primary_text="Shape Tools")
        shapes_palette.set_secondary_text("Select a shape to draw")

        rect_btn = ToolButton(icon_name=get_valid_icon(os.path.join(SUGAR_ICONS_PATH, "view-box.svg")))
        shapes_palette.append(rect_btn, "Rectangle")

        circle_btn = ToolButton(icon_name=get_valid_icon(os.path.join(SUGAR_ICONS_PATH, "view-radial.svg")))
        shapes_palette.append(circle_btn, "Circle")

        triangle_btn = ToolButton(icon_name=get_valid_icon(os.path.join(SUGAR_ICONS_PATH, "view-triangle.svg")))
        shapes_palette.append(triangle_btn, "Triangle")

        shapes_button.set_palette(shapes_palette)
        toolbar.append(shapes_button)

        regular_button = ToolButton(
            icon_name=get_valid_icon(os.path.join(SUGAR_ICONS_PATH, "document-save.svg")),
            tooltip="Save (Regular Button)"
        )
        regular_palette = Palette()
        regular_palette.set_primary_text("Regular Palette")
        regular_palette.set_secondary_text("This should work normally")
        regular_button.set_palette(regular_palette)
        toolbar.append(regular_button)

        main_box.append(toolbar)

        # Status
        status = Gtk.Label()
        status.set_markup("<i>RadioPalettes provide dropdown menus with options</i>")
        main_box.append(status)

        self.set_canvas(main_box)
        self.set_default_size(450, 300)


def main():
    """Run the example."""
    app = Gtk.Application(application_id='org.sugarlabs.RadioPaletteExample')

    def on_activate(app):
        activity = RadioPaletteExampleActivity()
        app.add_window(activity)
        activity.present()

    app.connect('activate', on_activate)
    return app.run(sys.argv)


if __name__ == "__main__":
    main()