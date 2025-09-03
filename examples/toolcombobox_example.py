#!/usr/bin/env python3
"""
Example demonstrating the Sugar ToolComboBox widget.

This example shows how to use the ToolComboBox component from the Sugar Toolkit,
including using it in toolbars with labels and custom combo boxes.
"""

import sys
import os

# Add src to path to import sugar modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GObject

from sugar.graphics.toolcombobox import ToolComboBox
from sugar.graphics.combobox import ComboBox


class ToolComboBoxExample(Gtk.ApplicationWindow):
    """Example window demonstrating ToolComboBox usage."""

    def __init__(self, app):
        super().__init__(application=app, title="Sugar ToolComboBox Example")
        self.set_default_size(700, 500)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_margin_top(10)
        vbox.set_margin_bottom(10)
        vbox.set_margin_start(10)
        vbox.set_margin_end(10)
        self.set_child(vbox)

        title = Gtk.Label(label="<b>Sugar ToolComboBox Examples</b>")
        title.set_use_markup(True)
        vbox.append(title)

        self.create_basic_toolbar_example(vbox)
        self.create_formatting_toolbar_example(vbox)
        self.create_custom_combo_example(vbox)
        self.create_dynamic_toolbar_example(vbox)

        self.status_label = Gtk.Label(label="Select items from the combo boxes to see their values")
        self.status_label.set_selectable(True)
        self.status_label.set_wrap(True)
        vbox.append(self.status_label)

    def create_basic_toolbar_example(self, parent):
        """Create basic tool combo box example."""
        frame = Gtk.Frame(label="Basic ToolComboBox Usage")
        frame.set_margin_top(10)

        vbox_inner = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox_inner.set_margin_top(10)
        vbox_inner.set_margin_bottom(10)
        vbox_inner.set_margin_start(10)
        vbox_inner.set_margin_end(10)
        frame.set_child(vbox_inner)

        # Create horizontal box as toolbar replacement (GTK4 doesn't have Toolbar)
        toolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        toolbar.set_margin_top(5)
        toolbar.set_margin_bottom(5)
        toolbar.set_margin_start(5)
        toolbar.set_margin_end(5)
        vbox_inner.append(toolbar)

        self.basic_tool_combo = ToolComboBox(label_text="Language:")
        self.basic_tool_combo.combo.append_item("en", "English")
        self.basic_tool_combo.combo.append_item("es", "Español")
        self.basic_tool_combo.combo.append_item("fr", "Français")
        self.basic_tool_combo.combo.append_item("de", "Deutsch")
        self.basic_tool_combo.combo.append_item("pt", "Português")
        self.basic_tool_combo.combo.connect("changed", self.on_language_changed)
        toolbar.append(self.basic_tool_combo)

        separator = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        toolbar.append(separator)

        icon_combo = ComboBox()
        try:
            icon_combo.append_item("high", "High Quality", icon_name="video-display")
            icon_combo.append_item("medium", "Medium Quality", icon_name="audio-volume-medium")
            icon_combo.append_item("low", "Low Quality", icon_name="audio-volume-low")
        except ValueError:
            # Fallback if icons don't exist
            icon_combo.append_item("high", "High Quality")
            icon_combo.append_item("medium", "Medium Quality")
            icon_combo.append_item("low", "Low Quality")

        self.quality_tool_combo = ToolComboBox(combo=icon_combo, label_text="Quality:")
        self.quality_tool_combo.combo.connect("changed", self.on_quality_changed)
        toolbar.append(self.quality_tool_combo)

        desc = Gtk.Label(label="Basic usage with text labels and optional icons")
        desc.set_wrap(True)
        vbox_inner.append(desc)

        parent.append(frame)

    def create_formatting_toolbar_example(self, parent):
        """Create formatting toolbar example."""
        frame = Gtk.Frame(label="Text Formatting Toolbar")
        frame.set_margin_top(10)

        vbox_inner = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox_inner.set_margin_top(10)
        vbox_inner.set_margin_bottom(10)
        vbox_inner.set_margin_start(10)
        vbox_inner.set_margin_end(10)
        frame.set_child(vbox_inner)

        # Create horizontal box as toolbar replacement (GTK4 doesn't have Toolbar)
        toolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        toolbar.set_margin_top(5)
        toolbar.set_margin_bottom(5)
        toolbar.set_margin_start(5)
        toolbar.set_margin_end(5)
        vbox_inner.append(toolbar)

        # Font family combo
        font_combo = ComboBox()
        fonts = ["Arial", "Times New Roman", "Helvetica", "Georgia", "Verdana", "Courier New"]
        for font in fonts:
            font_combo.append_item(font, font)

        self.font_tool_combo = ToolComboBox(combo=font_combo, label_text="Font:")
        self.font_tool_combo.combo.connect("changed", self.on_font_changed)
        toolbar.append(self.font_tool_combo)

        # Font size combo
        size_combo = ComboBox()
        sizes = [8, 10, 12, 14, 16, 18, 20, 24, 28, 32, 36, 48]
        for size in sizes:
            size_combo.append_item(size, f"{size}pt")

        self.size_tool_combo = ToolComboBox(combo=size_combo, label_text="Size:")
        self.size_tool_combo.combo.connect("changed", self.on_size_changed)
        toolbar.append(self.size_tool_combo)

        # Color combo
        color_combo = ComboBox()
        colors = [
            ("black", "Black"),
            ("red", "Red"),
            ("blue", "Blue"),
            ("green", "Green"),
            ("purple", "Purple"),
            ("orange", "Orange")
        ]
        for color_value, color_name in colors:
            color_combo.append_item(color_value, color_name)

        self.color_tool_combo = ToolComboBox(combo=color_combo, label_text="Color:")
        self.color_tool_combo.combo.connect("changed", self.on_color_changed)
        toolbar.append(self.color_tool_combo)

        # Description
        desc = Gtk.Label(label="Text formatting controls using multiple ToolComboBox widgets")
        desc.set_wrap(True)
        vbox_inner.append(desc)

        parent.append(frame)

    def create_custom_combo_example(self, parent):
        """Create example with custom combo behavior."""
        frame = Gtk.Frame(label="Custom ComboBox Integration")
        frame.set_margin_top(10)

        vbox_inner = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox_inner.set_margin_top(10)
        vbox_inner.set_margin_bottom(10)
        vbox_inner.set_margin_start(10)
        vbox_inner.set_margin_end(10)
        frame.set_child(vbox_inner)

        # Create horizontal box as toolbar replacement (GTK4 doesn't have Toolbar)
        toolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        toolbar.set_margin_top(5)
        toolbar.set_margin_bottom(5)
        toolbar.set_margin_start(5)
        toolbar.set_margin_end(5)
        vbox_inner.append(toolbar)

        custom_combo = ComboBox()

        file_ops = [
            {"action": "new", "label": "New Document", "icon": "document-new"},
            {"action": "open", "label": "Open Document", "icon": "document-open"},
            {"action": "save", "label": "Save Document", "icon": "document-save"}
        ]

        for op in file_ops:
            try:
                custom_combo.append_item(op, op["label"], icon_name=op["icon"])
            except ValueError:
                custom_combo.append_item(op, op["label"])

        custom_combo.append_separator()

        edit_ops = [
            {"action": "copy", "label": "Copy", "icon": "edit-copy"},
            {"action": "paste", "label": "Paste", "icon": "edit-paste"},
            {"action": "undo", "label": "Undo", "icon": "edit-undo"}
        ]

        for op in edit_ops:
            try:
                custom_combo.append_item(op, op["label"], icon_name=op["icon"])
            except ValueError:
                custom_combo.append_item(op, op["label"])

        self.action_tool_combo = ToolComboBox(combo=custom_combo, label_text="Action:")
        self.action_tool_combo.combo.connect("changed", self.on_action_changed)
        toolbar.append(self.action_tool_combo)

        # Add separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        toolbar.append(separator)

        # Combo with no label
        no_label_combo = ComboBox()
        templates = ["Blank", "Letter", "Resume", "Report", "Presentation"]
        for template in templates:
            no_label_combo.append_item(template.lower(), template)

        self.template_tool_combo = ToolComboBox(combo=no_label_combo, label_text="")
        self.template_tool_combo.combo.connect("changed", self.on_template_changed)
        toolbar.append(self.template_tool_combo)

        # Description
        desc = Gtk.Label(label="Custom combo with separators, complex values, and no-label combo")
        desc.set_wrap(True)
        vbox_inner.append(desc)

        parent.append(frame)

    def create_dynamic_toolbar_example(self, parent):
        """Create dynamic toolbar example."""
        frame = Gtk.Frame(label="Dynamic ToolComboBox Management")
        frame.set_margin_top(10)

        vbox_inner = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox_inner.set_margin_top(10)
        vbox_inner.set_margin_bottom(10)
        vbox_inner.set_margin_start(10)
        vbox_inner.set_margin_end(10)
        frame.set_child(vbox_inner)

        # Create horizontal box as toolbar replacement (GTK4 doesn't have Toolbar)
        self.dynamic_toolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.dynamic_toolbar.set_margin_top(5)
        self.dynamic_toolbar.set_margin_bottom(5)
        self.dynamic_toolbar.set_margin_start(5)
        self.dynamic_toolbar.set_margin_end(5)
        vbox_inner.append(self.dynamic_toolbar)

        # Category combo (always present)
        category_combo = ComboBox()
        categories = ["Animals", "Colors", "Countries", "Foods"]
        for category in categories:
            category_combo.append_item(category.lower(), category)

        self.category_tool_combo = ToolComboBox(combo=category_combo, label_text="Category:")
        self.category_tool_combo.combo.connect("changed", self.on_category_changed)
        self.dynamic_toolbar.append(self.category_tool_combo)

        # Placeholder for dynamic combo
        self.dynamic_tool_combo = None

        # Control buttons
        control_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        vbox_inner.append(control_box)

        add_items_btn = Gtk.Button(label="Add Random Items")
        add_items_btn.connect("clicked", self.on_add_items_clicked)
        control_box.append(add_items_btn)

        clear_items_btn = Gtk.Button(label="Clear Items")
        clear_items_btn.connect("clicked", self.on_clear_items_clicked)
        control_box.append(clear_items_btn)

        change_label_btn = Gtk.Button(label="Change Label")
        change_label_btn.connect("clicked", self.on_change_label_clicked)
        control_box.append(change_label_btn)

        # Description
        desc = Gtk.Label(label="Dynamic toolbar that changes content based on category selection")
        desc.set_wrap(True)
        vbox_inner.append(desc)

        parent.append(frame)

    def on_language_changed(self, combo):
        """Handle language selection change."""
        value = combo.get_value()
        item = combo.get_active_item()
        if value and item:
            text = item[1]
            self.status_label.set_text(f"Language changed to: {text} ({value})")

    def on_quality_changed(self, combo):
        """Handle quality selection change."""
        value = combo.get_value()
        if value:
            self.status_label.set_text(f"Quality changed to: {value}")

    def on_font_changed(self, combo):
        """Handle font selection change."""
        value = combo.get_value()
        if value:
            self.status_label.set_text(f"Font changed to: {value}")

    def on_size_changed(self, combo):
        """Handle size selection change."""
        value = combo.get_value()
        if value:
            self.status_label.set_text(f"Font size changed to: {value}pt")

    def on_color_changed(self, combo):
        """Handle color selection change."""
        value = combo.get_value()
        if value:
            self.status_label.set_text(f"Text color changed to: {value}")

    def on_action_changed(self, combo):
        """Handle action selection change."""
        value = combo.get_value()
        if value and isinstance(value, dict):
            action = value["action"]
            label = value["label"]
            self.status_label.set_text(f"Action selected: {label} ({action})")

    def on_template_changed(self, combo):
        """Handle template selection change."""
        value = combo.get_value()
        if value:
            self.status_label.set_text(f"Template selected: {value}")

    def on_category_changed(self, combo):
        """Handle category change - update dynamic combo."""
        category = combo.get_value()
        if not category:
            return

        # Remove existing dynamic combo
        if self.dynamic_tool_combo:
            self.dynamic_toolbar.remove(self.dynamic_tool_combo)

        # Create new combo based on category
        dynamic_combo = ComboBox()

        items_map = {
            "animals": ["Dog", "Cat", "Bird", "Fish", "Rabbit"],
            "colors": ["Red", "Blue", "Green", "Yellow", "Purple"],
            "countries": ["USA", "Canada", "Mexico", "Brazil", "Argentina"],
            "foods": ["Pizza", "Burger", "Salad", "Pasta", "Soup"]
        }

        items = items_map.get(category, [])
        for item in items:
            dynamic_combo.append_item(item.lower(), item)

        self.dynamic_tool_combo = ToolComboBox(combo=dynamic_combo, label_text=f"{category.title()}:")
        self.dynamic_tool_combo.combo.connect("changed", self.on_dynamic_changed)
        self.dynamic_toolbar.append(self.dynamic_tool_combo)

        self.status_label.set_text(f"Category changed to: {category} - new combo created")

    def on_dynamic_changed(self, combo):
        """Handle dynamic combo selection change."""
        value = combo.get_value()
        if value:
            self.status_label.set_text(f"Dynamic selection: {value}")

    def on_add_items_clicked(self, button):
        """Add random items to dynamic combo."""
        if not self.dynamic_tool_combo:
            return

        import random
        items = ["Item A", "Item B", "Item C", "Item D", "Item E"]
        selected_items = random.sample(items, random.randint(1, 3))

        for item in selected_items:
            self.dynamic_tool_combo.combo.append_item(item.lower(), item)

        self.status_label.set_text(f"Added items: {', '.join(selected_items)}")

    def on_clear_items_clicked(self, button):
        """Clear all items from dynamic combo."""
        if not self.dynamic_tool_combo:
            return

        self.dynamic_tool_combo.combo.remove_all()
        self.status_label.set_text("Dynamic combo cleared")

    def on_change_label_clicked(self, button):
        """Change the label of the dynamic combo."""
        if not self.dynamic_tool_combo:
            return

        import random
        labels = ["Selection:", "Choose:", "Pick:", "Option:", "Item:"]
        new_label = random.choice(labels)

        self.dynamic_tool_combo.set_label_text(new_label)
        self.status_label.set_text(f"Dynamic combo label changed to: {new_label}")


class ToolComboBoxApp(Gtk.Application):
    """Main application class."""

    def __init__(self):
        super().__init__(application_id="org.sugarlabs.ToolComboBoxExample")

    def do_activate(self):
        """Activate the application."""
        window = ToolComboBoxExample(self)
        window.present()


def main():
    """Main function."""
    app = ToolComboBoxApp()
    return app.run(sys.argv)


if __name__ == "__main__":
    sys.exit(main())
