# Copyright (C) 2006-2007 Red Hat, Inc.
# Copyright (C) 2007-2009 One Laptop Per Child
# Copyright (C) 2010 Collabora Ltd. <http://www.collabora.co.uk/>
# Copyright (C) 2025 MostlyK
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#
# SPDX-License-Identifier: LGPL-2.1-or-later

"""
Activity - GTK4 Port
====================

A definitive reference for what a Sugar Python activity must do to
participate in the Sugar desktop - GTK4 version.

This is a modernized port of the sugar3.activity.activity module for GTK4.

.. note:: This API is under development for GTK4.

The :class:`Activity` class is used to derive all Sugar Python
activities using GTK4.

Basic Usage


        from sugar.activity import Activity

        class MyActivity(Activity):
            def __init__(self):
                Activity.__init__(self)

                # Set up your UI here
                label = Gtk.Label(label="Hello, Sugar GTK4!")
                self.set_canvas(label)

"""

import os
import logging
import time
from pathlib import Path

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
gi.require_version("GLib", "2.0")
gi.require_version("GObject", "2.0")
gi.require_version("Gio", "2.0")

from gi.repository import GObject, Gdk, Gtk

SCOPE_PRIVATE = "private"
SCOPE_INVITE_ONLY = "invite"
SCOPE_NEIGHBORHOOD = "public"

PREVIEW_SIZE = (300, 225)
"""Size of a preview image for journal object metadata."""


class Activity(Gtk.ApplicationWindow):
    """
    Base Activity class for GTK4 Sugar activities.

    This is a modernized version of the Sugar Activity class that uses
    GTK4 features and follows modern Python practices.

    **Signals:**
        * **shared** - the activity has been shared on a network
        * **joined** - the activity has joined a shared network activity
        * **closing** - the activity is about to close

    Args:
        application (Gtk.Application, optional): The GTK application
    """

    __gtype_name__ = "SugarGtk4Activity"

    __gsignals__ = {
        "shared": (GObject.SignalFlags.RUN_FIRST, None, ()),
        "joined": (GObject.SignalFlags.RUN_FIRST, None, ()),
        "closing": (GObject.SignalFlags.RUN_FIRST, None, ()),
    }

    def __init__(self, application=None):
        super().__init__(application=application)

        # Basic activity properties
        self._activity_id = self._generate_activity_id()
        self._canvas = None
        self._is_shared = False
        self._active = True
        self._active_time = time.time()
        self._spent_time = 0
        self._metadata = {}

        # Set up the window
        self._setup_window()

        # Initialize activity
        self._initialize_activity()

        logging.info(f"Activity initialized with ID: {self._activity_id}")

    def _generate_activity_id(self):
        """Generate a unique activity ID."""
        import uuid

        return str(uuid.uuid4())

    def _setup_window(self):
        """Set up the main window properties."""
        self.set_title("Sugar Activity")
        self.set_default_size(800, 600)

        # Sets up CSS for Sugar styling
        self._setup_styling()

        # Connect signals
        self.connect("close-request", self._on_close_request)

    def _setup_styling(self):
        """Set up CSS styling for Sugar look and feel."""
        css_provider = Gtk.CssProvider()
        css_data = """
        window.sugar-activity {
            background-color: #ffffff;
            color: #000000;
        }
        
        .sugar-toolbar {
            background-color: #c0c0c0;
            border-bottom: 1px solid #808080;
            padding: 4px;
        }
        
        .sugar-button {
            border-radius: 4px;
            padding: 8px 12px;
            margin: 2px;
        }
        """

        css_provider.load_from_string(css_data)

        # Add CSS to default display
        display = Gdk.Display.get_default()
        Gtk.StyleContext.add_provider_for_display(
            display, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        # Add CSS class to window
        self.add_css_class("sugar-activity")

    def _initialize_activity(self):
        """Initialize activity-specific settings."""
        # Set up metadata
        self._metadata = {
            "title": "Sugar Activity",
            "activity_id": self._activity_id,
            "creation_time": str(int(time.time())),
            "spent_time": "0",
        }

        # Create initial canvas container
        self._main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_child(self._main_box)

    def get_id(self):
        """
        Get the activity ID.

        Returns:
            str: The unique activity identifier
        """
        return self._activity_id

    def get_canvas(self):
        """
        Get the canvas widget.

        Returns:
            Gtk.Widget or None: The current canvas widget
        """
        return self._canvas

    def set_canvas(self, canvas):
        """
        Set the canvas widget.

        Args:
            canvas (Gtk.Widget): The widget to use as the main canvas
        """
        if self._canvas:
            self._main_box.remove(self._canvas)

        self._canvas = canvas
        if canvas:
            self._main_box.append(canvas)

    def get_title(self):
        """Get the activity title."""
        return self._metadata.get("title", "Sugar Activity")

    def set_title(self, title):
        """
        Set the activity title.

        Args:
            title (str): The new title for the activity
        """
        self._metadata["title"] = title
        super().set_title(title)

    def get_active(self):
        """
        Get whether the activity is active.

        Returns:
            bool: True if the activity is active
        """
        return self._active

    def set_active(self, active):
        """
        Set whether the activity is active.

        Args:
            active (bool): Whether the activity should be active
        """
        if self._active != active:
            self._active = active
            self._update_spent_time()

    def _update_spent_time(self):
        """Update the time spent in this activity."""
        current_time = time.time()
        if self._active and self._active_time:
            self._spent_time += current_time - self._active_time
        self._active_time = current_time if self._active else None

    def get_metadata(self):
        """
        Get the activity metadata.

        Returns:
            dict: Activity metadata dictionary
        """
        return self._metadata

    def save(self):
        """
        Save the activity state.

        Subclasses should override this method to save their specific data.
        """
        self._update_spent_time()
        self._metadata["spent_time"] = str(int(self._spent_time))
        logging.info("Activity saved")

    def close(self):
        """Close the activity."""
        self.emit("closing")
        self.save()
        if self.get_application():
            self.get_application().quit()
        else:
            self.destroy()

    def _on_close_request(self, window):
        """Handle the close request."""
        self.close()
        return True

    def share(self, private=False):
        """
        Share the activity (placeholder for future implementation).

        Args:
            private (bool): Whether to share privately
        """
        logging.info(f"Activity sharing requested (private={private})")
        self._is_shared = True
        self.emit("shared")

    def get_shared(self):
        """
        Get whether the activity is shared.

        Returns:
            bool: True if the activity is shared
        """
        return self._is_shared

    # NOTE: Underdevelopment!! Following methods are placeholders
    def read_file(self, file_path):
        """
        Read activity data from a file.

        Subclasses should override this method.

        Args:
            file_path (str): Path to the file to read
        """
        pass

    def write_file(self, file_path):
        """
        Write activity data to a file.

        Subclasses should override this method.

        Args:
            file_path (str): Path to the file to write
        """
        pass

    def can_close(self):
        """
        Check if the activity can be closed.

        Returns:
            bool: True if the activity can be closed
        """
        return True


class SimpleActivity(Activity):
    """
    A simple activity implementation for quick prototyping.

    This provides a basic activity with a toolbar and content area.
    """

    def __init__(self, application=None):
        super().__init__(application=application)

        # Create toolbar
        self._create_toolbar()

        # Create content area
        self._create_content_area()

    def _create_toolbar(self):
        """Create a simple toolbar."""
        toolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        toolbar.add_css_class("sugar-toolbar")

        # Title label
        title_label = Gtk.Label(label=self.get_title())
        title_label.set_hexpand(True)
        title_label.set_halign(Gtk.Align.START)
        toolbar.append(title_label)

        # Close button
        close_button = Gtk.Button(label="×")
        close_button.add_css_class("sugar-button")
        close_button.connect("clicked", lambda w: self.close())
        toolbar.append(close_button)

        self._main_box.prepend(toolbar)

    def _create_content_area(self):
        """Create the main content area."""
        content = Gtk.Label(label="Sugar GTK4 Activity\n\nReady for development!")
        content.set_vexpand(True)
        content.set_halign(Gtk.Align.CENTER)
        content.set_valign(Gtk.Align.CENTER)

        self.set_canvas(content)


def get_bundle_name():
    """Get the bundle name from environment or default."""
    return os.environ.get("SUGAR_BUNDLE_NAME", "Sugar GTK4 Activity")


def get_bundle_path():
    """Get the bundle path from environment or current directory."""
    return os.environ.get("SUGAR_BUNDLE_PATH", os.getcwd())


def get_activity_root():
    """Get the activity root directory for data storage."""
    if "SUGAR_ACTIVITY_ROOT" in os.environ:
        return os.environ["SUGAR_ACTIVITY_ROOT"]

    # Fallback to user data directory
    data_dir = Path.home() / ".local" / "share" / "sugar-gtk4"
    data_dir.mkdir(parents=True, exist_ok=True)
    return str(data_dir)
