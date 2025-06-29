"""Sugar GTK4 Animator Example """

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
gi.require_version("Gsk", "4.0")
gi.require_version("Graphene", "1.0")
from gi.repository import Gtk, Gdk, Gsk, Graphene

from sugar.activity import SimpleActivity
from sugar.graphics.animator import Animator, Animation, FadeAnimation, ScaleAnimation, MoveAnimation, ColorAnimation

class AnimatorExampleActivity(SimpleActivity):
    """Example activity demonstrating Sugar GTK4 Animator features."""

    def __init__(self):
        super().__init__()
        self.set_title("Sugar GTK4 Animator Example")
        self._create_content()

    def _create_content(self):
        # Apply black text CSS
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(b"""
            * { color: #000000; }
        """)
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        main_box.set_margin_start(20)
        main_box.set_margin_end(20)
        main_box.set_margin_top(20)
        main_box.set_margin_bottom(20)

        # Title
        title = Gtk.Label()
        title.set_markup("<big><b>Sugar GTK4 Animator Example</b></big>")
        main_box.append(title)

        # Animated widget (Gtk.DrawingArea)
        self._color = (0.2, 0.6, 0.9, 1.0)
        self._scale = 1.0
        self._offset = (0, 0)
        self.animated_area = Gtk.DrawingArea()
        self.animated_area.set_content_width(100)
        self.animated_area.set_content_height(100)
        self.animated_area.set_draw_func(self._draw_area)
        self.animated_area.set_halign(Gtk.Align.CENTER)
        self.animated_area.set_valign(Gtk.Align.CENTER)
        main_box.append(self.animated_area)

        # Animation controls
        controls = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        controls.set_halign(Gtk.Align.CENTER)

        fade_btn = Gtk.Button(label="Fade In/Out")
        fade_btn.connect("clicked", self._on_fade)
        controls.append(fade_btn)

        scale_btn = Gtk.Button(label="Scale Up/Down")
        scale_btn.connect("clicked", self._on_scale)
        controls.append(scale_btn)

        move_btn = Gtk.Button(label="Move Box")
        move_btn.connect("clicked", self._on_move)
        controls.append(move_btn)

        color_btn = Gtk.Button(label="Color Animate")
        color_btn.connect("clicked", self._on_color)
        controls.append(color_btn)

        main_box.append(controls)

        # Status label
        self.status_label = Gtk.Label(label="Click a button to animate the box.")
        main_box.append(self.status_label)

        self.set_canvas(main_box)
        self.set_default_size(600, 400)

    def _draw_area(self, area, cr, width, height):
        # Apply translation and scale
        cr.save()
        cr.translate(self._offset[0], self._offset[1])
        cr.scale(self._scale, self._scale)
        # Draw rectangle with current color and opacity
        r, g, b, a = self._color
        cr.set_source_rgba(r, g, b, a)
        cr.rectangle(0, 0, width, height)
        cr.fill()
        cr.restore()

    def _on_fade(self, button):
        """Fade the box in/out."""
        start = self._color[3]
        end = 0.0 if start > 0.5 else 1.0
        animator = Animator(2.0, widget=self.animated_area)
        class Fade(Animation):
            def __init__(self, outer, start, end):
                super().__init__(0.0, 1.0)
                self.outer = outer
                self.start = start
                self.end = end
            def next_frame(self, frame):
                value = self.start + (self.end - self.start) * frame
                r, g, b, _ = self.outer._color
                self.outer._color = (r, g, b, value)
                self.outer.animated_area.queue_draw()
        fade = Fade(self, start, end)
        animator.add(fade)
        animator.connect("completed", lambda *_: self.status_label.set_text("Fade animation completed."))
        animator.start()
        self.status_label.set_text("Fading...")

    def _on_scale(self, button):
        """Scale the box up/down."""
        start = self._scale
        end = 2.0 if abs(start - 1.0) < 0.1 else 1.0
        animator = Animator(1.0, widget=self.animated_area)
        class Scale(Animation):
            def __init__(self, outer, start, end):
                super().__init__(0.0, 1.0)
                self.outer = outer
                self.start = start
                self.end = end
            def next_frame(self, frame):
                value = self.start + (self.end - self.start) * frame
                self.outer._scale = value
                self.outer.animated_area.queue_draw()
        scale = Scale(self, start, end)
        animator.add(scale)
        animator.connect("completed", lambda *_: self.status_label.set_text("Scale animation completed."))
        animator.start()
        self.status_label.set_text("Scaling...")

    def _on_move(self, button):
        """Move the box horizontally (keep it visible)."""
        # Move between 0 and 100 pixels only (animate only x offset)
        start_x = self._offset[0]
        end_x = 100 if start_x < 50 else 0
        animator = Animator(1.0, widget=self.animated_area)
        class Move(Animation):
            def __init__(self, outer, start_x, end_x):
                super().__init__(0.0, 1.0)
                self.outer = outer
                self.start_x = start_x
                self.end_x = end_x
            def next_frame(self, frame):
                value = self.start_x + (self.end_x - self.start_x) * frame
                self.outer._offset = (value, 0)
                self.outer.animated_area.queue_draw()
        move = Move(self, start_x, end_x)
        animator.add(move)
        animator.connect("completed", lambda *_: self.status_label.set_text("Move animation completed."))
        animator.start()
        self.status_label.set_text("Moving...")

    def _on_color(self, button):
        """Animate the box color."""
        # Toggle robustly between two colors
        current = tuple(round(x, 2) for x in self._color[:3])
        color_a = (0.2, 0.6, 0.9, 1.0)
        color_b = (0.9, 0.2, 0.4, 1.0)
        # If current color is close to color_a, animate to color_b, else to color_a
        if all(abs(ca - cc) < 0.05 for ca, cc in zip(color_a[:3], current)):
            end_color = color_b
        else:
            end_color = color_a
        animator = Animator(1.0, widget=self.animated_area)
        class Color(Animation):
            def __init__(self, outer, start_color, end_color):
                super().__init__(0.0, 1.0)
                self.outer = outer
                self.start_color = start_color
                self.end_color = end_color
            def next_frame(self, frame):
                r = self.start_color[0] + (self.end_color[0] - self.start_color[0]) * frame
                g = self.start_color[1] + (self.end_color[1] - self.start_color[1]) * frame
                b = self.start_color[2] + (self.end_color[2] - self.start_color[2]) * frame
                a = self.start_color[3] + (self.end_color[3] - self.start_color[3]) * frame
                self.outer._color = (r, g, b, a)
                self.outer.animated_area.queue_draw()
        color_anim = Color(self, self._color, end_color)
        animator.add(color_anim)
        animator.connect("completed", lambda *_: self.status_label.set_text("Color animation completed."))
        animator.start()
        self.status_label.set_text("Color animating...")

def main():
    """Run the animator example activity."""
    app = Gtk.Application(application_id="org.sugarlabs.AnimatorExample")

    def on_activate(app):
        activity = AnimatorExampleActivity()
        app.add_window(activity)
        activity.present()

    app.connect("activate", on_activate)
    return app.run(sys.argv)

if __name__ == "__main__":
    main()
