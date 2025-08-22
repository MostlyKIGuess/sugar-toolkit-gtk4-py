"""
Creative Studio Activity Example
================================

This example demonstrates an advanced Sugar creative activity featuring:
- Multiple creative tools (drawing, text, shapes)
- Keyboard shortcuts (Ctrl+Z/Y/S)
- Color selection with visual feedback
- File operations with auto-save
- Preview generation
- Flexible creative workspace
"""

import os
import sys
import logging
import json
import tempfile
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

# Set up mock environment if not running in Sugar
if 'SUGAR_BUNDLE_ID' not in os.environ:
    os.environ['SUGAR_BUNDLE_ID'] = 'org.sugarlabs.CreativeStudio'
    os.environ['SUGAR_BUNDLE_NAME'] = 'Creative Studio'
    os.environ['SUGAR_BUNDLE_PATH'] = os.path.dirname(__file__)
    os.environ['SUGAR_ACTIVITY_ROOT'] = '/tmp/creative_studio'

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")

from gi.repository import Gtk,  Gio, Gdk

from sugar.activity.activity import Activity
from sugar.activity.activityhandle import ActivityHandle
from sugar.graphics.toolbarbox import ToolbarBox
from sugar.activity.widgets import ActivityToolbarButton, StopButton


class CreativeCanvas(Gtk.DrawingArea):
    """A versatile creative canvas supporting multiple tools and media."""

    def __init__(self):
        super().__init__()
        self.set_size_request(800, 600)
        self.set_draw_func(self._draw_func)
        self.set_focusable(True)

        # Set up gesture for drawing
        self._gesture = Gtk.GestureDrag()
        self._gesture.connect('drag-begin', self._drag_begin_cb)
        self._gesture.connect('drag-update', self._drag_update_cb)
        self._gesture.connect('drag-end', self._drag_end_cb)
        self.add_controller(self._gesture)

        # Set up key controller for keyboard shortcuts
        self._key_controller = Gtk.EventControllerKey()
        self._key_controller.connect('key-pressed', self._key_pressed_cb)
        self.add_controller(self._key_controller)

        # Make sure canvas can receive focus for keyboard events
        self.set_can_focus(True)

        self._elements = []  # All creative elements (strokes, text, shapes, etc.)
        self._current_stroke = []

        self._current_color = (0, 0, 0)  # Black
        self._current_brush_size = 3
        self._current_tool = "brush"  # brush, eraser, line, rectangle, circle, spray
        self._current_fill = False  # Whether shapes should be filled

        # Undo/Redo stacks
        self._undo_stack = []
        self._redo_stack = []

        self._on_change_callback = None

    def set_change_callback(self, callback):
        """Set callback function to call when canvas changes."""
        self._on_change_callback = callback

    def _notify_change(self):
        """Notify that canvas has changed."""
        if self._on_change_callback:
            self._on_change_callback()

    def _key_pressed_cb(self, controller, keyval, keycode, state):
        """Handle keyboard shortcuts."""
        # Check for Ctrl key
        if state & Gdk.ModifierType.CONTROL_MASK:
            if keyval == Gdk.KEY_z or keyval == Gdk.KEY_Z:
                if self.undo():
                    print("Undo triggered by keyboard")
                return True
            elif keyval == Gdk.KEY_y or keyval == Gdk.KEY_Y:
                if self.redo():
                    print("Redo triggered by keyboard")
                return True
            elif keyval == Gdk.KEY_s or keyval == Gdk.KEY_S:
                # Trigger save through callback
                if hasattr(self, '_save_callback') and self._save_callback:
                    self._save_callback()
                    print("Save triggered by keyboard")
                return True
        return False

    def set_save_callback(self, callback):
        """Set callback for save shortcut."""
        self._save_callback = callback

    def _draw_func(self, area, cr, width, height, user_data=None):
        """Draw the canvas content."""
        cr.set_source_rgb(1, 1, 1)  # White background
        cr.paint()

        for element in self._elements:
            self._draw_element(cr, element)

        # Draw current stroke being created
        if self._current_stroke:
            self._draw_current_stroke(cr)

    def _draw_element(self, cr, element):
        element_type = element.get('type', 'stroke')
        color = element.get('color', (0, 0, 0))
        size = element.get('size', 3)
        points = element.get('points', [])

        cr.set_source_rgb(*color)
        cr.set_line_width(size)

        if element_type == 'brush':
            if len(points) > 1:
                cr.move_to(points[0][0], points[0][1])
                for point in points[1:]:
                    cr.line_to(point[0], point[1])
                cr.stroke()

        elif element_type == 'eraser':
            # Eraser removes content by painting white with a thicker line
            cr.set_source_rgb(1, 1, 1)  # White for eraser
            cr.set_line_width(size * 3)  # Make eraser more visible/effective
            cr.set_line_cap(1)  # Round line caps
            cr.set_line_join(1)  # Round line joins
            if len(points) > 1:
                cr.move_to(points[0][0], points[0][1])
                for point in points[1:]:
                    cr.line_to(point[0], point[1])
                cr.stroke()

        elif element_type == 'line':
            if len(points) >= 2:
                cr.move_to(points[0][0], points[0][1])
                cr.line_to(points[-1][0], points[-1][1])
                cr.stroke()

        elif element_type == 'rectangle':
            if len(points) >= 2:
                x1, y1 = points[0]
                x2, y2 = points[-1]
                width = abs(x2 - x1)
                height = abs(y2 - y1)
                x = min(x1, x2)
                y = min(y1, y2)

                if element.get('fill', False):
                    cr.rectangle(x, y, width, height)
                    cr.fill()
                else:
                    cr.rectangle(x, y, width, height)
                    cr.stroke()

        elif element_type == 'circle':
            if len(points) >= 2:
                x1, y1 = points[0]
                x2, y2 = points[-1]
                radius = ((x2-x1)**2 + (y2-y1)**2)**0.5

                if element.get('fill', False):
                    cr.arc(x1, y1, radius, 0, 2 * 3.14159)
                    cr.fill()
                else:
                    cr.arc(x1, y1, radius, 0, 2 * 3.14159)
                    cr.stroke()

    def _draw_current_stroke(self, cr):
        """Draw the stroke currently being created."""
        cr.set_source_rgb(*self._current_color)
        cr.set_line_width(self._current_brush_size)

        if self._current_tool == 'eraser':
            cr.set_source_rgb(1, 1, 1)
            cr.set_line_width(self._current_brush_size * 3)
            cr.set_line_cap(1)  # Round line caps
            cr.set_line_join(1)  # Round line joins

        if self._current_tool in ['brush', 'eraser'] and len(self._current_stroke) > 1:
            cr.move_to(self._current_stroke[0][0], self._current_stroke[0][1])
            for point in self._current_stroke[1:]:
                cr.line_to(point[0], point[1])
            cr.stroke()
        elif self._current_tool == 'line' and len(self._current_stroke) >= 2:
            cr.move_to(self._current_stroke[0][0], self._current_stroke[0][1])
            cr.line_to(self._current_stroke[-1][0], self._current_stroke[-1][1])
            cr.stroke()
        elif self._current_tool == 'rectangle' and len(self._current_stroke) >= 2:
            x1, y1 = self._current_stroke[0]
            x2, y2 = self._current_stroke[-1]
            width = abs(x2 - x1)
            height = abs(y2 - y1)
            x = min(x1, x2)
            y = min(y1, y2)
            cr.rectangle(x, y, width, height)
            if self._current_fill:
                cr.fill()
            else:
                cr.stroke()
        elif self._current_tool == 'circle' and len(self._current_stroke) >= 2:
            x1, y1 = self._current_stroke[0]
            x2, y2 = self._current_stroke[-1]
            radius = ((x2-x1)**2 + (y2-y1)**2)**0.5
            cr.arc(x1, y1, radius, 0, 2 * 3.14159)
            if self._current_fill:
                cr.fill()
            else:
                cr.stroke()

    def _drag_begin_cb(self, gesture, x, y):
        """Start a new creative action."""
        self._current_stroke = [(x, y)]
        self.queue_draw()

    def _drag_update_cb(self, gesture, x, y):
        """Continue the current action."""
        result = gesture.get_start_point()
        if len(result) == 3:
            valid, start_x, start_y = result
            if valid:
                current_x = start_x + x
                current_y = start_y + y
                if self._current_tool in ['brush', 'eraser']:
                    # For freehand tools, add all points
                    self._current_stroke.append((current_x, current_y))
                else:
                    # For shape tools, only keep start and current point
                    if len(self._current_stroke) == 1:
                        self._current_stroke.append((current_x, current_y))
                    else:
                        self._current_stroke[-1] = (current_x, current_y)
                self.queue_draw()

    def _drag_end_cb(self, gesture, x, y):
        """Finish the current action."""
        if self._current_stroke:
            self._save_state()

            element_data = {
                'type': self._current_tool,
                'points': self._current_stroke[:],
                'color': self._current_color,
                'size': self._current_brush_size,
                'fill': self._current_fill,
                'timestamp': datetime.now().isoformat()
            }

            self._elements.append(element_data)
            self._current_stroke = []

            # Clear redo stack
            self._redo_stack = []

            self.queue_draw()
            self._notify_change()

    def _save_state(self):
        """Save current state for undo."""
        state = [element.copy() for element in self._elements]
        self._undo_stack.append(state)
        # Limit undo stack size
        if len(self._undo_stack) > 50:
            self._undo_stack.pop(0)

    def set_color(self, color):
        """Set the current color."""
        self._current_color = color

    def set_brush_size(self, size):
        """Set the brush size."""
        self._current_brush_size = size

    def set_tool(self, tool):
        """Set the current tool."""
        self._current_tool = tool

    def set_fill_mode(self, fill):
        """Set whether shapes should be filled."""
        self._current_fill = fill

    def clear_canvas(self):
        """Clear all content."""
        self._save_state()
        self._elements = []
        self._current_stroke = []
        self._redo_stack = []
        self.queue_draw()
        self._notify_change()

    def undo(self):
        """Undo last action."""
        if self._undo_stack:
            # Save current state to redo stack
            current_state = [element.copy() for element in self._elements]
            self._redo_stack.append(current_state)

            # Restore previous state
            self._elements = self._undo_stack.pop()
            self.queue_draw()
            self._notify_change()
            return True
        return False

    def redo(self):
        """Redo last undone action."""
        if self._redo_stack:
            # Save current state to undo stack
            current_state = [element.copy() for element in self._elements]
            self._undo_stack.append(current_state)

            # Restore redone state
            self._elements = self._redo_stack.pop()
            self.queue_draw()
            self._notify_change()
            return True
        return False

    def get_canvas_data(self):
        """Get all canvas data for saving."""
        return {
            'elements': self._elements,
            'canvas_size': (self.get_width(), self.get_height()),
            'version': '2.0'
        }

    def set_canvas_data(self, data):
        """Set canvas data from saved file."""
        self._elements = data.get('elements', [])
        self._current_stroke = []
        self._undo_stack = []
        self._redo_stack = []
        self.queue_draw()


class CreativeStudioActivity(Activity):
    """An advanced creative studio Sugar activity."""

    def __init__(self, handle=None, application=None):
        """Initialize the activity."""
        # Create handle if not provided (for testing)
        if handle is None:
            handle = ActivityHandle('creative-studio-123')

        Activity.__init__(self, handle, application=application)

        self._initialize_document_data()

        self._current_tool = "brush"
        self._canvas_size = (800, 600)
        self._preview_image_path = None
        self._current_color = (0, 0, 0)
        self._has_unsaved_changes = False

        self._color_buttons = {}

        self._setup_ui()

        self.set_title("Creative Studio")
        self.set_default_size(1200, 800)

    def _initialize_document_data(self):
        """Initialize document metadata."""
        self._document_data = {
            'created': datetime.now().isoformat(),
            'modified': datetime.now().isoformat(),
            'version': '2.0',
            'author': 'Creative User',
            'title': 'Untitled Creation',
            'element_count': 0,
            'last_tool': 'brush'
        }

    def _setup_ui(self):
        """Set up the user interface."""
        self._create_toolbar()
        self._create_canvas()

    def _create_toolbar(self):
        """Create the activity toolbar with creative tools."""
        toolbar_box = ToolbarBox()

        # Activity button
        activity_button = ActivityToolbarButton(self)
        toolbar_box.toolbar.append(activity_button)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        toolbar_box.toolbar.append(separator)

        # Tool selection
        tools_label = Gtk.Label()
        tools_label.set_markup("<span color='white' weight='bold'>Tools:</span>")
        toolbar_box.toolbar.append(tools_label)

        # Brush tool
        brush_btn = Gtk.ToggleButton()
        brush_btn.set_label("Brush")
        brush_btn.set_active(True)
        brush_btn.connect('toggled', lambda btn: self._tool_selected(btn, 'brush'))
        toolbar_box.toolbar.append(brush_btn)
        self._brush_btn = brush_btn

        # Eraser tool
        eraser_btn = Gtk.ToggleButton()
        eraser_btn.set_label("Eraser")
        eraser_btn.connect('toggled', lambda btn: self._tool_selected(btn, 'eraser'))
        toolbar_box.toolbar.append(eraser_btn)
        self._eraser_btn = eraser_btn

        # Line tool
        line_btn = Gtk.ToggleButton()
        line_btn.set_label("Line")
        line_btn.connect('toggled', lambda btn: self._tool_selected(btn, 'line'))
        toolbar_box.toolbar.append(line_btn)
        self._line_btn = line_btn

        # Rectangle tool
        rect_btn = Gtk.ToggleButton()
        rect_btn.set_label("Rectangle")
        rect_btn.connect('toggled', lambda btn: self._tool_selected(btn, 'rectangle'))
        toolbar_box.toolbar.append(rect_btn)
        self._rect_btn = rect_btn

        # Circle tool
        circle_btn = Gtk.ToggleButton()
        circle_btn.set_label("Circle")
        circle_btn.connect('toggled', lambda btn: self._tool_selected(btn, 'circle'))
        toolbar_box.toolbar.append(circle_btn)
        self._circle_btn = circle_btn

        # Separator
        separator2 = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        toolbar_box.toolbar.append(separator2)

        # Fill mode toggle
        fill_btn = Gtk.ToggleButton()
        fill_btn.set_label("Fill Mode")
        fill_btn.connect('toggled', self._fill_mode_toggled)
        toolbar_box.toolbar.append(fill_btn)
        self._fill_btn = fill_btn

        # Brush size
        size_label = Gtk.Label()
        size_label.set_markup("<span color='white' weight='bold'>Size:</span>")
        toolbar_box.toolbar.append(size_label)

        size_adjustment = Gtk.Adjustment(value=3, lower=1, upper=50, step_increment=1)
        size_spin = Gtk.SpinButton()
        size_spin.set_adjustment(size_adjustment)
        size_spin.connect('value-changed', self._brush_size_changed)
        toolbar_box.toolbar.append(size_spin)

        # Separator
        separator3 = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        toolbar_box.toolbar.append(separator3)

        colors_label = Gtk.Label()
        colors_label.set_markup("<span color='white' weight='bold'>Colors:</span>")
        toolbar_box.toolbar.append(colors_label)

        colors = [
            ("Black", (0, 0, 0)),
            ("Red", (1, 0, 0)),
            ("Blue", (0, 0, 1)),
            ("Green", (0, 0.8, 0)),
            ("Yellow", (1, 1, 0)),
            ("Purple", (0.8, 0, 0.8))
        ]

        for color_name, color_value in colors:
            color_btn = Gtk.Button()
            color_btn.set_tooltip_text(f"Select {color_name}")

            color_box = Gtk.Box()
            color_box.set_orientation(Gtk.Orientation.VERTICAL)
            color_box.set_spacing(2)

            # Create colored rectangle
            color_area = Gtk.DrawingArea()
            color_area.set_size_request(60, 20)

            def draw_color(area, cr, width, height, color_val=color_value):
                cr.set_source_rgb(*color_val)
                cr.paint()
                cr.set_source_rgb(0, 0, 0)
                cr.set_line_width(1)
                cr.rectangle(0.5, 0.5, width-1, height-1)
                cr.stroke()

            color_area.set_draw_func(draw_color)

            color_label = Gtk.Label()
            color_label.set_markup(f"<span color='black' size='small' weight='bold'>{color_name}</span>")

            color_box.append(color_area)
            color_box.append(color_label)
            color_btn.set_child(color_box)

            css_provider = Gtk.CssProvider()
            css = "button { background-color: #2a2a2a; border: 1px solid #555; padding: 4px; }"
            css_provider.load_from_data(css.encode())
            color_btn.get_style_context().add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

            color_btn.connect('clicked', lambda btn, c=color_value, name=color_name: self._color_selected(c, name))
            toolbar_box.toolbar.append(color_btn)
            self._color_buttons[color_value] = color_btn

        self._highlight_color_button((0, 0, 0))

        # Set up application accelerators for keyboard shortcuts
        self._setup_accelerators()

        separator4 = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        toolbar_box.toolbar.append(separator4)

        # Action buttons
        # Undo
        undo_btn = Gtk.Button()
        undo_btn.set_label("Undo")
        undo_btn.connect('clicked', lambda btn: self._undo_action())
        toolbar_box.toolbar.append(undo_btn)

        # Redo
        redo_btn = Gtk.Button()
        redo_btn.set_label("Redo")
        redo_btn.connect('clicked', lambda btn: self._redo_action())
        toolbar_box.toolbar.append(redo_btn)

        # Clear
        clear_btn = Gtk.Button()
        clear_btn.set_label("Clear")
        clear_btn.connect('clicked', lambda btn: self.clear_canvas())
        toolbar_box.toolbar.append(clear_btn)

        # Separator
        separator5 = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        toolbar_box.toolbar.append(separator5)

        # Save
        save_btn = Gtk.Button()
        save_btn.set_label("Save")
        save_btn.connect('clicked', lambda btn: self.save_creation())
        toolbar_box.toolbar.append(save_btn)

        # Preview
        preview_btn = Gtk.Button()
        preview_btn.set_label("Preview")
        preview_btn.connect('clicked', lambda btn: self.show_preview())
        toolbar_box.toolbar.append(preview_btn)

        # Spacer
        spacer = Gtk.Box()
        spacer.set_hexpand(True)
        toolbar_box.toolbar.append(spacer)

        # Stop button
        stop_button = StopButton(self)
        toolbar_box.toolbar.append(stop_button)

        self.set_toolbar_box(toolbar_box)

    def _highlight_color_button(self, color):
        """Highlight the selected color button."""
        for btn in self._color_buttons.values():
            btn.remove_css_class("suggested-action")

        if color in self._color_buttons:
            self._color_buttons[color].add_css_class("suggested-action")

    def _tool_selected(self, button, tool):
        """Handle tool selection."""
        if button.get_active():
            # Deactivate other tool buttons
            tool_buttons = [self._brush_btn, self._eraser_btn, self._line_btn,
                          self._rect_btn, self._circle_btn]
            for btn in tool_buttons:
                if btn != button:
                    btn.set_active(False)

            self._creative_canvas.set_tool(tool)
            self._current_tool = tool
            self._status_label.set_text(f"Selected tool: {tool.title()}")

    def _fill_mode_toggled(self, button):
        """Handle fill mode toggle."""
        fill_mode = button.get_active()
        self._creative_canvas.set_fill_mode(fill_mode)
        mode_text = "Fill" if fill_mode else "Outline"
        self._status_label.set_text(f"Shape mode: {mode_text}")

    def _brush_size_changed(self, spin_button):
        """Handle brush size change."""
        size = int(spin_button.get_value())
        self._creative_canvas.set_brush_size(size)
        self._status_label.set_text(f"Brush size: {size}")

    def _color_selected(self, color, color_name=None):
        """Handle color selection."""
        self._creative_canvas.set_color(color)
        self._current_color = color
        self._highlight_color_button(color)

        if color_name is None:
            color_names = {
                (0, 0, 0): "Black",
                (1, 0, 0): "Red",
                (0, 0, 1): "Blue",
                (0, 0.8, 0): "Green",
                (1, 1, 0): "Yellow",
                (0.8, 0, 0.8): "Purple"
            }
            color_name = color_names.get(color, "Custom")

        self._status_label.set_text(f"Selected color: {color_name}")

        # Give focus back to canvas for keyboard shortcuts
        self._creative_canvas.grab_focus()

    def _undo_action(self):
        """Handle undo action."""
        if self._creative_canvas.undo():
            self._status_label.set_text("Undid last action")
            self._has_unsaved_changes = True
        else:
            self._status_label.set_text("Nothing to undo")

    def _redo_action(self):
        """Handle redo action."""
        if self._creative_canvas.redo():
            self._status_label.set_text("Redid last action")
            self._has_unsaved_changes = True
        else:
            self._status_label.set_text("Nothing to redo")

    def _on_canvas_change(self):
        """Called when canvas content changes."""
        self._has_unsaved_changes = True
        self._update_doc_info()

    def _setup_accelerators(self):
        """Set up application-level keyboard accelerators."""
        # Create event controller for window-level shortcuts
        key_controller = Gtk.EventControllerKey()

        def on_key_pressed(controller, keyval, keycode, state):
            if state & Gdk.ModifierType.CONTROL_MASK:
                if keyval == Gdk.KEY_z or keyval == Gdk.KEY_Z:
                    self._undo_action()
                    return True
                elif keyval == Gdk.KEY_y or keyval == Gdk.KEY_Y:
                    self._redo_action()
                    return True
                elif keyval == Gdk.KEY_s or keyval == Gdk.KEY_S:
                    self.save_creation()
                    return True
            return False

        key_controller.connect('key-pressed', on_key_pressed)
        self.add_controller(key_controller)

    def _create_canvas(self):
        """Create the main canvas area."""
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        main_box.set_margin_top(12)
        main_box.set_margin_bottom(12)
        main_box.set_margin_start(12)
        main_box.set_margin_end(12)

        # Title
        title_label = Gtk.Label()
        title_label.set_markup("<span size='large' weight='bold'>Creative Studio</span>")
        title_label.set_halign(Gtk.Align.CENTER)
        main_box.append(title_label)

        # Status area
        self._status_label = Gtk.Label()
        self._status_label.set_text("Welcome to Creative Studio! Select a tool and start creating.")
        self._status_label.set_halign(Gtk.Align.CENTER)
        self._status_label.set_wrap(True)
        main_box.append(self._status_label)

        # Creative area
        canvas_frame = Gtk.Frame()
        canvas_frame.set_label("Creative Canvas")

        self._creative_canvas = CreativeCanvas()
        self._creative_canvas.set_change_callback(self._on_canvas_change)
        self._creative_canvas.set_save_callback(self.save_creation)

        # Make canvas focusable and give it initial focus
        self._creative_canvas.set_can_focus(True)
        self._creative_canvas.grab_focus()

        canvas_frame.set_child(self._creative_canvas)
        main_box.append(canvas_frame)

        # Info area
        info_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)

        doc_frame = Gtk.Frame()
        doc_frame.set_label("Project Info")

        self._doc_info_label = Gtk.Label()
        self._update_doc_info()
        self._doc_info_label.set_margin_top(6)
        self._doc_info_label.set_margin_bottom(6)
        self._doc_info_label.set_margin_start(6)
        self._doc_info_label.set_margin_end(6)

        doc_frame.set_child(self._doc_info_label)
        info_box.append(doc_frame)

        main_box.append(info_box)

        self.set_canvas(main_box)

    def _update_doc_info(self):
        """Update document info display."""
        if hasattr(self, '_doc_info_label'):
            element_count = len(self._creative_canvas._elements) if hasattr(self, '_creative_canvas') else 0
            save_status = "Unsaved changes" if self._has_unsaved_changes else "Saved"

            text = f"Created: {self._document_data['created'][:19]}\n"
            text += f"Modified: {self._document_data['modified'][:19]}\n"
            text += f"Elements: {element_count}\n"
            text += f"Status: {save_status}\n"
            text += f"Current Tool: {self._current_tool.title()}"
            self._doc_info_label.set_text(text)

    def clear_canvas(self):
        """Clear the creative canvas."""
        self._creative_canvas.clear_canvas()
        self._document_data['modified'] = datetime.now().isoformat()
        self._update_doc_info()
        self._status_label.set_text("Canvas cleared")

    def save_creation(self):
        """Save the current creation."""
        try:
            self._document_data['modified'] = datetime.now().isoformat()
            self._document_data['element_count'] = len(self._creative_canvas._elements)
            self._document_data['last_tool'] = self._current_tool

            # In a real Sugar activity, this would use the activity's write_file method
            # For demo purposes, we'll save to a temp location
            save_path = "/tmp/creative_studio_save.json"

            canvas_data = self._creative_canvas.get_canvas_data()
            data = {
                'document_data': self._document_data,
                'canvas_data': canvas_data,
                'current_tool': self._current_tool,
                'current_color': self._current_color,
                'saved_at': datetime.now().isoformat()
            }

            with open(save_path, 'w') as f:
                json.dump(data, f, indent=2)

            self._has_unsaved_changes = False
            self._update_doc_info()
            self._status_label.set_text(f"Creation saved successfully!")

        except Exception as e:
            logging.error(f"Error saving creation: {e}")
            self._status_label.set_text(f"Error saving: {e}")

    def show_preview(self):
        """Show a preview of the current creation."""
        try:
            preview_data = self.get_preview()
            if preview_data:
                # Save preview to temp file
                preview_path = "/tmp/creative_studio_preview.png"
                with open(preview_path, 'wb') as f:
                    f.write(preview_data)

                # Show preview dialog
                self._show_preview_dialog(preview_path)
                self._status_label.set_text("Preview shown")
            else:
                self._status_label.set_text("No content to preview")

        except Exception as e:
            logging.error(f"Error showing preview: {e}")
            self._status_label.set_text(f"Error showing preview: {e}")

    def _show_preview_dialog(self, image_path):
        """Show preview image in a dialog."""
        dialog = Gtk.Dialog()
        dialog.set_title("Creation Preview")
        dialog.set_transient_for(self)
        dialog.set_modal(True)
        dialog.set_default_size(850, 650)

        dialog.add_button("Close", Gtk.ResponseType.CLOSE)

        try:
            # Create a scrolled window for the image
            scrolled = Gtk.ScrolledWindow()
            scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
            scrolled.set_margin_top(10)
            scrolled.set_margin_bottom(10)
            scrolled.set_margin_start(10)
            scrolled.set_margin_end(10)

            image = Gtk.Image()
            image.set_from_file(image_path)

            scrolled.set_child(image)
            dialog.get_content_area().append(scrolled)
            dialog.present()

            def on_response(dialog, response_id):
                dialog.destroy()

            dialog.connect('response', on_response)

        except Exception as e:
            logging.error(f"Error loading preview image: {e}")
            dialog.destroy()

    def get_preview(self):
        """Generate a preview image of the current creation."""
        try:
            import cairo

            preview_width, preview_height = 1200, 800
            surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, preview_width, preview_height)
            cr = cairo.Context(surface)

            cr.set_source_rgb(1, 1, 1)
            cr.paint()

            cr.set_source_rgb(0.8, 0.8, 0.8)
            cr.set_line_width(2)
            cr.rectangle(2, 2, preview_width - 4, preview_height - 4)
            cr.stroke()

            if hasattr(self, '_creative_canvas') and self._creative_canvas._elements:
                # Scale the creation to fit the preview
                canvas_width, canvas_height = 800, 600
                scale_x = (preview_width - 20) / canvas_width
                scale_y = (preview_height - 20) / canvas_height
                scale = min(scale_x, scale_y)

                cr.save()
                cr.translate(10, 10)
                cr.scale(scale, scale)

                # Draw all elements
                for element in self._creative_canvas._elements:
                    self._creative_canvas._draw_element(cr, element)

                cr.restore()
            else:
                # No content, show placeholder
                cr.set_source_rgb(0.5, 0.5, 0.5)
                cr.select_font_face("Sans", 0, 0)
                cr.set_font_size(24)

                text = "Creative Studio"
                text_extents = cr.text_extents(text)
                x = (preview_width - text_extents.width) / 2
                y = preview_height / 2 - 10

                cr.move_to(x, y)
                cr.show_text(text)

                cr.set_font_size(16)
                text2 = "Create something amazing!"
                text_extents2 = cr.text_extents(text2)
                x2 = (preview_width - text_extents2.width) / 2
                y2 = y + 40

                cr.move_to(x2, y2)
                cr.show_text(text2)

            # Convert to PNG
            import io
            preview_str = io.BytesIO()
            surface.write_to_png(preview_str)
            return preview_str.getvalue()

        except Exception as e:
            logging.error(f"Error generating preview: {e}")
            return None

    def read_file(self, file_path):
        """Read creation data from file."""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)

            self._document_data = data.get('document_data', self._document_data)
            canvas_data = data.get('canvas_data', {})
            self._creative_canvas.set_canvas_data(canvas_data)

            self._current_tool = data.get('current_tool', 'brush')
            self._current_color = tuple(data.get('current_color', (0, 0, 0)))

            self._has_unsaved_changes = False
            self._update_doc_info()
            self._status_label.set_text("Creation loaded successfully")

        except Exception as e:
            logging.error(f"Error reading file: {e}")
            self._status_label.set_text(f"Error loading creation: {e}")

    def write_file(self, file_path):
        """Write creation data to file."""
        try:
            self._document_data['modified'] = datetime.now().isoformat()
            self._document_data['element_count'] = len(self._creative_canvas._elements)

            canvas_data = self._creative_canvas.get_canvas_data()
            data = {
                'document_data': self._document_data,
                'canvas_data': canvas_data,
                'current_tool': self._current_tool,
                'current_color': self._current_color,
                'activity_id': self.get_id(),
                'bundle_id': self.get_bundle_id(),
                'saved_at': datetime.now().isoformat()
            }

            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)

            self._has_unsaved_changes = False
            logging.info(f"Creative studio data saved to {file_path}")

        except Exception as e:
            logging.error(f"Error writing file: {e}")
            raise

    def can_close(self):
        """Check if the activity can be closed."""
        return True


class CreativeStudioApplication(Gtk.Application):
    """Application wrapper for the creative studio activity."""

    def __init__(self):
        super().__init__(application_id='org.sugarlabs.CreativeStudio',
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
        self.activity = None

    def do_activate(self):
        """Activate the application."""
        if not self.activity:
            handle = ActivityHandle('creative-studio-123')
            self.activity = CreativeStudioActivity(handle, application=self)
            self.activity.present()


def main():
    """Main entry point."""
    logging.basicConfig(level=logging.DEBUG)
    app = CreativeStudioApplication()
    return app.run(sys.argv)


if __name__ == "__main__":
    main()
