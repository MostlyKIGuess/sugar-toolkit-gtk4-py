"""
Tray example.
"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(__file__))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk, GLib

from sugar.graphics.tray import HTray, VTray, TrayButton, TrayIcon
from sugar.graphics.xocolor import XoColor


class TrayWindow(Gtk.ApplicationWindow):
    """A small window that showcases horizontal and vertical trays."""

    def __init__(self, app):
        super().__init__(application=app, title="Tray Example")
        self.set_default_size(700, 420)

        outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        outer.set_margin_start(12)
        outer.set_margin_end(12)
        outer.set_margin_top(12)
        outer.set_margin_bottom(12)
        self.set_child(outer)

        label = Gtk.Label()
        label.set_markup("<b>Tray Example</b>\nClick icons or buttons. Use Add/Remove controls.")
        label.set_halign(Gtk.Align.START)
        label.set_valign(Gtk.Align.START)
        outer.append(label)

        hframe = Gtk.Frame(label="Horizontal Tray")
        hbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        hframe.set_child(hbox)
        outer.append(hframe)

        self.htray = HTray()
        self.htray.set_hexpand(True)
        self.htray.set_vexpand(False)
        # Put the tray inside a ScrolledWindow so the scroll buttons work nicely
        scrolled_h = Gtk.ScrolledWindow()
        scrolled_h.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.NEVER)
        scrolled_h.set_child(self.htray)
        scrolled_h.set_hexpand(True)
        scrolled_h.set_vexpand(False)
        hbox.append(scrolled_h)

        controls = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        add_h = Gtk.Button(label="Add H Item")
        add_h.connect("clicked", self._on_add_htray_item)
        controls.append(add_h)
        remove_h = Gtk.Button(label="Remove H Last")
        remove_h.connect("clicked", self._on_remove_htray_item)
        controls.append(remove_h)
        hbox.append(controls)

        vframe = Gtk.Frame(label="Vertical Tray")
        vbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        vframe.set_child(vbox)
        outer.append(vframe)

        self.vtray = VTray()
        self.vtray.set_hexpand(False)
        self.vtray.set_vexpand(True)

        scrolled_v = Gtk.ScrolledWindow()
        scrolled_v.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled_v.set_child(self.vtray)
        scrolled_v.set_hexpand(False)
        scrolled_v.set_vexpand(True)
        vbox.append(scrolled_v)

        vcontrols = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        add_v = Gtk.Button(label="Add V Icon")
        add_v.connect("clicked", self._on_add_vtray_item)
        vcontrols.append(add_v)
        remove_v = Gtk.Button(label="Remove V Last")
        remove_v.connect("clicked", self._on_remove_vtray_item)
        vcontrols.append(remove_v)

        self.vstatus = Gtk.Label(label="No V item clicked yet")
        self.vstatus.set_halign(Gtk.Align.START)
        vcontrols.append(self.vstatus)
        vbox.append(vcontrols)

        self._populate_initial_items()

        self._apply_css()

    def _populate_initial_items(self):
        icons_dir = os.path.join(SRC, "sugar", "graphics", "icons")
        svg_candidates = [
            "checkbox-checked.svg",
            "document-open.svg",
            "go-right.svg",
            "media-playback-start.svg",
            "media-playback-pause.svg",
            "preferences-system.svg",
            "radio-active.svg",
            "system-search.svg",
            "test.svg",
        ]
        for i, name in enumerate(svg_candidates):
            path = os.path.join(icons_dir, name)
            if os.path.exists(path):
                icon = TrayIcon(icon_name=path, xo_color=XoColor.get_random_color())
            else:
                icon = TrayIcon(icon_name="document-open", xo_color=XoColor.get_random_color())
            icon.connect("clicked", self._on_tray_icon_clicked, f"H-Icon-{i}")
            self.htray.add_item(icon)

        v_icons = ["system-search", "media-playback-start", "media-playback-pause"]
        for i, icon_name in enumerate(v_icons):
            icon = TrayIcon(icon_name=icon_name, xo_color=XoColor.get_random_color())
            icon.connect("clicked", self._on_vtray_icon_clicked, f"V-Icon-{i}")
            self.vtray.add_item(icon)

    def _apply_css(self):
        css = """
        label, button {
            color: #000000;
        }
        frame {
            margin: 6px;
        }
        """
        provider = Gtk.CssProvider()
        provider.load_from_data(css.encode())
        display = Gdk.Display.get_default()
        if display:
            Gtk.StyleContext.add_provider_for_display(display, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def _on_tray_icon_clicked(self, widget, info):
        print(f"Horizontal tray icon clicked: {info}")

    def _on_vtray_icon_clicked(self, widget, info):
        self.vstatus.set_text(f"Clicked: {info}")
        print(f"Vertical tray icon clicked: {info}")

    def _on_add_htray_item(self, button):
        count = len(self.htray.get_children())
        tb = TrayButton()
        tb.set_label(f"Btn {count}")
        tb.connect("clicked", self._on_tray_button_clicked, f"H-Btn-{count}")
        self.htray.add_item(tb)

    def _on_remove_htray_item(self, button):
        children = self.htray.get_children()
        if children:
            self.htray.remove_item(children[-1])

    def _on_add_vtray_item(self, button):
        count = len(self.vtray.get_children())
        icon = TrayIcon(icon_name="document-new", xo_color=XoColor.get_random_color())
        icon.connect("clicked", self._on_vtray_icon_clicked, f"V-New-{count}")
        self.vtray.add_item(icon)

    def _on_remove_vtray_item(self, button):
        children = self.vtray.get_children()
        if children:
            self.vtray.remove_item(children[-1])

    def _on_tray_button_clicked(self, widget, info):
        print(f"Tray button clicked: {info}")


def main():
    app = Gtk.Application(application_id="org.example.TrayExample")

    def on_activate(app):
        win = TrayWindow(app)
        app.add_window(win)
        win.present()

    app.connect("activate", on_activate)

    return app.run(sys.argv)


if __name__ == "__main__":
    sys.exit(main())
