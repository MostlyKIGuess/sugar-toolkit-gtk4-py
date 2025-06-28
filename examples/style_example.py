"""Sugar GTK4 Style Example - Complete Feature Demo."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from sugar.activity import SimpleActivity
from sugar.graphics import style


class StyleExampleActivity(SimpleActivity):
    """Example activity demonstrating all Sugar GTK4 style features."""

    def __init__(self):
        super().__init__()
        self.set_title("Sugar GTK4 Style Example")
        self._create_content()

    def _create_content(self):
        """Create the main content showing all style features."""
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=style.DEFAULT_SPACING)
        main_box.set_margin_start(style.DEFAULT_PADDING * 2)
        main_box.set_margin_end(style.DEFAULT_PADDING * 2)
        main_box.set_margin_top(style.DEFAULT_PADDING * 2)
        main_box.set_margin_bottom(style.DEFAULT_PADDING * 2)
        main_box.set_hexpand(True)
        main_box.set_vexpand(True)

        # Scrolled window for all content
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_child(main_box)
        scrolled.set_hexpand(True)
        scrolled.set_vexpand(True)

        # Title
        title = Gtk.Label()
        title.set_markup("<big><b>Sugar GTK4 Style System Demo</b></big>")
        title.set_hexpand(True)
        main_box.append(title)

        # Add sections
        self._add_color_section(main_box)
        self._add_font_section(main_box)
        self._add_sizing_section(main_box)
        self._add_css_integration_section(main_box)

        self.set_canvas(scrolled)
        self.set_default_size(800, 600)

    def _add_color_section(self, container):
        """Add color examples."""
        frame = Gtk.Frame(label="Color System")
        frame.set_hexpand(True)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=style.DEFAULT_SPACING)
        vbox.set_margin_start(style.DEFAULT_PADDING)
        vbox.set_margin_end(style.DEFAULT_PADDING)
        vbox.set_margin_top(style.DEFAULT_PADDING)
        vbox.set_margin_bottom(style.DEFAULT_PADDING)

        # Standard colors
        colors_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=style.DEFAULT_SPACING)
        colors_box.set_halign(Gtk.Align.CENTER)

        colors = [
            ("Black", style.COLOR_BLACK),
            ("White", style.COLOR_WHITE),
            ("Primary", style.COLOR_PRIMARY),
            ("Success", style.COLOR_SUCCESS),
            ("Warning", style.COLOR_WARNING),
            ("Error", style.COLOR_ERROR),
        ]

        for name, color in colors:
            color_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
            color_box.set_halign(Gtk.Align.CENTER)

            # Color swatch
            swatch = Gtk.DrawingArea()
            swatch.set_content_width(60)
            swatch.set_content_height(40)
            swatch.set_draw_func(self._draw_color_swatch, color)
            color_box.append(swatch)

            # Color info
            info_label = Gtk.Label(label=f"{name}\n{color.get_html()}")
            info_label.set_justify(Gtk.Justification.CENTER)
            color_box.append(info_label)

            colors_box.append(color_box)

        vbox.append(colors_box)

        # Color methods demo
        demo_color = style.Color("#FF6B35")
        methods_label = Gtk.Label()
        methods_text = f"""Color Methods Demo (using {demo_color.get_html()}):
• HTML: {demo_color.get_html()}
• RGBA: {demo_color.get_rgba()}
• CSS RGBA: {demo_color.get_css_rgba()}
• SVG: {demo_color.get_svg()}
• With Alpha 0.5: {demo_color.with_alpha(0.5).get_css_rgba()}"""
        methods_label.set_text(methods_text)
        methods_label.set_halign(Gtk.Align.START)
        vbox.append(methods_label)

        frame.set_child(vbox)
        container.append(frame)

    def _add_font_section(self, container):
        """Add font examples."""
        frame = Gtk.Frame(label="Font System")
        frame.set_hexpand(True)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=style.DEFAULT_SPACING)
        vbox.set_margin_start(style.DEFAULT_PADDING)
        vbox.set_margin_end(style.DEFAULT_PADDING)
        vbox.set_margin_top(style.DEFAULT_PADDING)
        vbox.set_margin_bottom(style.DEFAULT_PADDING)

        fonts = [
            ("Normal Font", style.FONT_NORMAL),
            ("Bold Font", style.FONT_BOLD),
            ("Italic Font", style.FONT_ITALIC),
        ]

        for name, font in fonts:
            font_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=style.DEFAULT_SPACING)

            label = Gtk.Label(label=f"{name}:")
            label.set_size_request(120, -1)
            font_box.append(label)

            sample = Gtk.Label(label="The quick brown fox jumps over the lazy dog")
            # Apply font using CSS
            css = f"label {{ {font.get_css_string()}; }}"
            style.apply_css_to_widget(sample, css)
            font_box.append(sample)

            vbox.append(font_box)

        # Font information
        info_label = Gtk.Label()
        info_text = f"""Font System Info:
• Font Face: {style.FONT_FACE}
• Font Size: {style.FONT_SIZE}pt
• Zoom Factor: {style.ZOOM_FACTOR:.2f}
• Normal Font Height: {style.FONT_NORMAL_H}px"""
        info_label.set_text(info_text)
        info_label.set_halign(Gtk.Align.START)
        vbox.append(info_label)

        frame.set_child(vbox)
        container.append(frame)

    def _add_sizing_section(self, container):
        """Add sizing and spacing examples."""
        frame = Gtk.Frame(label="Sizing and Spacing")
        frame.set_hexpand(True)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=style.DEFAULT_SPACING)
        vbox.set_margin_start(style.DEFAULT_PADDING)
        vbox.set_margin_end(style.DEFAULT_PADDING)
        vbox.set_margin_top(style.DEFAULT_PADDING)
        vbox.set_margin_bottom(style.DEFAULT_PADDING)

        # Icon sizes
        icon_sizes_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=style.DEFAULT_SPACING)
        icon_sizes_box.set_halign(Gtk.Align.CENTER)

        sizes = [
            ("Small", style.SMALL_ICON_SIZE),
            ("Standard", style.STANDARD_ICON_SIZE),
            ("Medium", style.MEDIUM_ICON_SIZE),
            ("Large", style.LARGE_ICON_SIZE),
        ]

        for name, size in sizes:
            size_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
            size_box.set_halign(Gtk.Align.CENTER)

            # Size demo box
            demo_box = Gtk.DrawingArea()
            demo_box.set_content_width(size)
            demo_box.set_content_height(size)
            demo_box.set_draw_func(self._draw_size_demo, size)
            size_box.append(demo_box)

            # Size label
            size_label = Gtk.Label(label=f"{name}\n{size}px")
            size_label.set_justify(Gtk.Justification.CENTER)
            size_box.append(size_label)

            icon_sizes_box.append(size_box)

        vbox.append(icon_sizes_box)

        # Spacing information
        spacing_info = Gtk.Label()
        spacing_text = f"""Spacing Constants:
• Default Spacing: {style.DEFAULT_SPACING}px
• Default Padding: {style.DEFAULT_PADDING}px
• Grid Cell Size: {style.GRID_CELL_SIZE}px
• Line Width: {style.LINE_WIDTH}px
• Border Radius: {style.BORDER_RADIUS}px"""
        spacing_info.set_text(spacing_text)
        spacing_info.set_halign(Gtk.Align.START)
        vbox.append(spacing_info)

        frame.set_child(vbox)
        container.append(frame)

    def _add_css_integration_section(self, container):
        """Add CSS integration examples."""
        frame = Gtk.Frame(label="GTK4 CSS Integration")
        frame.set_hexpand(True)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=style.DEFAULT_SPACING)
        vbox.set_margin_start(style.DEFAULT_PADDING)
        vbox.set_margin_end(style.DEFAULT_PADDING)
        vbox.set_margin_top(style.DEFAULT_PADDING)
        vbox.set_margin_bottom(style.DEFAULT_PADDING)

        # CSS styled buttons
        buttons_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=style.DEFAULT_SPACING)
        buttons_box.set_halign(Gtk.Align.CENTER)

        button_styles = [
            ("Primary", f"background-color: {style.COLOR_PRIMARY.get_css_rgba()}; color: white; border-radius: {style.BORDER_RADIUS}px;"),
            ("Success", f"background-color: {style.COLOR_SUCCESS.get_css_rgba()}; color: white; border-radius: {style.BORDER_RADIUS}px;"),
            ("Warning", f"background-color: {style.COLOR_WARNING.get_css_rgba()}; color: white; border-radius: {style.BORDER_RADIUS}px;"),
            ("Error", f"background-color: {style.COLOR_ERROR.get_css_rgba()}; color: white; border-radius: {style.BORDER_RADIUS}px;"),
        ]

        for name, css_style in button_styles:
            button = Gtk.Button(label=name)
            css_class = f"{name.lower()}-btn"
            button.add_css_class(css_class)
            style.apply_css_to_widget(button, f".{css_class} {{ {css_style} }}")
            buttons_box.append(button)

        vbox.append(buttons_box)

        # CSS demo explanation
        css_info = Gtk.Label()
        css_text = """CSS Integration Features:
• Color.get_css_rgba() for CSS color values
• Font.get_css_string() for CSS font specifications
• apply_css_to_widget() helper function
• Modern GTK4 styling with CssProvider"""
        css_info.set_text(css_text)
        css_info.set_halign(Gtk.Align.START)
        vbox.append(css_info)

        frame.set_child(vbox)
        container.append(frame)

    def _draw_color_swatch(self, area, cr, width, height, color):
        """Draw a color swatch."""
        rgba = color.get_rgba()
        cr.set_source_rgba(*rgba)
        cr.rectangle(0, 0, width, height)
        cr.fill()

        # Add border
        cr.set_source_rgba(0, 0, 0, 1)
        cr.set_line_width(1)
        cr.rectangle(0, 0, width, height)
        cr.stroke()

    def _draw_size_demo(self, area, cr, width, height, size):
        """Draw a size demonstration box."""
        # Fill with primary color
        rgba = style.COLOR_PRIMARY.get_rgba()
        cr.set_source_rgba(*rgba)
        cr.rectangle(0, 0, width, height)
        cr.fill()

        # Add border
        cr.set_source_rgba(0, 0, 0, 1)
        cr.set_line_width(2)
        cr.rectangle(0, 0, width, height)
        cr.stroke()


def main():
    """Run the style example activity."""
    app = Gtk.Application(application_id='org.sugarlabs.StyleExample')

    def on_activate(app):
        activity = StyleExampleActivity()
        app.add_window(activity)
        activity.present()

    app.connect('activate', on_activate)
    return app.run()


if __name__ == "__main__":
    main()
