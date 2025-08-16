#!/usr/bin/env python3
"""
Activity Example
======================

This example demonstrates how to create a simple Sugar activity using GTK4.
It shows the basic structure and key features of a Sugar activity.

This example runs WITHOUT the datastore/journal system for simplicity.
"""

import logging
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

if 'SUGAR_BUNDLE_ID' not in os.environ:
    os.environ['SUGAR_BUNDLE_ID'] = 'org.sugarlabs.BasicExample'
    os.environ['SUGAR_BUNDLE_NAME'] = 'Basic Example'
    os.environ['SUGAR_BUNDLE_PATH'] = os.path.dirname(__file__)
    os.environ['SUGAR_ACTIVITY_ROOT'] = '/tmp/basic_example'

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
gi.require_version("GLib", "2.0")

from gi.repository import Gtk, GLib, Gio

from sugar.activity.activity import Activity
from sugar.activity.activityhandle import ActivityHandle
from sugar.graphics.toolbarbox import ToolbarBox
from sugar.activity.widgets import ActivityToolbarButton, StopButton
from sugar.graphics.alert import Alert
from sugar.graphics.icon import Icon
import json


class BasicExampleActivity(Activity):
    """A basic example Sugar activity demonstrating key features."""

    def __init__(self, handle=None, application=None):
        """Initialize the activity."""
        # Create handle if not provided (for testing)
        if handle is None:
            handle = ActivityHandle('basic-example-123')

        # Initialize the parent
        Activity.__init__(self, handle, application=application)

        self._text_content = ""
        self._counter = 0

        self._setup_ui()

        self.set_title("Basic Sugar Activity Example")
        self.set_default_size(800, 600)

    def _setup_ui(self):
        """Set up the user interface."""
        self._create_toolbar()

        self._create_canvas()

    def _create_toolbar(self):
        """Create the activity toolbar."""
        toolbar_box = ToolbarBox()

        # Activity button (provides standard activity menu)
        activity_button = ActivityToolbarButton(self)
        toolbar_box.toolbar.append(activity_button)

        # Add separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        toolbar_box.toolbar.append(separator)

        # Add custom button
        hello_button = Gtk.Button()
        hello_button.set_label("Say Hello")
        hello_button.connect('clicked', self._hello_button_clicked)
        toolbar_box.toolbar.append(hello_button)

        # Add counter button
        counter_button = Gtk.Button()
        counter_button.set_label("Count")
        counter_button.connect('clicked', self._counter_button_clicked)
        toolbar_box.toolbar.append(counter_button)

        # Add notification button
        notify_button = Gtk.Button()
        notify_button.set_label("Notify")
        notify_button.connect('clicked', self._notify_button_clicked)
        toolbar_box.toolbar.append(notify_button)

        # Add save button
        save_button = Gtk.Button()
        save_button.set_label("Save to File")
        save_button.connect('clicked', self._save_button_clicked)
        toolbar_box.toolbar.append(save_button)

        # Add load button
        load_button = Gtk.Button()
        load_button.set_label("Load from File")
        load_button.connect('clicked', self._load_button_clicked)
        toolbar_box.toolbar.append(load_button)

        # Add spacer to push stop button to the right
        spacer = Gtk.Box()
        spacer.set_hexpand(True)
        toolbar_box.toolbar.append(spacer)

        # Stop button
        stop_button = StopButton(self)
        toolbar_box.toolbar.append(stop_button)

        # Set the toolbar
        self.set_toolbar_box(toolbar_box)

    def _create_canvas(self):
        """Create the main canvas area."""
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        main_box.set_margin_top(24)
        main_box.set_margin_bottom(24)
        main_box.set_margin_start(24)
        main_box.set_margin_end(24)

        # Title
        title_label = Gtk.Label()
        title_label.set_markup("<span size='x-large' weight='bold'>Basic Sugar Activity Example</span>")
        title_label.set_halign(Gtk.Align.CENTER)
        main_box.append(title_label)

        # Subtitle
        subtitle_label = Gtk.Label()
        subtitle_label.set_markup("<span style='italic'>Running with Sugar Activity framework</span>")
        subtitle_label.set_halign(Gtk.Align.CENTER)
        main_box.append(subtitle_label)

        self._status_label = Gtk.Label()
        self._status_label.set_text("Welcome! Click the toolbar buttons to test features.")
        self._status_label.set_halign(Gtk.Align.CENTER)
        self._status_label.set_wrap(True)
        main_box.append(self._status_label)

        text_frame = Gtk.Frame()
        text_frame.set_label("Text Content (can be saved to file)")

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_min_content_height(200)

        self._text_view = Gtk.TextView()
        self._text_view.set_wrap_mode(Gtk.WrapMode.WORD)
        self._text_buffer = self._text_view.get_buffer()
        self._text_buffer.connect('changed', self._text_changed_cb)

        scrolled.set_child(self._text_view)
        text_frame.set_child(scrolled)
        main_box.append(text_frame)

        self._counter_label = Gtk.Label()
        self._counter_label.set_text(f"Counter: {self._counter}")
        self._counter_label.set_halign(Gtk.Align.CENTER)
        main_box.append(self._counter_label)

        info_frame = Gtk.Frame()
        info_frame.set_label("Activity Information")

        info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        info_box.set_margin_top(12)
        info_box.set_margin_bottom(12)
        info_box.set_margin_start(12)
        info_box.set_margin_end(12)

        id_label = Gtk.Label()
        id_label.set_markup(f"<b>Activity ID:</b> {self.get_id()}")
        id_label.set_halign(Gtk.Align.START)
        info_box.append(id_label)

        bundle_label = Gtk.Label()
        bundle_label.set_markup(f"<b>Bundle ID:</b> {self.get_bundle_id()}")
        bundle_label.set_halign(Gtk.Align.START)
        info_box.append(bundle_label)

        name_label = Gtk.Label()
        name_label.set_markup(f"<b>Bundle Name:</b> {os.environ.get('SUGAR_BUNDLE_NAME', 'N/A')}")
        name_label.set_halign(Gtk.Align.START)
        info_box.append(name_label)

        self._active_label = Gtk.Label()
        self._update_active_label()
        self._active_label.set_halign(Gtk.Align.START)
        info_box.append(self._active_label)

        self._shared_label = Gtk.Label()
        self._update_shared_label()
        self._shared_label.set_halign(Gtk.Align.START)
        info_box.append(self._shared_label)

        info_frame.set_child(info_box)
        main_box.append(info_frame)

        self.set_canvas(main_box)

    def _update_active_label(self):
        """Update the active state label."""
        if hasattr(self, '_active_label'):
            self._active_label.set_markup(f"<b>Active:</b> {self.get_active()}")

    def _update_shared_label(self):
        """Update the shared state label."""
        if hasattr(self, '_shared_label'):
            self._shared_label.set_markup(f"<b>Shared:</b> {self.get_shared()}")

    def _hello_button_clicked(self, button):
        """Handle hello button click."""
        self._status_label.set_text("Hello! This is a Sugar Activity running on GTK4.")

        alert = Alert()
        alert.props.title = 'Hello!'
        alert.props.msg = 'This demonstrates the alert system in Sugar GTK4.'

        ok_icon = Icon(icon_name='dialog-ok')
        alert.add_button(Gtk.ResponseType.OK, 'OK', ok_icon)
        alert.connect('response', self._alert_response_cb)

        self.add_alert(alert)

    def _counter_button_clicked(self, button):
        """Handle counter button click."""
        self._counter += 1
        self._counter_label.set_text(f"Counter: {self._counter}")
        self._status_label.set_text(f"Counter incremented to {self._counter}")

    def _notify_button_clicked(self, button):
        """Handle notification button click."""
        if hasattr(self, 'notify_user'):
            try:
                self.notify_user('Test Notification',
                               f'This is a test notification from the activity. Counter: {self._counter}')
                self._status_label.set_text("Notification sent!")
            except Exception as e:
                self._status_label.set_text(f"Notification error: {e}")
        else:
            if self.get_application():
                notification = Gio.Notification.new("Test Notification")
                notification.set_body(f"This is a test notification from the activity. Counter: {self._counter}")
                self.get_application().send_notification(self.get_id(), notification)
                self._status_label.set_text("Notification sent!")
            else:
                self._status_label.set_text("Notification: No application context available")

    def _save_button_clicked(self, button):
        """Handle save button click."""
        try:
            save_dir = os.path.expanduser("~/Documents/SugarActivity")
            os.makedirs(save_dir, exist_ok=True)

            file_path = os.path.join(save_dir, f"activity_data_{self.get_id()}.json")

            data = {
                'text_content': self._text_content,
                'counter': self._counter,
                'activity_id': self.get_id(),
                'bundle_id': self.get_bundle_id(),
                'saved_at': GLib.DateTime.new_now_local().format_iso8601()
            }

            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)

            self._status_label.set_text(f"Saved to {file_path}")

        except Exception as e:
            self._status_label.set_text(f"Save error: {e}")

    def _load_button_clicked(self, button):
        """Handle load button click."""
        try:
            file_path = os.path.join(os.path.expanduser("~/Documents/SugarActivity"),
                                   f"activity_data_{self.get_id()}.json")

            if not os.path.exists(file_path):
                self._status_label.set_text("No saved file found")
                return

            with open(file_path, 'r') as f:
                data = json.load(f)

            self._text_content = data.get('text_content', '')
            if self._text_buffer:
                self._text_buffer.set_text(self._text_content)

            self._counter = data.get('counter', 0)
            if hasattr(self, '_counter_label'):
                self._counter_label.set_text(f"Counter: {self._counter}")

            saved_at = data.get('saved_at', 'unknown time')
            self._status_label.set_text(f"Loaded from file (saved at {saved_at[:19]})")

        except Exception as e:
            self._status_label.set_text(f"Load error: {e}")

    def _alert_response_cb(self, alert, response_id):
        """Handle alert response."""
        self.remove_alert(alert)
        if response_id == Gtk.ResponseType.OK:
            self._status_label.set_text("Alert dismissed")

    def _text_changed_cb(self, text_buffer):
        """Handle text buffer changes."""
        start_iter = text_buffer.get_start_iter()
        end_iter = text_buffer.get_end_iter()
        self._text_content = text_buffer.get_text(start_iter, end_iter, False)

    def set_active(self, active):
        """Override set_active to update our display."""
        Activity.set_active(self, active)
        self._update_active_label()

        if active:
            self._status_label.set_text("Activity is now active")
        else:
            self._status_label.set_text("Activity is now inactive")

    # Override Activity file methods
    def read_file(self, file_path):
        """Read activity data from file."""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)

            self._text_content = data.get('text_content', '')
            if hasattr(self, '_text_buffer'):
                self._text_buffer.set_text(self._text_content)

            self._counter = data.get('counter', 0)
            if hasattr(self, '_counter_label'):
                self._counter_label.set_text(f"Counter: {self._counter}")

        except Exception as e:
            logging.error(f"Error reading file: {e}")

    def write_file(self, file_path):
        """Write activity data to file."""
        try:
            data = {
                'text_content': self._text_content,
                'counter': self._counter,
                'activity_id': self.get_id(),
                'bundle_id': self.get_bundle_id(),
                'saved_at': GLib.DateTime.new_now_local().format_iso8601()
            }

            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            logging.error(f"Error writing file: {e}")
            raise


class BasicExampleApplication(Gtk.Application):
    """Application wrapper for the activity."""

    def __init__(self):
        super().__init__(application_id='org.sugarlabs.BasicExample',
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
        self.activity = None

    def do_activate(self):
        """Activate the application."""
        if not self.activity:
            # Create activity handle
            handle = ActivityHandle('basic-example-123')

            # Create the activity
            self.activity = BasicExampleActivity(handle, application=self)

            # Present the activity window
            self.activity.present()


def main():
    """Main entry point."""
    logging.basicConfig(level=logging.INFO)

    app = BasicExampleApplication()
    return app.run(sys.argv)


if __name__ == "__main__":
    sys.exit(main())
