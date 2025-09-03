#!/usr/bin/env python3
"""
Simple example demonstrating the Sugar ToggleToolButton widget.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from sugar.graphics.toggletoolbutton import ToggleToolButton
from sugar.graphics.palette import Palette


class ToggleToolButtonExample(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app, title="Sugar ToggleToolButton Example")
        self.set_default_size(400, 200)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_margin_top(10)
        vbox.set_margin_bottom(10)
        vbox.set_margin_start(10)
        vbox.set_margin_end(10)
        self.set_child(vbox)

        # Title
        title = Gtk.Label(label="<b>ToggleToolButton Demo</b>")
        title.set_use_markup(True)
        vbox.append(title)

        # Toolbar
        toolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        vbox.append(toolbar)

        # Bold button
        self.bold_button = ToggleToolButton(icon_name="format-text-bold")
        self.bold_button.set_tooltip("Bold")
        self.bold_button.set_accelerator("<Ctrl>B")
        self.bold_button.connect("toggled", self.on_toggled, "Bold")
        toolbar.append(self.bold_button)

        # Italic button
        self.italic_button = ToggleToolButton(icon_name="format-text-italic")
        self.italic_button.set_tooltip("Italic")
        self.italic_button.set_accelerator("<Ctrl>I")
        self.italic_button.connect("toggled", self.on_toggled, "Italic")
        toolbar.append(self.italic_button)

        # Status
        self.status = Gtk.Label(label="Click buttons or use Ctrl+B/I")
        vbox.append(self.status)

    def on_toggled(self, button, name):
        state = "ON" if button.get_active() else "OFF"
        self.status.set_text(f"{name}: {state}")


class ToggleToolButtonApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="org.sugarlabs.ToggleToolButtonExample")

    def do_activate(self):
        window = ToggleToolButtonExample(self)
        window.present()


def main():
    app = ToggleToolButtonApp()
    return app.run(sys.argv)


if __name__ == "__main__":
    sys.exit(main())
