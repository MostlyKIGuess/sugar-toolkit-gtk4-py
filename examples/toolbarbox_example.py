"""ToolbarBox Example"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from sugar.activity import SimpleActivity
from sugar.graphics.toolbarbox import ToolbarBox, ToolbarButton
from sugar.graphics.toolbutton import ToolButton
from sugar.graphics.icon import Icon
from sugar.graphics import style

PROJECT_ROOT = os.path.join(os.path.dirname(__file__), "..")
SUGAR_ICONS_PATH = os.path.join(PROJECT_ROOT, "sugar-artwork", "icons", "scalable", "actions")
SUGAR_ICONS_PATH = os.path.abspath(SUGAR_ICONS_PATH)


class ToolbarBoxExampleActivity(SimpleActivity):
    """Example activity demonstrating Sugar GTK4 ToolbarBox features."""

    def __init__(self):
        super().__init__()
        self.set_title("Sugar GTK4 ToolbarBox Example")
        
        
        self._create_content()

    def _create_content(self):
        """Create the main content with expandable toolbars."""
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        self._toolbarbox = ToolbarBox()

        self._create_main_toolbar()

        main_box.append(self._toolbarbox)

        content_area = self._create_content_area()
        main_box.append(content_area)

        self._status_bar = Gtk.Label(
            label="Click toolbar buttons to expand/collapse sections"
        )
        self._status_bar.set_margin_start(style.DEFAULT_PADDING)
        self._status_bar.set_margin_end(style.DEFAULT_PADDING)
        self._status_bar.set_margin_top(style.DEFAULT_PADDING // 2)
        self._status_bar.set_margin_bottom(style.DEFAULT_PADDING // 2)
        self._status_bar.add_css_class("dim-label")
        main_box.append(self._status_bar)

        self.set_canvas(main_box)
        self.set_default_size(800, 600)

    def _create_main_toolbar(self):
        """Create the main toolbar with expandable sections."""
        toolbar = self._toolbarbox.get_toolbar()

        # Activity button (non-expandable)
        activity_button = ToolButton(icon_name=os.path.join(PROJECT_ROOT, "sugar-artwork", "icons", "scalable", "apps", "activity-journal.svg"))
        activity_button.set_tooltip("My Activity")
        toolbar.append(activity_button)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        separator.set_margin_start(6)
        separator.set_margin_end(6)
        toolbar.append(separator)

        # Edit tools (expandable)
        edit_button = ToolbarButton(
            page=self._create_edit_toolbar(), 
            icon_name=os.path.join(SUGAR_ICONS_PATH, "toolbar-edit.svg")
        )
        edit_button.set_tooltip("Edit Tools")
        toolbar.append(edit_button)

        # View tools (expandable)
        view_button = ToolbarButton(
            page=self._create_view_toolbar(), 
            icon_name=os.path.join(SUGAR_ICONS_PATH, "toolbar-view.svg")
        )
        view_button.set_tooltip("View Tools")
        toolbar.append(view_button)

        # Tools section (expandable)
        tools_button = ToolbarButton(
            page=self._create_tools_toolbar(), 
            icon_name=os.path.join(PROJECT_ROOT, "sugar-artwork", "icons", "scalable", "categories", "preferences-system.svg")
        )
        tools_button.set_tooltip("Tools")
        toolbar.append(tools_button)

        # Spacer
        spacer = Gtk.Box()
        spacer.set_hexpand(True)
        toolbar.append(spacer)

        # Stop button (non-expandable)
        stop_button = ToolButton(icon_name=os.path.join(SUGAR_ICONS_PATH, "activity-stop.svg"))
        stop_button.set_tooltip("Stop Activity")
        stop_button.connect("clicked", lambda w: self.close())
        toolbar.append(stop_button)

    def _create_edit_toolbar(self):
        """Create the edit toolbar page."""
        toolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        toolbar.set_margin_top(style.DEFAULT_PADDING)
        toolbar.set_margin_bottom(style.DEFAULT_PADDING)

        edit_buttons = [
            ("New", os.path.join(SUGAR_ICONS_PATH, "document-open.svg")),
            ("Save", os.path.join(SUGAR_ICONS_PATH, "document-save.svg")),
            ("---", None),  # Separator
            ("Copy", os.path.join(SUGAR_ICONS_PATH, "edit-copy.svg")),
            ("Paste", os.path.join(SUGAR_ICONS_PATH, "edit-paste.svg")),
            ("---", None),  # Separator
            ("Undo", os.path.join(SUGAR_ICONS_PATH, "edit-undo.svg")),
            ("Redo", os.path.join(SUGAR_ICONS_PATH, "edit-redo.svg")),
        ]

        for label, icon_name in edit_buttons:
            if label == "---":
                separator = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
                separator.set_margin_start(6)
                separator.set_margin_end(6)
                toolbar.append(separator)
            else:
                button = ToolButton(icon_name=icon_name)
                button.set_tooltip(label)
                button.connect("clicked", self._on_toolbar_action, f"Edit: {label}")
                toolbar.append(button)

        return toolbar

    def _create_view_toolbar(self):
        """Create the view toolbar page."""
        toolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        toolbar.set_margin_top(style.DEFAULT_PADDING)
        toolbar.set_margin_bottom(style.DEFAULT_PADDING)

        zoom_out = ToolButton(icon_name=os.path.join(SUGAR_ICONS_PATH, "zoom-out.svg"))
        zoom_out.set_tooltip("Zoom Out")
        zoom_out.connect("clicked", self._on_toolbar_action, "View: Zoom Out")
        toolbar.append(zoom_out)

        zoom_label = Gtk.Label(label="100%")
        zoom_label.set_size_request(50, -1)
        toolbar.append(zoom_label)

        zoom_in = ToolButton(icon_name=os.path.join(SUGAR_ICONS_PATH, "zoom-in.svg"))
        zoom_in.set_tooltip("Zoom In")
        zoom_in.connect("clicked", self._on_toolbar_action, "View: Zoom In")
        toolbar.append(zoom_in)

        separator = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        separator.set_margin_start(6)
        separator.set_margin_end(6)
        toolbar.append(separator)

        view_modes = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=3)
        view_modes.add_css_class("linked")

        list_view = Gtk.ToggleButton()
        list_view.set_child(
            Icon(file_name=os.path.join(SUGAR_ICONS_PATH, "view-list.svg"), pixel_size=style.STANDARD_ICON_SIZE)
        )
        list_view.set_tooltip_text("List View")
        list_view.set_active(True)
        view_modes.append(list_view)

        grid_view = Gtk.ToggleButton()
        grid_view.set_child(
            Icon(file_name=os.path.join(SUGAR_ICONS_PATH, "view-details.svg"), pixel_size=style.STANDARD_ICON_SIZE)
        )
        grid_view.set_tooltip_text("Details View")
        view_modes.append(grid_view)

        toolbar.append(view_modes)

        return toolbar

    def _create_tools_toolbar(self):
        """Create the tools toolbar page."""
        toolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        toolbar.set_margin_top(style.DEFAULT_PADDING)
        toolbar.set_margin_bottom(style.DEFAULT_PADDING)

        # Tool selection  
        cursor_path = os.path.join(PROJECT_ROOT, "sugar-artwork", "cursor", "sugar", "pngs")
        tools = [
            ("Brush", os.path.join(cursor_path, "paintbrush.png")),
            ("Text", os.path.join(SUGAR_ICONS_PATH, "format-text-bold.svg")),
            ("Shape", os.path.join(SUGAR_ICONS_PATH, "view-triangle.svg")),
            ("Select", os.path.join(SUGAR_ICONS_PATH, "select-all.svg")),
        ]

        for name, icon_path in tools:
            tool_button = ToolButton(icon_name=icon_path)
            tool_button.set_tooltip(name)
            tool_button.connect("clicked", self._on_toolbar_action, f"Tool: {name}")
            toolbar.append(tool_button)

        separator = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        separator.set_margin_start(6)
        separator.set_margin_end(6)
        toolbar.append(separator)

        color_button = Gtk.ColorButton()
        color_button.set_tooltip_text("Choose Color")
        toolbar.append(color_button)

        properties_button = ToolButton(icon_name=os.path.join(PROJECT_ROOT, "sugar-artwork", "icons", "scalable", "categories", "preferences-system.svg"))
        properties_button.set_tooltip("Properties")
        properties_button.connect(
            "clicked", self._on_toolbar_action, "Tool: Properties"
        )
        toolbar.append(properties_button)

        return toolbar

    def _create_content_area(self):
        """Create main content area."""
        content_frame = Gtk.Frame()
        content_frame.set_margin_start(style.DEFAULT_PADDING)
        content_frame.set_margin_end(style.DEFAULT_PADDING)
        content_frame.set_margin_top(style.DEFAULT_PADDING)
        content_frame.set_margin_bottom(style.DEFAULT_PADDING)

        content_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=style.DEFAULT_SPACING
        )
        content_box.set_margin_start(style.DEFAULT_PADDING)
        content_box.set_margin_end(style.DEFAULT_PADDING)
        content_box.set_margin_top(style.DEFAULT_PADDING)
        content_box.set_margin_bottom(style.DEFAULT_PADDING)

        description = Gtk.Label()
        description.set_markup("""
<b>Sugar GTK4 ToolbarBox Example</b>

This example demonstrates the expandable toolbar functionality:

- <b>Expandable Sections:</b> Click Edit, View, or Tools buttons to expand sections
- <b>Inline Display:</b> Expanded toolbars appear below the main toolbar
- <b>Palette Fallback:</b> On smaller screens, content may appear in palettes

<i>Click the toolbar buttons above to see the expansion behavior.</i>
        """)
        description.set_halign(Gtk.Align.START)
        content_box.append(description)

        log_frame = Gtk.Frame(label="Action Log")
        log_frame.set_margin_top(style.DEFAULT_SPACING)

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_size_request(-1, 150)

        self._action_log = Gtk.TextView()
        self._action_log.set_editable(False)
        self._action_log.set_cursor_visible(False)
        scrolled.set_child(self._action_log)

        log_frame.set_child(scrolled)
        content_box.append(log_frame)

        content_frame.set_child(content_box)
        return content_frame

    def _on_toolbar_action(self, button, action):
        """Handle toolbar button clicks."""
        self._log_action(action)

    def _log_action(self, action):
        """Add action to the log."""
        buffer = self._action_log.get_buffer()

        import datetime

        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        text = f"[{timestamp}] {action}\n"

        end_iter = buffer.get_end_iter()
        buffer.insert(end_iter, text)

        mark = buffer.get_insert()
        self._action_log.scroll_mark_onscreen(mark)


def main():
    """Run the ToolbarBox example activity."""
    app = Gtk.Application(application_id="org.sugarlabs.ToolbarBoxExample")

    def on_activate(app):
        activity = ToolbarBoxExampleActivity()
        activity.set_application(app)
        activity.present()

    app.connect("activate", on_activate)
    return app.run(sys.argv)


if __name__ == "__main__":
    main()

