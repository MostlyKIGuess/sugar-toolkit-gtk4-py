"""Sugar GTK4 Toolbox Example """

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from sugar.activity import SimpleActivity
from sugar.graphics.toolbox import Toolbox
from sugar.graphics import style
from sugar.graphics.icon import Icon


class ToolboxExampleActivity(SimpleActivity):
    """Example activity demonstrating Sugar GTK4 Toolbox features."""

    def __init__(self):
        super().__init__()
        self.set_title("Sugar GTK4 Toolbox Example")
        self._create_content()

    def _create_content(self):
        """Create the main content with toolbox."""
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        # Create toolbox
        self._toolbox = Toolbox()
        self._toolbox.connect('current-toolbar-changed', self._on_toolbar_changed)

        # Add various toolbars
        self._create_edit_toolbar()
        self._create_view_toolbar()
        self._create_tools_toolbar()
        self._create_help_toolbar()

        main_box.append(self._toolbox)

        # Add content area
        content_area = self._create_content_area()
        main_box.append(content_area)

        # Status bar
        self._status_bar = Gtk.Label(label="Toolbox Example - Switch between toolbars using tabs")
        self._status_bar.set_margin_start(style.DEFAULT_PADDING)
        self._status_bar.set_margin_end(style.DEFAULT_PADDING)
        self._status_bar.set_margin_top(style.DEFAULT_PADDING // 2)
        self._status_bar.set_margin_bottom(style.DEFAULT_PADDING // 2)
        self._status_bar.add_css_class('dim-label')
        main_box.append(self._status_bar)

        self.set_canvas(main_box)
        self.set_default_size(800, 600)

    def _create_edit_toolbar(self):
        """Create edit toolbar with common editing tools."""
        toolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        toolbar.set_margin_top(style.DEFAULT_PADDING)
        toolbar.set_margin_bottom(style.DEFAULT_PADDING)

        # Common edit buttons
        edit_buttons = [
            ("New", "document-new"),
            ("Open", "document-open"),
            ("Save", "document-save"),
            ("---", None),  # Separator
            ("Cut", "edit-cut"),
            ("Copy", "edit-copy"),
            ("Paste", "edit-paste"),
            ("---", None),  # Separator
            ("Undo", "edit-undo"),
            ("Redo", "edit-redo"),
        ]

        for label, icon_name in edit_buttons:
            if label == "---":
                separator = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
                separator.set_margin_start(6)
                separator.set_margin_end(6)
                toolbar.append(separator)
            else:
                button = Gtk.Button()
                if icon_name:
                    icon = Icon(icon_name=icon_name, pixel_size=style.STANDARD_ICON_SIZE)
                    button.set_child(icon)
                button.set_tooltip_text(label)
                button.connect('clicked', self._on_toolbar_button_clicked, f"Edit: {label}")
                toolbar.append(button)

        # Add spacer
        spacer = Gtk.Box()
        spacer.set_hexpand(True)
        toolbar.append(spacer)

        # Add text entry for demonstration
        entry = Gtk.Entry()
        entry.set_placeholder_text("Type something...")
        entry.set_size_request(200, -1)
        toolbar.append(entry)

        self._toolbox.add_toolbar("Edit", toolbar)

    def _create_view_toolbar(self):
        """Create view toolbar with view-related controls."""
        toolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        toolbar.set_margin_top(style.DEFAULT_PADDING)
        toolbar.set_margin_bottom(style.DEFAULT_PADDING)

        # Zoom controls
        zoom_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=3)

        zoom_out = Gtk.Button()
        zoom_out.set_child(Icon(icon_name="zoom-out", pixel_size=style.STANDARD_ICON_SIZE))
        zoom_out.set_tooltip_text("Zoom Out")
        zoom_out.connect('clicked', self._on_toolbar_button_clicked, "View: Zoom Out")
        zoom_box.append(zoom_out)

        zoom_label = Gtk.Label(label="100%")
        zoom_label.set_size_request(50, -1)
        zoom_box.append(zoom_label)

        zoom_in = Gtk.Button()
        zoom_in.set_child(Icon(icon_name="zoom-in", pixel_size=style.STANDARD_ICON_SIZE))
        zoom_in.set_tooltip_text("Zoom In")
        zoom_in.connect('clicked', self._on_toolbar_button_clicked, "View: Zoom In")
        zoom_box.append(zoom_in)

        toolbar.append(zoom_box)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        separator.set_margin_start(6)
        separator.set_margin_end(6)
        toolbar.append(separator)

        # View mode toggle buttons
        view_modes = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=3)
        view_modes.add_css_class('linked')

        list_view = Gtk.ToggleButton()
        list_view.set_child(Icon(icon_name="view-list", pixel_size=style.STANDARD_ICON_SIZE))
        list_view.set_tooltip_text("List View")
        list_view.set_active(True)
        list_view.connect('toggled', self._on_view_mode_toggled, "List View")
        view_modes.append(list_view)

        grid_view = Gtk.ToggleButton()
        grid_view.set_child(Icon(icon_name="view-grid", pixel_size=style.STANDARD_ICON_SIZE))
        grid_view.set_tooltip_text("Grid View")
        grid_view.connect('toggled', self._on_view_mode_toggled, "Grid View")
        view_modes.append(grid_view)

        toolbar.append(view_modes)

        # Spacer
        spacer = Gtk.Box()
        spacer.set_hexpand(True)
        toolbar.append(spacer)

        # Fullscreen button
        fullscreen = Gtk.Button()
        fullscreen.set_child(Icon(icon_name="view-fullscreen", pixel_size=style.STANDARD_ICON_SIZE))
        fullscreen.set_tooltip_text("Fullscreen")
        fullscreen.connect('clicked', self._on_toolbar_button_clicked, "View: Fullscreen")
        toolbar.append(fullscreen)

        self._toolbox.add_toolbar("View", toolbar)

    def _create_tools_toolbar(self):
        """Create tools toolbar with tool-specific controls."""
        toolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        toolbar.set_margin_top(style.DEFAULT_PADDING)
        toolbar.set_margin_bottom(style.DEFAULT_PADDING)

        # Tool selection
        tools_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=3)
        tools_box.add_css_class('linked')

        tools = [
            ("Pointer", "tool-pointer"),
            ("Brush", "tool-brush"),
            ("Text", "tool-text"),
            ("Shape", "shape-rectangle"),
        ]

        for i, (name, icon_name) in enumerate(tools):
            tool_button = Gtk.ToggleButton()
            tool_button.set_child(Icon(icon_name=icon_name, pixel_size=style.STANDARD_ICON_SIZE))
            tool_button.set_tooltip_text(name)
            if i == 0:  # Select first tool by default
                tool_button.set_active(True)
            tool_button.connect('toggled', self._on_tool_selected, name)
            tools_box.append(tool_button)

        toolbar.append(tools_box)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        separator.set_margin_start(6)
        separator.set_margin_end(6)

        toolbar.append(separator)

        # Color picker
        color_button = Gtk.ColorButton()
        color_button.set_tooltip_text("Choose Color")
        toolbar.append(color_button)

        # Size adjustment
        size_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        size_label = Gtk.Label(label="Size:")
        size_box.append(size_label)

        size_scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL)
        size_scale.set_range(1, 20)
        size_scale.set_value(5)
        size_scale.set_size_request(100, -1)
        size_scale.set_tooltip_text("Tool Size")
        size_box.append(size_scale)

        toolbar.append(size_box)

        self._toolbox.add_toolbar("Tools", toolbar)

    def _create_help_toolbar(self):
        """Create help toolbar with help and information."""
        toolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        toolbar.set_margin_top(style.DEFAULT_PADDING)
        toolbar.set_margin_bottom(style.DEFAULT_PADDING)

        # Help buttons
        help_button = Gtk.Button()
        help_button.set_child(Icon(icon_name="help-contents", pixel_size=style.STANDARD_ICON_SIZE))
        help_button.set_tooltip_text("Help Contents")
        help_button.connect('clicked', self._on_toolbar_button_clicked, "Help: Contents")
        toolbar.append(help_button)

        about_button = Gtk.Button()
        about_button.set_child(Icon(icon_name="help-about", pixel_size=style.STANDARD_ICON_SIZE))
        about_button.set_tooltip_text("About")
        about_button.connect('clicked', self._on_toolbar_button_clicked, "Help: About")
        toolbar.append(about_button)

        # Spacer
        spacer = Gtk.Box()
        spacer.set_hexpand(True)
        toolbar.append(spacer)

        # Info display
        info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        info_title = Gtk.Label(label="Toolbox Info")
        info_title.add_css_class('heading')
        info_box.append(info_title)

        self._info_label = Gtk.Label(label=f"Total toolbars: {self._toolbox.get_toolbar_count()}")
        self._info_label.add_css_class('dim-label')
        info_box.append(self._info_label)

        toolbar.append(info_box)

        self._toolbox.add_toolbar("Help", toolbar)

    def _create_content_area(self):
        """Create main content area."""
        content_frame = Gtk.Frame()
        content_frame.set_hexpand(True)
        content_frame.set_vexpand(True)
        content_frame.set_margin_start(style.DEFAULT_PADDING)
        content_frame.set_margin_end(style.DEFAULT_PADDING)
        content_frame.set_margin_top(style.DEFAULT_PADDING)
        content_frame.set_margin_bottom(style.DEFAULT_PADDING)

        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=style.DEFAULT_SPACING)
        content_box.set_margin_start(style.DEFAULT_PADDING * 2)
        content_box.set_margin_end(style.DEFAULT_PADDING * 2)
        content_box.set_margin_top(style.DEFAULT_PADDING * 2)
        content_box.set_margin_bottom(style.DEFAULT_PADDING * 2)

        title = Gtk.Label()
        title.set_markup("<big><b>Toolbox Demo Content Area</b></big>")
        content_box.append(title)

        description = Gtk.Label()
        description.set_markup("""
<i>This demonstrates the Sugar Toolbox component:</i>

• <b>Multiple Toolbars:</b> Switch between Edit, View, Tools, and Help
• <b>Tab Navigation:</b> Click tabs at the bottom to switch toolbars
• <b>Dynamic Content:</b> Each toolbar can contain different widgets
• <b>Sugar Styling:</b> Consistent with Sugar visual design
• <b>Signal Handling:</b> Responds to toolbar changes

<i>Click the buttons in the toolbars above to see actions.</i>
        """)
        description.set_halign(Gtk.Align.START)
        content_box.append(description)

        # Action log
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

    def _on_toolbar_changed(self, toolbox, page_num):
        """Handle toolbar change."""
        toolbar_name = self._toolbox.get_toolbar_label(page_num)
        self._log_action(f"Switched to {toolbar_name} toolbar")

        # Update info in help toolbar
        if hasattr(self, '_info_label'):
            self._info_label.set_text(
                f"Total toolbars: {self._toolbox.get_toolbar_count()}, "
                f"Current: {page_num + 1} ({toolbar_name})"
            )

    def _on_toolbar_button_clicked(self, button, action):
        """Handle toolbar button clicks."""
        self._log_action(action)

    def _on_view_mode_toggled(self, button, mode):
        """Handle view mode toggle."""
        if button.get_active():
            self._log_action(f"Switched to {mode}")

    def _on_tool_selected(self, button, tool_name):
        """Handle tool selection."""
        if button.get_active():
            self._log_action(f"Selected {tool_name} tool")

    def _log_action(self, action):
        """Add action to the log."""
        buffer = self._action_log.get_buffer()

        # Add timestamp and action
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        text = f"[{timestamp}] {action}\n"

        # Insert at end
        end_iter = buffer.get_end_iter()
        buffer.insert(end_iter, text)

        # Scroll to end
        mark = buffer.get_insert()
        self._action_log.scroll_mark_onscreen(mark)


def main():
    """Run the Toolbox example activity."""
    app = Gtk.Application(application_id='org.sugarlabs.ToolboxExample')

    def on_activate(app):
        activity = ToolboxExampleActivity()
        app.add_window(activity)
        activity.present()

    app.connect('activate', on_activate)
    return app.run()


if __name__ == "__main__":
    main()
