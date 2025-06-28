"""
Sugar Toolkit GTK4 Python
==========================

A modern GTK4 port of the Sugar Toolkit for Python activities.

This package provides the core functionality needed to create Sugar activities
using GTK4, maintaining compatibility with Sugar's educational framework while
leveraging modern GTK4 features.

Modules:
    activity: Core activity classes and functionality
    graphics: Visual components, styling, and UI widgets
    bundle: Activity bundle management
"""

__version__ = "0.1.0"
__author__ = "Sugar Labs Community"
__license__ = "LGPL-2.1-or-later"

from .activity.activity import Activity, SimpleActivity
from .graphics.xocolor import XoColor
from .graphics.icon import Icon, EventIcon
# from .graphics.tray import HTray, VTray, TrayButton, TrayIcon
# from .graphics.window import Window, UnfullscreenButton
from .graphics.menuitem import MenuItem, MenuSeparator
# from .graphics.toolbox import Toolbox
from .graphics import style

__all__ = [
    "Activity",
    "SimpleActivity",
    "XoColor",
    "Icon",
    "EventIcon",
    # "HTray",
    # "VTray",
    # "TrayButton",
    # "TrayIcon",
    # "Window",
    # "UnfullscreenButton",
    "MenuItem",
    "MenuSeparator",
    # "Toolbox",
    "style",
]
