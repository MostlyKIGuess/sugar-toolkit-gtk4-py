# Copyright (C) 2007, Red Hat, Inc.
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

"""
STABLE.
"""

from gi.repository import Gtk
from gi.repository import GObject

from sugar.graphics.combobox import ComboBox
from sugar.graphics import style


class ToolComboBox(Gtk.Box):
    def __init__(self, combo=None, label_text="", **kwargs):
        self.label = None
        self._label_text = label_text

        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=style.DEFAULT_SPACING, **kwargs)

        self.set_margin_top(style.DEFAULT_PADDING)
        self.set_margin_bottom(style.DEFAULT_PADDING)
        self.set_margin_start(style.DEFAULT_PADDING)
        self.set_margin_end(style.DEFAULT_PADDING)

        self.label = Gtk.Label(label=self._label_text)
        self.append(self.label)

        if combo:
            self.combo = combo
        else:
            self.combo = ComboBox()

        self.append(self.combo)

    def do_set_property(self, pspec, value):
        if pspec.name == "label-text":
            self._label_text = value
            if self.label:
                self.label.set_text(self._label_text)

    def set_label_text(self, text):
        """Set the label text."""
        self._label_text = text
        if self.label:
            self.label.set_text(self._label_text)

    def get_label_text(self):
        """Get the label text."""
        return self._label_text
