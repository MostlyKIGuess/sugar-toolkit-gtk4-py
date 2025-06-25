"""Basic Sugar GTK4 Activity Example."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from sugar.activity import SimpleActivity
from sugar.graphics.xocolor import XoColor


class BasicExampleActivity(SimpleActivity):
    """A basic example activity showing Sugar GTK4 features."""

    def __init__(self):
        super().__init__()
        self.set_title("Basic Sugar GTK4 Example")

        self._create_content()

        self._show_color_info()

    def _create_content(self):
        """Create the main content area."""
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        main_box.set_margin_start(20)
        main_box.set_margin_end(20)
        main_box.set_margin_top(20)
        main_box.set_margin_bottom(20)

        # Title
        title = Gtk.Label()
        title.set_markup("<big><b>Welcome to Sugar GTK4!</b></big>")
        main_box.append(title)

        # Description
        desc = Gtk.Label(
            label="This is a basic Sugar activity using GTK4.\n"
            "It demonstrates the new toolkit features."
        )
        desc.set_justify(Gtk.Justification.CENTER)
        main_box.append(desc)

        # Color demo
        color_frame = Gtk.Frame(label="XO Color Demo")
        color_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        color_box.set_margin_start(10)
        color_box.set_margin_end(10)
        color_box.set_margin_top(10)
        color_box.set_margin_bottom(10)

        # Show current XO color
        self.xo_color = XoColor()
        self.color_info_label = Gtk.Label(
            label=f"Current XO Color: {self.xo_color.to_string()}"
        )
        color_box.append(self.color_info_label)

        # Color preview boxes
        color_preview_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        color_preview_box.set_halign(Gtk.Align.CENTER)

        # Stroke color box
        self.stroke_box = Gtk.Box()
        self.stroke_box.set_size_request(100, 50)
        stroke_label = Gtk.Label(label="Stroke")
        stroke_label.set_halign(Gtk.Align.CENTER)
        stroke_label.set_valign(Gtk.Align.CENTER)
        self.stroke_box.append(stroke_label)
        color_preview_box.append(self.stroke_box)

        # Fill color box
        self.fill_box = Gtk.Box()
        self.fill_box.set_size_request(100, 50)
        fill_label = Gtk.Label(label="Fill")
        fill_label.set_halign(Gtk.Align.CENTER)
        fill_label.set_valign(Gtk.Align.CENTER)
        self.fill_box.append(fill_label)
        color_preview_box.append(self.fill_box)

        color_box.append(color_preview_box)

        same_color_label = Gtk.Label(label="Same Color (Stroke & Fill)")
        same_color_label.set_halign(Gtk.Align.CENTER)
        color_box.append(same_color_label)

        self.same_color_area = Gtk.DrawingArea()
        self.same_color_area.set_content_width(100)
        self.same_color_area.set_content_height(50)
        self.same_color_area.set_halign(Gtk.Align.CENTER)
        self.same_color_area.set_valign(Gtk.Align.CENTER)
        self.same_color_area.set_draw_func(self._draw_same_color_box)
        color_box.append(self.same_color_area)

        # Interact with the colors hahahaha
        random_button = Gtk.Button(label="Get Random Color")
        random_button.connect("clicked", self._on_random_color)
        # setting up color as black
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(b"button { color: #000000; }")
        random_button.get_style_context().add_provider(
            css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER
        )
        color_box.append(random_button)

        color_frame.set_child(color_box)
        main_box.append(color_frame)

        info_frame = Gtk.Frame(label="Activity Info")
        info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        info_box.set_margin_start(10)
        info_box.set_margin_end(10)
        info_box.set_margin_top(10)
        info_box.set_margin_bottom(10)

        info_box.append(Gtk.Label(label=f"Activity ID: {self.get_id()[:8]}..."))
        info_box.append(Gtk.Label(label=f"Title: {self.get_title()}"))
        info_box.append(Gtk.Label(label=f"Active: {self.get_active()}"))

        info_frame.set_child(info_box)
        main_box.append(info_frame)

        self.set_canvas(main_box)

    def _show_color_info(self):
        """Display color information in terminal."""
        print(f"Activity Color: {self.xo_color.to_string()}")
        print(f"Stroke: {self.xo_color.get_stroke_color()}")
        print(f"Fill: {self.xo_color.get_fill_color()}")

        rgba = self.xo_color.to_rgba_tuple()
        print(f"RGBA - Stroke: {rgba[0]}, Fill: {rgba[1]}")

    def _draw_same_color_box(self, area, cr, width, height):
        """Draw a rectangle filled with fill color and stroked with stroke color."""
        fill_rgba = self.xo_color.get_fill_color()
        stroke_rgba = self.xo_color.get_stroke_color()
        # Convert hex color to RGB
        fill_rgb = [int(fill_rgba[i : i + 2], 16) / 255.0 for i in (1, 3, 5)]
        stroke_rgb = [int(stroke_rgba[i : i + 2], 16) / 255.0 for i in (1, 3, 5)]
        cr.set_source_rgb(*fill_rgb)
        cr.rectangle(5, 5, width - 10, height - 10)
        cr.fill_preserve()
        cr.set_line_width(4)
        cr.set_source_rgb(*stroke_rgb)
        cr.stroke()

    def _on_random_color(self, button):
        """Handle random color button click."""
        self.xo_color = XoColor.get_random_color()
        self.color_info_label.set_text(f"Current XO Color: {self.xo_color.to_string()}")
        print(f"New random color: {self.xo_color.to_string()}")
        self.same_color_area.queue_draw()


def main():
    """Run the basic example activity."""
    app = Gtk.Application(application_id="org.sugarlabs.BasicExample")

    def on_activate(app):
        activity = BasicExampleActivity()
        app.add_window(activity)
        activity.present()

    app.connect("activate", on_activate)
    return app.run(sys.argv)


if __name__ == "__main__":
    main()
