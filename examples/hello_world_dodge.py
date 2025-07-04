"""
Hello World Dodge! - Animated Game Demo for sugar-toolkit-gtk4

- Move the "Hello World!" ball with arrow keys, WASD, or buttons.
- Ball moves smoothly, bounces off walls (increasing speed), and changes color.
- Avoid obstacles, reach the goal to score!
- Uses: Toolbox, ToolButton, Icon, XoColor, style

"""

import sys
import os
import random
import math

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
from gi.repository import Gtk, Gdk, GLib

from sugar.activity import SimpleActivity
from sugar.graphics.toolbox import Toolbox
from sugar.graphics.toolbutton import ToolButton
from sugar.graphics.icon import Icon
from sugar.graphics.xocolor import XoColor
from sugar.graphics import style

BALL_RADIUS = 28
GOAL_RADIUS = 20
OBSTACLE_RADIUS = 22
BALL_INIT_SPEED = 3.0
BALL_MAX_SPEED = 50.0
BALL_SPEED_INC = 0.7
OBSTACLE_COUNT = 3

class HelloWorldDodgeActivity(SimpleActivity):
    """Animated Hello World Dodge Game."""

    def __init__(self):
        super().__init__()
        self.set_title("Hello World Dodge!")
        self._create_content()

    def _create_content(self):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(b"""
            * { color: #000000; }
            .game-btn {
                background: #e0e0e0;
                border-radius: 16px;
                border: 2px solid #888;
                padding: 8px 16px;
                margin: 2px;
                transition: background 150ms, border-color 150ms;
            }
            .game-btn:hover {
                background: #b0e0ff;
                border-color: #0077cc;
            }
            .score-label {
                font-weight: bold;
                font-size: 18pt;
            }
            .header-label {
                font-weight: bold;
                font-size: 22pt;
            }
            .instructions-label {
                font-size: 13pt;
                color: #222;
            }
            .center-box {
                margin-left: auto;
                margin-right: auto;
            }
        """)
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(), # type: ignore
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

        # Main vertical box
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=style.DEFAULT_SPACING)
        main_box.set_margin_top(style.DEFAULT_SPACING)
        main_box.set_margin_bottom(style.DEFAULT_SPACING)
        main_box.set_margin_start(style.DEFAULT_SPACING)
        main_box.set_margin_end(style.DEFAULT_SPACING)

        # Instructions
        self.instructions_label = Gtk.Label()
        self.instructions_label.set_wrap(True)
        self.instructions_label.set_justify(Gtk.Justification.CENTER)
        self.instructions_label.set_margin_bottom(style.DEFAULT_SPACING // 2)
        self.instructions_label.set_markup(
            "<span size='large' weight='bold'>How to Play:</span>\n"
            "<span size='medium'>Move the ball with arrow keys, WASD, or the on-screen buttons. "
            "Reach the <b>green</b> goal, avoid <b>red</b> obstacles. "
            "Press <b>Reset</b> to restart. Each wall bounce increases speed!</span>"
        )
        self.instructions_label.get_style_context().add_class("instructions-label")
        main_box.append(self.instructions_label)

        # Welcome and Score
        self.header_label = Gtk.Label()
        self.header_label.set_markup("<span size='xx-large' weight='bold'>Sugar Ball Dodge!</span>")
        self.header_label.set_margin_bottom(style.DEFAULT_SPACING // 2)
        self.header_label.get_style_context().add_class("header-label")
        main_box.append(self.header_label)

        self.score = 0
        self.score_label = Gtk.Label(label="Score: 0")
        self.score_label.set_margin_bottom(style.DEFAULT_SPACING)
        self.score_label.get_style_context().add_class("score-label")
        main_box.append(self.score_label)


        # Ball Name ( Default to Hello World Lol)
        name_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        name_label = Gtk.Label(label="Your Name:")
        self.name_entry = Gtk.Entry()
        self.name_entry.set_placeholder_text("Enter your name")
        self.name_entry.set_max_length(16)
        self.name_entry.set_width_chars(12)
        self.name_entry.set_text("Hello World!")
        self.name_entry.connect("changed", self._on_name_changed)
        name_box.append(name_label)
        name_box.append(self.name_entry)
        main_box.append(name_box)



        # Toolbar with movement buttons, pause, and reset, centered
        toolbox = Toolbox()
        toolbar_outer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        toolbar_outer.set_halign(Gtk.Align.CENTER)
        toolbar_outer.set_hexpand(True)

        toolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=style.DEFAULT_SPACING)
        toolbar.set_halign(Gtk.Align.CENTER)
        toolbar.set_hexpand(False)

        btn_left = ToolButton(tooltip="Left")
        btn_left.set_icon_widget(Icon(icon_name="go-left", pixel_size=36))
        btn_left.get_style_context().add_class("game-btn")
        btn_right = ToolButton(tooltip="Right")
        btn_right.set_icon_widget(Icon(icon_name="go-right", pixel_size=36))
        btn_right.get_style_context().add_class("game-btn")
        btn_up = ToolButton(tooltip="Up")
        btn_up.set_icon_widget(Icon(icon_name="go-up", pixel_size=36))
        btn_up.get_style_context().add_class("game-btn")
        btn_down = ToolButton(tooltip="Down")
        btn_down.set_icon_widget(Icon(icon_name="go-down", pixel_size=36))
        btn_down.get_style_context().add_class("game-btn")
        toolbar.append(btn_left)
        toolbar.append(btn_up)
        toolbar.append(btn_down)
        toolbar.append(btn_right)

        # Pause
        self.btn_pause = ToolButton(tooltip="Pause/Resume")
        self.btn_pause.set_icon_widget(Icon(icon_name="media-playback-pause", pixel_size=36))
        self.btn_pause.get_style_context().add_class("game-btn")
        self.btn_pause.connect("clicked", self._toggle_pause)
        toolbar.append(self.btn_pause)

        # Reset
        btn_reset = ToolButton(tooltip="Reset")
        btn_reset.set_icon_widget(Icon(icon_name="document-open", pixel_size=36))
        btn_reset.get_style_context().add_class("game-btn")
        toolbar.append(btn_reset)

        toolbar_outer.append(toolbar)
        toolbox.add_toolbar("Controls", toolbar_outer)
        main_box.append(toolbox)

        # Main Game Area
        area_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        area_box.set_hexpand(True)
        area_box.set_vexpand(True)
        area_box.set_halign(Gtk.Align.CENTER)
        area_box.set_valign(Gtk.Align.CENTER)

        # Frame
        frame = Gtk.Frame()
        frame.set_margin_top(10)
        frame.set_margin_bottom(10)
        frame.set_margin_start(10)
        frame.set_margin_end(10)

        self.area = Gtk.DrawingArea()
        self.area.set_content_width(800)
        self.area.set_content_height(600)
        self.area.set_hexpand(False)
        self.area.set_vexpand(False)
        self.area.set_halign(Gtk.Align.CENTER)
        self.area.set_valign(Gtk.Align.CENTER)
        self.area.set_draw_func(self._draw_area)
        frame.set_child(self.area)

        # Scrolled Window
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_child(frame)
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_propagate_natural_width(True)
        scrolled.set_propagate_natural_height(True)
        area_box.append(scrolled)
        main_box.append(area_box)

        # Status ( Instructions )
        self.status_label = Gtk.Label(label="Use arrow keys, WASD, or buttons to move the ball! Get the green goal, avoid red obstacles.")
        self.status_label.set_margin_top(style.DEFAULT_SPACING)
        main_box.append(self.status_label)

        self.set_canvas(main_box)
        self.set_default_size(1600, 1100)

        # Ball state
        self.ball_pos = [700.0, 450.0]
        self.ball_radius = BALL_RADIUS
        self.ball_color = XoColor()
        self.ball_text = self.name_entry.get_text()
        self.ball_velocity = [BALL_INIT_SPEED, 0.0]
        self.ball_speed = BALL_INIT_SPEED


        # Goal and obstacles
        self.goal_pos = self._random_pos(GOAL_RADIUS)
        self.obstacles = [self._random_pos(OBSTACLE_RADIUS) for _ in range(OBSTACLE_COUNT)]

        self.animating = False
        self.running = True

        # Keyboard controls
        key_controller = Gtk.EventControllerKey()
        key_controller.connect("key-pressed", self._on_key_pressed)
        self.add_controller(key_controller)

        # Button controls
        btn_left.connect("clicked", lambda b: self._set_direction(-1, 0))
        btn_right.connect("clicked", lambda b: self._set_direction(1, 0))
        btn_up.connect("clicked", lambda b: self._set_direction(0, -1))
        btn_down.connect("clicked", lambda b: self._set_direction(0, 1))
        btn_reset.connect("clicked", lambda b: self._reset_game())


        # Start game loop
        GLib.timeout_add(16, self._game_tick)  # 60 FPS


    def _draw_area(self, area, cr, width, height):
        # Draw goal
        cr.save()
        cr.set_source_rgb(0.2, 0.8, 0.2)
        cr.arc(self.goal_pos[0], self.goal_pos[1], GOAL_RADIUS, 0, 2*math.pi)
        cr.fill()
        cr.restore()

        # Draw obstacles
        for ox, oy in self.obstacles:
            cr.save()
            cr.set_source_rgb(0.85, 0.1, 0.1)
            cr.arc(ox, oy, OBSTACLE_RADIUS, 0, 2*math.pi)
            cr.fill()
            cr.restore()

        # Draw ball with current color and position
        r, g, b = self._hex_to_rgb(self.ball_color.get_fill_color())
        cr.save()
        cr.set_source_rgb(r, g, b)
        cr.arc(self.ball_pos[0], self.ball_pos[1], self.ball_radius, 0, 2*math.pi)
        cr.fill()
        cr.restore()

        # Draw text centered in the ball
        cr.save()
        cr.set_source_rgb(0, 0, 0)
        cr.select_font_face("Sans", 0, 0)
        cr.set_font_size(16)
        text = self.ball_text
        xbearing, ybearing, tw, th, xadv, yadv = cr.text_extents(text)
        cr.move_to(self.ball_pos[0] - tw/2, self.ball_pos[1] + th/2)
        cr.show_text(text)
        cr.restore()

        # Draw boundary rectangle (border)
        cr.save()
        cr.set_line_width(6)
        cr.set_source_rgb(0.2, 0.2, 0.2)
        cr.rectangle(3, 3, width - 6, height - 6)
        cr.stroke()
        cr.restore()


    def _hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i+2], 16)/255.0 for i in (0, 2, 4))

    def _set_direction(self, dx, dy):
        if not self.running:
            return
        speed = self.ball_speed
        norm = math.hypot(dx, dy)
        if norm == 0:
            return
        self.ball_velocity = [speed * dx / norm, speed * dy / norm]

    def _on_name_changed(self, entry):
        self.ball_text = entry.get_text()
        # Pause the game when editing the name
        if self.running:
            self.running = False
            self.btn_pause.set_icon_widget(Icon(icon_name="media-playback-start", pixel_size=36))
            self.status_label.set_text("Paused for name entry. Click on Pause/Resume Button. Press Enter to Finish Typing!")
        self.area.queue_draw()
        # Connect Enter key to remove focus (finish editing)
        entry.connect("activate", self._on_entry_activate)

    def _on_entry_activate(self, entry):
        # Remove focus from entry so user can resume game with keyboard
        entry.get_root().set_focus(None)

    def _toggle_pause(self, button):
        if self.running:
            self.running = False
            self.btn_pause.set_icon_widget(Icon(icon_name="media-playback-start", pixel_size=36))
            self.status_label.set_text("Paused. Click Pause/Resume or press 'p' to continue.")
        else:
            self.running = True
            self.btn_pause.set_icon_widget(Icon(icon_name="media-playback-pause", pixel_size=36))
            self.status_label.set_text("Game resumed!")

    def _on_key_pressed(self, controller, keyval, keycode, state):
        # Only handle keys if name_entry is not focused
        if self.name_entry.has_focus():
            return False
        key = Gdk.keyval_name(keyval)
        if key in ("Left", "a", "A"):
            self._set_direction(-1, 0)
        elif key in ("Right", "d", "D"):
            self._set_direction(1, 0)
        elif key in ("Up", "w", "W"):
            self._set_direction(0, -1)
        elif key in ("Down", "s", "S"):
            self._set_direction(0, 1)
        elif key == "r":
            self._reset_game()
        elif key in ("Return", "KP_Enter", "Enter"):
            self._reset_game()
        elif key in ("p", "P"):
            self._toggle_pause(None)
        return True

    def _random_pos(self, radius):
        # TODO: Make sure they are away from the ball slightly along with velocity accomodation so direct hits are avoided
        width = self.area.get_content_width()
        height = self.area.get_content_height()
        return [
            random.uniform(radius + 10, width - radius - 10),
            random.uniform(radius + 10, height - radius - 10),
        ]

    def _reset_game(self):
        # self.ball_pos = [700.0, 450.0]
        # TODO: start from width half, but this should be random?
        self.ball_pos = [400.0,300.0]
        self.ball_color = XoColor()
        self.ball_velocity = [BALL_INIT_SPEED, 0.0]
        self.ball_speed = BALL_INIT_SPEED
        self.goal_pos = self._random_pos(GOAL_RADIUS)
        self.obstacles = [self._random_pos(OBSTACLE_RADIUS) for _ in range(OBSTACLE_COUNT)]
        self.score = 0
        self.score_label.set_text("Score: 0")
        self.status_label.set_text("Game reset! Use arrows, WASD, or buttons.")
        self.running = True
        self.btn_pause.set_icon_widget(Icon(icon_name="media-playback-pause", pixel_size=36))
        self.area.queue_draw()

    def _game_tick(self):
        if not self.running:
            return True
        width = self.area.get_content_width()
        height = self.area.get_content_height()
        x, y = self.ball_pos
        vx, vy = self.ball_velocity

        # Move ball
        x_new = x + vx
        y_new = y + vy
        bounced = False

        # Bounce off walls, increase speed
        if x_new - self.ball_radius < 0:
            x_new = self.ball_radius
            vx = abs(vx)
            bounced = True
        if x_new + self.ball_radius > width:
            x_new = width - self.ball_radius
            vx = -abs(vx)
            bounced = True
        if y_new - self.ball_radius < 0:
            y_new = self.ball_radius
            vy = abs(vy)
            bounced = True
        if y_new + self.ball_radius > height:
            y_new = height - self.ball_radius
            vy = -abs(vy)
            bounced = True

        if bounced:
            self.ball_speed = min(self.ball_speed + BALL_SPEED_INC, BALL_MAX_SPEED)
            norm = math.hypot(vx, vy)
            if norm > 0:
                vx = self.ball_speed * vx / norm
                vy = self.ball_speed * vy / norm
            self.ball_color = XoColor()
            self.status_label.set_text("Bounced! Speed up!")
        self.ball_pos = [x_new, y_new]
        self.ball_velocity = [vx, vy]

        # Check collision with goal
        if self._distance(self.ball_pos, self.goal_pos) < self.ball_radius + GOAL_RADIUS:
            self.score += 1
            self.score_label.set_text(f"Score: {self.score}")
            self.goal_pos = self._random_pos(GOAL_RADIUS)
            self.status_label.set_text("Goal! +1 Score")
            # Move obstacles too
            self.obstacles = [self._random_pos(OBSTACLE_RADIUS) for _ in range(OBSTACLE_COUNT)]
            self.area.queue_draw()
            # IMP: Return to fix the overlap issue
            return True

        # ONLY after checking goal check obstacles
        for ox, oy in self.obstacles:
            if self._distance(self.ball_pos, [ox, oy]) < self.ball_radius + OBSTACLE_RADIUS:
                self.status_label.set_text("Game Over! Hit an obstacle. Press Reset.")
                self.running = False
                return True

        self.area.queue_draw()
        return True

    def _distance(self, a, b):
        return math.hypot(a[0] - b[0], a[1] - b[1])

def main():
    app = Gtk.Application(application_id="org.sugarlabs.HelloWorldDodge")

    def on_activate(app):
        activity = HelloWorldDodgeActivity()
        app.add_window(activity)
        activity.present()

    app.connect("activate", on_activate)
    return app.run(sys.argv)

if __name__ == "__main__":
    main()
