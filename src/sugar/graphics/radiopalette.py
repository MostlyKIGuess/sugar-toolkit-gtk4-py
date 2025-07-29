# Copyright (C) 2009, Aleksey Lim
# Copyright (C) 2025 MostlyK
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.
#
# SPDX-License-Identifier: LGPL-2.1-or-later

"""
RadioPalette
=========================

Radio palette provides a way to create radio button groups within palettes,
allowing users to select one option from multiple choices.

This GTK4 port modernizes the radio palette system while maintaining
compatibility with Sugar's palette interface patterns.

Example:

    Create a radio palette with multiple tool options.

    .. code-block:: python

        from gi.repository import Gtk
        from sugar.graphics.radiopalette import RadioToolsButton, RadioPalette
        from sugar.graphics.toolbutton import ToolButton

        # Create the main radio button
        radio_button = RadioToolsButton(
            icon_name='tool-brush',
            tooltip='Drawing Tools'
        )

        # Create the palette
        palette = RadioPalette(primary_text='Drawing Tools')
        radio_button.set_palette(palette)

        # Add tool options
        brush_btn = ToolButton(icon_name='tool-brush')
        palette.append(brush_btn, 'Brush')

        pen_btn = ToolButton(icon_name='tool-pen')
        palette.append(pen_btn, 'Pen')

"""

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("GObject", "2.0")

from gi.repository import Gtk
import logging

from sugar.graphics.toolbutton import ToolButton
from sugar.graphics.palette import Palette

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RadioMenuButton(ToolButton):
    """
    A toolbar button that shows a radio palette when clicked.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_button = None

        invoker = self.get_palette_invoker()
        if invoker:
            # In GTK4, we handle toggle behavior differently
            invoker.set_toggle_palette(True)

        self.set_hide_tooltip_on_click(False)

        self.connect("notify::palette", self._on_palette_changed)

        if self.get_palette():
            self._on_palette_changed(self, None)

    def _on_palette_changed(self, widget, pspec):
        palette = self.get_palette()
        if not isinstance(palette, RadioPalette):
            return
        palette.update_button()

    def get_selected_button(self):
        return self.selected_button

    def set_selected_button(self, button):
        self.selected_button = button


class RadioToolsButton(RadioMenuButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def do_clicked(self):
        if not self.selected_button:
            logger.warning("RadioToolsButton clicked but no button selected")
            return
        self.selected_button.emit("clicked")


class RadioPalette(Palette):
    """
    A palette containing radio button options.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.button_box.set_spacing(6)
        self.button_box.set_homogeneous(True)

        self.set_content(self.button_box)

    def append(self, button, label):
        """
        Add a button option to the radio palette.

        Args:
            button: The ToolButton to add to the radio group
            label: The label text for this option
        """
        if not isinstance(button, ToolButton):
            raise TypeError("Button must be a ToolButton instance")

        if button.get_palette() is not None:
            raise RuntimeError("Radio palette buttons should not have sub-palettes")

        button.palette_label = label

        button.connect("clicked", self._on_button_clicked)

        self.button_box.append(button)

        children_count = 0
        child = self.button_box.get_first_child()
        while child:
            children_count += 1
            child = child.get_next_sibling()

        if children_count == 1:
            self._on_button_clicked(button)

    def update_button(self):
        child = self.button_box.get_first_child()
        while child:
            if hasattr(child, "get_active") and child.get_active():
                self._on_button_clicked(child)
                break
            child = child.get_next_sibling()

    def _on_button_clicked(self, button):
        if not hasattr(button, "get_active") or not button.get_active():
            if hasattr(button, "set_active"):
                button.set_active(True)

        if hasattr(button, "palette_label"):
            self.set_primary_text(button.palette_label)

        self.popdown(immediate=True)

        invoker = self.get_invoker()
        if invoker and hasattr(invoker, "parent"):
            parent = invoker.parent
            if isinstance(parent, RadioMenuButton):
                if hasattr(button, "palette_label"):
                    parent.set_label(button.palette_label)

                icon_name = button.get_icon_name()
                if icon_name:
                    parent.set_icon_name(icon_name)

                parent.set_selected_button(button)

    def get_buttons(self):
        buttons = []
        child = self.button_box.get_first_child()
        while child:
            if isinstance(child, ToolButton):
                buttons.append(child)
            child = child.get_next_sibling()
        return buttons

    def get_selected_button(self):
        child = self.button_box.get_first_child()
        while child:
            if hasattr(child, "get_active") and child.get_active():
                return child
            child = child.get_next_sibling()
        return None
