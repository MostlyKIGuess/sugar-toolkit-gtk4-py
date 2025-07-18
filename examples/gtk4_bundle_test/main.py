#!/usr/bin/env python3
import sys
import os

# hacked for this example
# You must add this where toolkit code actually is
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from sugar.activity import SimpleActivity


class BundleTestActivity(SimpleActivity):
    def __init__(self):
        super().__init__()
        self.set_title("GTK4 Bundle Test Activity")
        label = Gtk.Label(label="Hello from a bundled GTK4 Sugar activity!")
        label.set_margin_top(40)
        label.set_margin_bottom(40)
        label.set_margin_start(40)
        label.set_margin_end(40)
        self.set_canvas(label)


def main():
    app = Gtk.Application(application_id="org.sugarlabs.Gtk4BundleTest")

    def on_activate(app):
        win = BundleTestActivity()
        win.set_application(app)
        win.present()

    app.connect("activate", on_activate)
    return app.run(sys.argv)


if __name__ == "__main__":
    sys.exit(main())
