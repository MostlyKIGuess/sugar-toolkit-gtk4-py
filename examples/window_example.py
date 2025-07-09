import gi
gi.require_version("Gtk", "4.0")
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from gi.repository import Gtk, GLib, Gdk

from sugar.graphics.window import Window

class ExampleApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="org.sugarlabs.WindowExample")

    def do_activate(self, *args):
        win = Window(application=self)
        win.set_title("Sugar GTK4 Window Example")
        win.set_default_size(700, 500)

        toolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        toolbar.set_margin_top(6)
        toolbar.set_margin_bottom(6)
        toolbar.set_margin_start(6)
        toolbar.set_margin_end(6)

        # Fullscreen button
        fullscreen_btn = Gtk.Button(label="Fullscreen")
        fullscreen_btn.set_tooltip_text("Enter fullscreen mode (Escape to exit)")
        fullscreen_btn.connect("clicked", lambda btn: win.fullscreen())
        toolbar.append(fullscreen_btn)

        # Alert button
        alert_btn = Gtk.Button(label="Show Alert")
        alert_btn.set_tooltip_text("Show an alert overlay")
        alert_btn.connect("clicked", lambda btn: self._show_alert(win))
        toolbar.append(alert_btn)

        win.set_toolbar_box(toolbar)

        label = Gtk.Label(label="Hello, Sugar GTK4 Window!\n\n"
                                "Try:\n"
                                " - Clicking 'Fullscreen' (Escape to exit)\n"
                                " - Clicking 'Show Alert'\n")
        label.set_margin_top(24)
        win.set_canvas(label)

        win.present()

    def _show_alert(self, win):
        alert_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        alert_box.set_margin_top(16)
        alert_box.set_margin_start(16)
        alert_box.set_margin_end(16)
        alert_box.set_margin_bottom(8)
        alert_box.set_valign(Gtk.Align.START)
        alert_box.set_halign(Gtk.Align.FILL)
        alert_box.set_hexpand(True)
        alert_box.set_vexpand(False)
        alert_box.get_style_context().add_class("alert")

        alert_label = Gtk.Label(label="This is an alert overlay! Click Dismiss to remove.")
        alert_label.set_hexpand(True)
        alert_box.append(alert_label)

        dismiss_btn = Gtk.Button(label="Dismiss")
        def on_dismiss(_btn):
            win.remove_alert(alert_box)
        dismiss_btn.connect("clicked", on_dismiss)
        alert_box.append(dismiss_btn)

        win.add_alert(alert_box)

def main():
    app = ExampleApp()
    app.run(None)

if __name__ == "__main__":
    main()
