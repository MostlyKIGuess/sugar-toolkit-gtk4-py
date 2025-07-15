"""
Simple PaletteGroup Example
"""

import gi
gi.require_version('Gtk', '4.0')

from gi.repository import Gtk, GObject
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from sugar.graphics.palettegroup import get_group, popdown_all


class MockPalette(Gtk.Box):
    """Simple mock palette for demonstration."""

    def __init__(self, name):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self.name = name
        self._is_up = False
        self.palette_state = "invoker"

        # Add some content
        label = Gtk.Label(label=f"Palette: {name}")
        self.append(label)

    def is_up(self):
        return self._is_up

    def popdown(self, immediate=False):
        if self._is_up:
            self._is_up = False
            self.emit('popdown')
            print(f"{self.name} popped down")

    def popup(self):
        if not self._is_up:
            self._is_up = True
            self.emit('popup')
            print(f"{self.name} popped up")


# Register signals for MockPalette
GObject.type_register(MockPalette)
GObject.signal_new('popup', MockPalette, GObject.SignalFlags.RUN_FIRST, None, ())
GObject.signal_new('popdown', MockPalette, GObject.SignalFlags.RUN_FIRST, None, ())


class PaletteGroupExample(Gtk.ApplicationWindow):

    def __init__(self, app):
        super().__init__(application=app)
        self.set_title("PaletteGroup Example")
        self.set_default_size(400, 300)

        # Create palettes
        self.palette1 = MockPalette("Palette 1")
        self.palette2 = MockPalette("Palette 2")
        self.palette3 = MockPalette("Palette 3")

        # Add to group
        group = get_group('test_group')
        group.add(self.palette1)
        group.add(self.palette2)
        group.add(self.palette3)

        # Connect to group signals
        group.connect('popup', self._on_group_popup)
        group.connect('popdown', self._on_group_popdown)

        self._setup_ui()

    def _setup_ui(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        box.set_margin_top(20)
        box.set_margin_bottom(20)
        box.set_margin_start(20)
        box.set_margin_end(20)

        # Buttons to show palettes
        btn1 = Gtk.Button(label="Show Palette 1")
        btn1.connect('clicked', lambda b: self.palette1.popup())

        btn2 = Gtk.Button(label="Show Palette 2")
        btn2.connect('clicked', lambda b: self.palette2.popup())

        btn3 = Gtk.Button(label="Show Palette 3")
        btn3.connect('clicked', lambda b: self.palette3.popup())

        # Control button
        popdown_btn = Gtk.Button(label="Pop Down All")
        popdown_btn.connect('clicked', lambda b: popdown_all())

        box.append(btn1)
        box.append(btn2)
        box.append(btn3)
        box.append(popdown_btn)

        self.set_child(box)

    def _on_group_popup(self, group):
        print("Group popped up")

    def _on_group_popdown(self, group):
        print("Group popped down")


class PaletteGroupApp(Gtk.Application):

    def __init__(self):
        super().__init__(application_id='org.sugarlabs.PaletteGroupExample')

    def do_activate(self):
        window = PaletteGroupExample(self)
        window.present()


def main():
    app = PaletteGroupApp()
    return app.run(sys.argv)


if __name__ == "__main__":
    main()
