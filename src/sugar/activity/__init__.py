"""
Activity Module
===============

Core activity classes and functionality for Sugar GTK4 activities.
"""

# Set GTK version requirements before any GTK imports
try:
    import gi

    gi.require_version("Gtk", "4.0")
    gi.require_version("Gdk", "4.0")
    gi.require_version("GObject", "2.0")
    gi.require_version("Gio", "2.0")
    gi.require_version("GLib", "2.0")
    gi.require_version("Pango", "1.0")
    gi.require_version("GdkPixbuf", "2.0")
except ImportError:
    # gi might not be available during docs build
    pass

from .activity import Activity, SimpleActivity

__all__ = ["Activity", "SimpleActivity"]
