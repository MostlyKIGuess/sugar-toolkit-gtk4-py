"""
Complete Palette Demo
"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')

import sys
import os
from gi.repository import Gtk

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from sugar.graphics.palette import Palette
from sugar.graphics.palettewindow import (
    PaletteWindow, WidgetInvoker,  CursorInvoker,
)
from sugar.graphics.palettemenu import PaletteMenuItem, PaletteMenuItemSeparator
from sugar.graphics.palettegroup import get_group
from sugar.graphics.icon import Icon
from sugar.graphics import style


class PaletteDemo(Gtk.ApplicationWindow):
    """Main demo window showcasing all palette features."""

    def __init__(self, app):
        super().__init__(application=app)
        self.set_title("Sugar Palette Complete Demo - GTK4")
        self.set_default_size(800, 600)

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_box.set_margin_start(20)
        main_box.set_margin_end(20)
        main_box.set_margin_top(20)
        main_box.set_margin_bottom(20)
        self.set_child(main_box)

        title = Gtk.Label()
        title.set_markup("<big><b>Sugar Palette Demo - GTK4</b></big>")
        main_box.append(title)

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_vexpand(True)
        main_box.append(scrolled)

        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        scrolled.set_child(content_box)

        self._create_basic_palette_section(content_box)
        self._create_menu_palette_section(content_box)
        self._create_palette_window_section(content_box)
        self._create_invoker_section(content_box)
        self._create_treeview_section(content_box)
        self._create_palette_group_section(content_box)

    def _create_section_header(self, parent, title, description):
        header_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        parent.append(header_box)

        title_label = Gtk.Label()
        title_label.set_markup(f"<b>{title}</b>")
        title_label.set_halign(Gtk.Align.START)
        header_box.append(title_label)

        desc_label = Gtk.Label(label=description)
        desc_label.set_halign(Gtk.Align.START)
        desc_label.set_wrap(True)
        desc_label.add_css_class('dim-label')
        header_box.append(desc_label)

        sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        sep.set_margin_top(10)
        sep.set_margin_bottom(10)
        parent.append(sep)

        return header_box

    def _create_basic_palette_section(self, parent):
        section = self._create_section_header(
            parent,
            "Basic Palettes",
            "Basic palette widgets with text, icons, and content"
        )

        demo_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        demo_box.set_margin_top(10)
        parent.append(demo_box)

        simple_btn = Gtk.Button(label="Simple Palette")
        demo_box.append(simple_btn)

        simple_palette = Palette(label="Simple Palette")
        simple_palette.props.secondary_text = "This is a simple palette with primary and secondary text."

        close_btn1 = Gtk.Button(label="Close")
        close_btn1.connect('clicked', lambda btn: simple_palette.popdown(immediate=True))
        simple_palette.set_content(close_btn1)

        simple_invoker = WidgetInvoker()
        simple_invoker.attach(simple_btn)
        simple_invoker.set_lock_palette(True)
        simple_palette.set_invoker(simple_invoker)
        simple_btn.connect('clicked', lambda btn: simple_palette.popup(immediate=True))

        icon_btn = Gtk.Button(label="With Icon")
        demo_box.append(icon_btn)

        icon_palette = Palette(label="Palette with Icon")
        icon_palette.props.secondary_text = "This palette includes an icon and action buttons."
        icon_palette.set_icon(Icon(icon_name='dialog-information', pixel_size=style.STANDARD_ICON_SIZE))

        close_btn2 = Gtk.Button(label="Close")
        close_btn2.connect('clicked', lambda btn: icon_palette.popdown(immediate=True))
        icon_palette.set_content(close_btn2)

        icon_palette.action_bar.add_action("Action 1", "document-save")
        icon_palette.action_bar.add_action("Action 2", "edit-copy")

        icon_invoker = WidgetInvoker()
        icon_invoker.attach(icon_btn)
        icon_invoker.set_lock_palette(True)
        icon_palette.set_invoker(icon_invoker)
        icon_btn.connect('clicked', lambda btn: icon_palette.popup(immediate=True))

        # custom content
        content_btn = Gtk.Button(label="Custom Content")
        demo_box.append(content_btn)

        content_palette = Palette(label="Custom Content")
        content_palette.props.secondary_text = "This palette contains custom widgets."

        custom_content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        custom_content.set_margin_start(10)
        custom_content.set_margin_end(10)
        custom_content.set_margin_top(5)
        custom_content.set_margin_bottom(5)

        entry = Gtk.Entry()
        entry.set_placeholder_text("Type something...")
        custom_content.append(entry)

        scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 0, 100, 1)
        scale.set_value(50)
        custom_content.append(scale)

        check = Gtk.CheckButton(label="Enable feature")
        custom_content.append(check)

        close_btn3 = Gtk.Button(label="Close")
        close_btn3.connect('clicked', lambda btn: content_palette.popdown(immediate=True))
        custom_content.append(close_btn3)

        content_palette.set_content(custom_content)

        content_invoker = WidgetInvoker()
        content_invoker.attach(content_btn)
        content_invoker.set_lock_palette(True)
        content_palette.set_invoker(content_invoker)
        content_btn.connect('clicked', lambda btn: content_palette.popup(immediate=True))

    def _create_menu_palette_section(self, parent):
        """Create menu palette examples."""
        section = self._create_section_header(
            parent,
            "Menu Palettes",
            "Palettes that act as context menus with menu items"
        )

        demo_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        demo_box.set_margin_top(10)
        parent.append(demo_box)

        menu_btn = Gtk.Button(label="Menu Palette")
        demo_box.append(menu_btn)

        self.menu_feedback_label = Gtk.Label(label="(No menu action yet)")
        demo_box.append(self.menu_feedback_label)

        menu_palette = Palette(label="Menu Options")
        menu_palette.props.secondary_text = "Right-click or use menu property for options"
        menu = menu_palette.menu

        def feedback(msg):
            self.menu_feedback_label.set_text(msg)

        item1 = PaletteMenuItem("Open File", "document-open")
        item1.connect('activate', lambda x: feedback("Open File clicked"))
        menu.append(item1)

        item2 = PaletteMenuItem("Save File", "document-save")
        item2.connect('activate', lambda x: feedback("Save File clicked"))
        menu.append(item2)

        menu.append(PaletteMenuItemSeparator())

        item3 = PaletteMenuItem("Settings", "preferences-system")
        item3.connect('activate', lambda x: feedback("Settings clicked"))
        menu.append(item3)

        menu_invoker = WidgetInvoker()
        menu_invoker.attach_widget(menu_btn)
        menu_palette.set_invoker(menu_invoker)
        menu_btn.connect('clicked', lambda btn: menu_palette.popup(immediate=True))

    def _create_palette_window_section(self, parent):
        """Create palette window examples."""
        section = self._create_section_header(
            parent,
            "Palette Windows",
            "Low-level palette window implementation"
        )

        demo_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        demo_box.set_margin_top(10)
        parent.append(demo_box)

        window_btn = Gtk.Button(label="Palette Window")
        demo_box.append(window_btn)

        palette_window = PaletteWindow()

        custom_widget = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        custom_widget.set_margin_start(10)
        custom_widget.set_margin_end(10)
        custom_widget.set_margin_top(10)
        custom_widget.set_margin_bottom(10)

        label = Gtk.Label(label="Custom Palette Window")
        label.add_css_class('heading')
        custom_widget.append(label)

        progress = Gtk.ProgressBar()
        progress.set_fraction(0.7)
        progress.set_text("Progress: 70%")
        progress.set_show_text(True)
        custom_widget.append(progress)

        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        button_box.set_halign(Gtk.Align.CENTER)
        ok_btn = Gtk.Button(label="OK")
        cancel_btn = Gtk.Button(label="Cancel")
        button_box.append(ok_btn)
        button_box.append(cancel_btn)
        custom_widget.append(button_box)

        palette_window.set_content(custom_widget)

        window_invoker = WidgetInvoker()
        window_invoker.attach(window_btn)
        palette_window.set_invoker(window_invoker)
        window_btn.connect('clicked', lambda btn: palette_window.popup(immediate=True))

        ok_btn.connect('clicked', lambda btn: palette_window.popdown(immediate=True))
        cancel_btn.connect('clicked', lambda btn: palette_window.popdown(immediate=True))

    def _create_invoker_section(self, parent):
        """Create different invoker type examples."""
        section = self._create_section_header(
            parent,
            "Invoker Types",
            "Different ways to trigger palette display"
        )

        demo_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        demo_box.set_margin_top(10)
        parent.append(demo_box)

        # Widget invoker (hover demo with box)
        widget_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hover_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        hover_box.set_size_request(120, 40)
        hover_box.set_halign(Gtk.Align.START)
        hover_box.set_valign(Gtk.Align.CENTER)
        hover_box.set_margin_top(4)
        hover_box.set_margin_bottom(4)
        hover_box.set_margin_start(4)
        hover_box.set_margin_end(4)
        hover_box.add_css_class('suggested-action')
        hover_label = Gtk.Label(label="Hover Me (Box)")
        hover_box.append(hover_label)
        widget_row.append(hover_box)
        widget_row.append(Gtk.Label(label="← Hover to invoke palette"))
        demo_box.append(widget_row)

        widget_palette = Palette(label="Widget Invoker (Hover)")
        widget_palette.props.secondary_text = "Triggered by hover on box"
        widget_invoker = WidgetInvoker()
        widget_invoker.attach_widget(hover_box)
        widget_palette.set_invoker(widget_invoker)
        def on_motion_enter(controller, x, y):
            widget_palette.popup(immediate=True)
        motion_controller = Gtk.EventControllerMotion()
        motion_controller.connect('enter', on_motion_enter)
        hover_box.add_controller(motion_controller)


        cursor_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        cursor_btn = Gtk.Button(label="Cursor Invoker")
        cursor_row.append(cursor_btn)
        cursor_row.append(Gtk.Label(label="← Click to show at cursor position"))
        demo_box.append(cursor_row)

        cursor_palette = Palette(label="Cursor Invoker")
        cursor_palette.props.secondary_text = "Shows at cursor position"
        cursor_invoker = CursorInvoker()
        cursor_invoker.attach(cursor_btn)
        cursor_palette.set_invoker(cursor_invoker)

        def update_pointer_position(motion_controller, x, y):
            cursor_invoker._cursor_x = int(x)
            cursor_invoker._cursor_y = int(y)
        motion_controller = Gtk.EventControllerMotion()
        motion_controller.connect('motion', update_pointer_position)
        cursor_btn.add_controller(motion_controller)

        def show_cursor_palette(btn):
            cursor_palette.popup(immediate=True)
        cursor_btn.connect('clicked', show_cursor_palette)

    def _create_treeview_section(self, parent):
        """Create TreeView invoker examples."""
        section = self._create_section_header(
            parent,
            "TreeView Integration",
            "Double-click a row to show a palette for that item."
        )

        demo_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        demo_box.set_margin_top(10)
        parent.append(demo_box)

        store = Gtk.ListStore(str, str)
        store.append(["Item 1", "Description 1"])
        store.append(["Item 2", "Description 2"])
        store.append(["Item 3", "Description 3"])

        tree_view = Gtk.TreeView(model=store)
        tree_view.set_size_request(-1, 150)

        renderer = Gtk.CellRendererText()
        column1 = Gtk.TreeViewColumn("Name", renderer, text=0)
        tree_view.append_column(column1)

        column2 = Gtk.TreeViewColumn("Description", renderer, text=1)
        tree_view.append_column(column2)

        scrolled_tree = Gtk.ScrolledWindow()
        scrolled_tree.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled_tree.set_child(tree_view)
        demo_box.append(scrolled_tree)

        #  only double-click (row-activated) opens palette
        def show_row_palette(treeview, path, column=None):
            row = store[path][0]
            palette = Palette(label=f"Row: {row}")
            palette.props.secondary_text = f"Palette for {row}"
            close_btn = Gtk.Button(label="Close")
            close_btn.connect('clicked', lambda btn: palette.popdown(immediate=True))
            palette.set_content(close_btn)
            invoker = WidgetInvoker()
            invoker.attach(tree_view)
            invoker.set_lock_palette(True)
            palette.set_invoker(invoker)
            palette.popup(immediate=True)
        def on_row_activated(treeview, path, column):
            show_row_palette(treeview, path, column)
        tree_view.connect('row-activated', on_row_activated)

    def _create_palette_group_section(self, parent):
        """Create palette group examples."""
        section = self._create_section_header(
            parent,
            "Palette Groups",
            "Coordinated palettes - only one shows at a time"
        )

        demo_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        demo_box.set_margin_top(10)
        parent.append(demo_box)

        group = get_group('demo_group')

        for i in range(3):
            btn = Gtk.Button(label=f"Group Palette {i+1}")
            demo_box.append(btn)

            palette = Palette(label=f"Grouped Palette {i+1}")
            palette.props.secondary_text = f"This is palette {i+1} in the group. Only one group palette can be open at a time."

            group.add(palette)

            invoker = WidgetInvoker()
            invoker.attach(btn)
            palette.set_invoker(invoker)
            btn.connect('clicked', lambda btn, p=palette: p.popup(immediate=True))

        control_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        control_box.set_margin_top(10)
        parent.append(control_box)

        popdown_btn = Gtk.Button(label="Pop Down All Groups")
        popdown_btn.connect('clicked', lambda btn: self._popdown_all_groups())
        control_box.append(popdown_btn)

    def _popdown_all_groups(self):
        """Pop down all palette groups."""
        from sugar.graphics.palettegroup import popdown_all
        popdown_all()
        print("All palette groups popped down")


class PaletteDemoApp(Gtk.Application):

    def __init__(self):
        super().__init__(application_id='org.sugarlabs.PaletteDemo')

    def do_activate(self):
        window = PaletteDemo(self)
        window.present()


def main():
    app = PaletteDemoApp()
    return app.run([])


if __name__ == '__main__':
    sys.exit(main())
