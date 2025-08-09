#!/usr/bin/env python3

import dbus
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from sugar.graphics.objectchooser import ObjectChooser, FILTER_TYPE_GENERIC_MIME


def is_journal_service_available():
    bus = dbus.SessionBus()
    try:
        bus.get_object('org.laptop.Journal', '/org/laptop/Journal')
        return True
    except dbus.exceptions.DBusException:
        return False

class ObjectChooserExample(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app, title="ObjectChooser Example")
        self.set_default_size(400, 300)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_margin_top(20)
        vbox.set_margin_bottom(20)
        vbox.set_margin_start(20)
        vbox.set_margin_end(20)
        self.set_child(vbox)

        # Instructions
        label = Gtk.Label(label="Click buttons to open ObjectChooser with different filters")
        label.set_wrap(True)
        vbox.append(label)

        # Button for any object
        btn_any = Gtk.Button(label="Choose Any Object")
        btn_any.connect("clicked", self.on_choose_any)
        vbox.append(btn_any)

        btn_image = Gtk.Button(label="Choose Image")
        btn_image.connect("clicked", self.on_choose_image)
        vbox.append(btn_image)

        self.result_label = Gtk.Label(label="No object selected")
        vbox.append(self.result_label)

    def on_choose_any(self, button):
        self.run_chooser(None, None)

    def on_choose_image(self, button):
        self.run_chooser("image/*", FILTER_TYPE_GENERIC_MIME)

    def run_chooser(self, what_filter, filter_type):
        if not is_journal_service_available():
            self.result_label.set_text(
                "Sugar Journal service is not running.\n"
                "ObjectChooser only works inside the Sugar desktop environment."
            )
            return
        try:
            chooser = ObjectChooser(
                parent=self,
                what_filter=what_filter,
                filter_type=filter_type,
                show_preview=True
            )

            result = chooser.run()

            if result == Gtk.ResponseType.ACCEPT:
                obj = chooser.get_selected_object()
                if obj:
                    title = obj.metadata.get('title', 'Unknown')
                    mime_type = obj.metadata.get('mime_type', 'Unknown')
                    self.result_label.set_text(f"Selected: {title} ({mime_type})")
                    obj.destroy()
                else:
                    self.result_label.set_text("No object returned")
            else:
                self.result_label.set_text("Selection cancelled")

            chooser.destroy()

        except Exception as e:
            self.result_label.set_text(f"Error: {e}")

class ObjectChooserApp(Gtk.Application):
    def do_activate(self):
        window = ObjectChooserExample(self)
        window.present()

if __name__ == "__main__":
    app = ObjectChooserApp()
    app.run()
