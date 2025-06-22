# Copyright (C) 2006-2007 Red Hat, Inc.
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
XoColor - GTK4 Port
===================

This class represents all of the colors that the XO can take on.
Each pair of colors represents the fill color and the stroke color.

Ported to GTK4 from sugar3.graphics.xocolor
"""

import random
import logging

import gi

gi.require_version("Gio", "2.0")
from gi.repository import Gio

# Standard Sugar XO Colors palette
colors = [
    ["#B20008", "#FF2B34"],
    ["#FF2B34", "#B20008"],
    ["#E6000A", "#FF2B34"],
    ["#FF2B34", "#E6000A"],
    ["#FFADCE", "#FF2B34"],
    ["#9A5200", "#FF2B34"],
    ["#FF2B34", "#9A5200"],
    ["#FF8F00", "#FF2B34"],
    ["#FF2B34", "#FF8F00"],
    ["#FFC169", "#FF2B34"],
    ["#807500", "#FF2B34"],
    ["#FF2B34", "#807500"],
    ["#BE9E00", "#FF2B34"],
    ["#FF2B34", "#BE9E00"],
    ["#F8E800", "#FF2B34"],
    ["#008009", "#FF2B34"],
    ["#FF2B34", "#008009"],
    ["#00B20D", "#FF2B34"],
    ["#FF2B34", "#00B20D"],
    ["#8BFF7A", "#FF2B34"],
    ["#00588C", "#FF2B34"],
    ["#FF2B34", "#00588C"],
    ["#005FE4", "#FF2B34"],
    ["#FF2B34", "#005FE4"],
    ["#BCCDFF", "#FF2B34"],
    ["#5E008C", "#FF2B34"],
    ["#FF2B34", "#5E008C"],
    ["#7F00BF", "#FF2B34"],
    ["#FF2B34", "#7F00BF"],
    ["#D1A3FF", "#FF2B34"],
    ["#9A5200", "#FF8F00"],
    ["#FF8F00", "#9A5200"],
    ["#C97E00", "#FF8F00"],
    ["#FF8F00", "#C97E00"],
    ["#FFC169", "#FF8F00"],
    ["#807500", "#FF8F00"],
    ["#FF8F00", "#807500"],
    ["#BE9E00", "#FF8F00"],
    ["#FF8F00", "#BE9E00"],
    ["#F8E800", "#FF8F00"],
    ["#008009", "#FF8F00"],
    ["#FF8F00", "#008009"],
    ["#00B20D", "#FF8F00"],
    ["#FF8F00", "#00B20D"],
    ["#8BFF7A", "#FF8F00"],
    ["#00588C", "#FF8F00"],
    ["#FF8F00", "#00588C"],
    ["#005FE4", "#FF8F00"],
    ["#FF8F00", "#005FE4"],
    ["#BCCDFF", "#FF8F00"],
    ["#5E008C", "#FF8F00"],
    ["#FF8F00", "#5E008C"],
    ["#A700FF", "#FF8F00"],
    ["#FF8F00", "#A700FF"],
    ["#D1A3FF", "#FF8F00"],
    ["#B20008", "#FF8F00"],
    ["#FF8F00", "#B20008"],
    ["#FF2B34", "#FF8F00"],
    ["#FF8F00", "#FF2B34"],
    ["#FFADCE", "#FF8F00"],
    ["#807500", "#F8E800"],
    ["#F8E800", "#807500"],
    ["#BE9E00", "#F8E800"],
    ["#F8E800", "#BE9E00"],
    ["#FFFA00", "#EDDE00"],
    ["#008009", "#F8E800"],
    ["#F8E800", "#008009"],
    ["#00EA11", "#F8E800"],
    ["#F8E800", "#00EA11"],
    ["#8BFF7A", "#F8E800"],
    ["#00588C", "#F8E800"],
    ["#F8E800", "#00588C"],
    ["#00A0FF", "#F8E800"],
    ["#F8E800", "#00A0FF"],
    ["#BCCEFF", "#F8E800"],
    ["#5E008C", "#F8E800"],
    ["#F8E800", "#5E008C"],
    ["#AC32FF", "#F8E800"],
    ["#F8E800", "#AC32FF"],
    ["#D1A3FF", "#F8E800"],
    ["#B20008", "#F8E800"],
    ["#F8E800", "#B20008"],
    ["#FF2B34", "#F8E800"],
    ["#F8E800", "#FF2B34"],
    ["#FFADCE", "#F8E800"],
    ["#9A5200", "#F8E800"],
    ["#F8E800", "#9A5200"],
    ["#FF8F00", "#F8E800"],
    ["#F8E800", "#FF8F00"],
    ["#FFC169", "#F8E800"],
    ["#008009", "#00EA11"],
    ["#00EA11", "#008009"],
    ["#00B20D", "#00EA11"],
    ["#00EA11", "#00B20D"],
    ["#8BFF7A", "#00EA11"],
    ["#00588C", "#00EA11"],
    ["#00EA11", "#00588C"],
    ["#005FE4", "#00EA11"],
    ["#00EA11", "#005FE4"],
    ["#BCCDFF", "#00EA11"],
    ["#5E008C", "#00EA11"],
    ["#00EA11", "#5E008C"],
    ["#7F00BF", "#00EA11"],
    ["#00EA11", "#7F00BF"],
    ["#D1A3FF", "#00EA11"],
    ["#B20008", "#00EA11"],
    ["#00EA11", "#B20008"],
    ["#FF2B34", "#00EA11"],
    ["#00EA11", "#FF2B34"],
    ["#FFADCE", "#00EA11"],
    ["#9A5200", "#00EA11"],
    ["#00EA11", "#9A5200"],
    ["#FF8F00", "#00EA11"],
    ["#00EA11", "#FF8F00"],
    ["#FFC169", "#00EA11"],
    ["#807500", "#00EA11"],
    ["#00EA11", "#807500"],
    ["#BE9E00", "#00EA11"],
    ["#00EA11", "#BE9E00"],
    ["#F8E800", "#00EA11"],
    ["#00588C", "#00A0FF"],
    ["#00A0FF", "#00588C"],
    ["#005FE4", "#00A0FF"],
    ["#00A0FF", "#005FE4"],
    ["#BCCDFF", "#00A0FF"],
    ["#5E008C", "#00A0FF"],
    ["#00A0FF", "#5E008C"],
    ["#9900E6", "#00A0FF"],
    ["#00A0FF", "#9900E6"],
    ["#D1A3FF", "#00A0FF"],
    ["#B20008", "#00A0FF"],
    ["#00A0FF", "#B20008"],
    ["#FF2B34", "#00A0FF"],
    ["#00A0FF", "#FF2B34"],
    ["#FFADCE", "#00A0FF"],
    ["#9A5200", "#00A0FF"],
    ["#00A0FF", "#9A5200"],
    ["#FF8F00", "#00A0FF"],
    ["#00A0FF", "#FF8F00"],
    ["#FFC169", "#00A0FF"],
    ["#807500", "#00A0FF"],
    ["#00A0FF", "#807500"],
    ["#BE9E00", "#00A0FF"],
    ["#00A0FF", "#BE9E00"],
    ["#F8E800", "#00A0FF"],
    ["#008009", "#00A0FF"],
    ["#00A0FF", "#008009"],
    ["#00B20D", "#00A0FF"],
    ["#00A0FF", "#00B20D"],
    ["#8BFF7A", "#00A0FF"],
    ["#5E008C", "#AC32FF"],
    ["#AC32FF", "#5E008C"],
    ["#7F00BF", "#AC32FF"],
    ["#AC32FF", "#7F00BF"],
    ["#D1A3FF", "#AC32FF"],
    ["#B20008", "#AC32FF"],
    ["#AC32FF", "#B20008"],
    ["#FF2B34", "#AC32FF"],
    ["#AC32FF", "#FF2B34"],
    ["#FFADCE", "#AC32FF"],
    ["#9A5200", "#AC32FF"],
    ["#AC32FF", "#9A5200"],
    ["#FF8F00", "#AC32FF"],
    ["#AC32FF", "#FF8F00"],
    ["#FFC169", "#AC32FF"],
    ["#807500", "#AC32FF"],
    ["#AC32FF", "#807500"],
    ["#BE9E00", "#AC32FF"],
    ["#AC32FF", "#BE9E00"],
    ["#F8E800", "#AC32FF"],
    ["#008009", "#AC32FF"],
    ["#AC32FF", "#008009"],
    ["#00B20D", "#AC32FF"],
    ["#AC32FF", "#00B20D"],
    ["#8BFF7A", "#AC32FF"],
    ["#00588C", "#AC32FF"],
    ["#AC32FF", "#00588C"],
    ["#005FE4", "#AC32FF"],
    ["#AC32FF", "#005FE4"],
    ["#BCCDFF", "#AC32FF"],
]


def _parse_string(color_string):
    """
    Parse a color string into stroke and fill colors.

    Args:
        color_string (str): two html format strings separated by a comma,
                           "white", or "insensitive"

    Returns:
        list or None: [stroke_color, fill_color] or None if parsing fails
    """
    if not isinstance(color_string, str):
        logging.error("Invalid color string: %r", color_string)
        return None

    if color_string == "white":
        return ["#ffffff", "#414141"]
    elif color_string == "insensitive":
        return ["#ffffff", "#e2e2e2"]

    splitted = color_string.split(",")
    if len(splitted) == 2:
        return [splitted[0], splitted[1]]
    else:
        return None


class XoColor:
    """
    Defines color for XO

    This class represents a pair of colors (stroke and fill) that can be
    used throughout Sugar activities. Colors can be parsed from strings,
    loaded from user settings, or chosen randomly.

    Args:
        color_string (str, optional): Color specification in one of these formats:
            - "stroke_hex,fill_hex" (e.g., "#FF0000,#00FF00")
            - "white" for white theme
            - "insensitive" for disabled/grayed theme
            - None to use user's color from settings or random if not available

    Examples:
        >>> #from string
        >>> color = XoColor("#FF0000,#00FF00")
        >>> print(color.get_stroke_color())  # "#FF0000"
        >>> print(color.get_fill_color())    # "#00FF00"

        >>> # create user's color (or random if not set)
        >>> color = XoColor()

        >>> # themed colors
        >>> white_color = XoColor("white")
        >>> disabled_color = XoColor("insensitive")
    """

    def __init__(self, color_string=None):
        parsed_color = None

        if color_string is None:
            if "org.sugarlabs.user" in Gio.Settings.list_schemas():
                try:
                    settings = Gio.Settings("org.sugarlabs.user")
                    color_string = settings.get_string("color")
                except Exception as e:
                    logging.debug("Could not load user color from settings: %s", e)
                    color_string = None

        if color_string is not None:
            parsed_color = _parse_string(color_string)

        if parsed_color is None:
            n = int(random.random() * len(colors))
            self.stroke, self.fill = colors[n]
        else:
            self.stroke, self.fill = parsed_color

    def __eq__(self, other):
        """
        Check if two XoColor objects are equal.

        Args:
            other (object): Another XoColor object to compare

        Returns:
            bool: True if both stroke and fill colors match
        """
        if isinstance(other, XoColor):
            return self.stroke == other.stroke and self.fill == other.fill
        return False

    def __ne__(self, other):
        """Check if two XoColor objects are not equal."""
        return not self.__eq__(other)

    def __hash__(self):
        """Make XoColor hashable for use in sets and as dict keys."""
        return hash((self.stroke, self.fill))

    def __str__(self):
        """String representation of XoColor."""
        return f"XoColor(stroke={self.stroke}, fill={self.fill})"

    def __repr__(self):
        """Detailed string representation of XoColor."""
        return f'XoColor("{self.to_string()}")'

    def get_stroke_color(self):
        """
        Returns:
            str: stroke color in HTML hex format (#RRGGBB)
        """
        return self.stroke

    def get_fill_color(self):
        """
        Returns:
            str: fill color in HTML hex format (#RRGGBB)
        """
        return self.fill

    def to_string(self):
        """
        Returns:
            str: formatted string in the format "#STROKEHEX,#FILLHEX"
        """
        return f"{self.stroke},{self.fill}"

    @classmethod
    def from_string(cls, color_string):
        """
        Create XoColor from string representation.

        Args:
            color_string (str): Color string to parse

        Returns:
            XoColor: New XoColor instance

        Raises:
            ValueError: If color_string cannot be parsed
        """
        parsed = _parse_string(color_string)
        if parsed is None:
            raise ValueError(f"Cannot parse color string: {color_string}")

        color = cls.__new__(cls)
        color.stroke, color.fill = parsed
        return color

    @classmethod
    def get_random_color(cls):
        """
        Get a random XO color.

        Returns:
            XoColor: Random XoColor instance from the standard palette
        """
        n = int(random.random() * len(colors))
        color = cls.__new__(cls)
        color.stroke, color.fill = colors[n]
        return color

    def to_rgba_tuple(self, alpha=1.0):
        """
        Convert colors to RGBA tuples for use with Cairo/GTK4.

        Args:
            alpha (float): Alpha value (0.0 - 1.0)

        Returns:
            tuple: ((r, g, b, a), (r, g, b, a)) for stroke and fill colors
        """

        def hex_to_rgba(hex_color):
            hex_color = hex_color.lstrip("#")
            r = int(hex_color[0:2], 16) / 255.0
            g = int(hex_color[2:4], 16) / 255.0
            b = int(hex_color[4:6], 16) / 255.0
            return (r, g, b, alpha)

        return (hex_to_rgba(self.stroke), hex_to_rgba(self.fill))


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # color file generator (for development)
        import re

        with open(sys.argv[1], "r") as f:
            print("colors = [")
            for line in f.readlines():
                match = re.match(r"fill: ([A-Z0-9]*) stroke: ([A-Z0-9]*)", line)
                if match:
                    print(f"['{match.group(2)}', '{match.group(1)}'],")
            print("]")
    else:
        print("Testing XoColor...")

        # random color
        color1 = XoColor()
        print(f"Random color: {color1}")

        # string parsing
        color2 = XoColor("#FF0000,#00FF00")
        print(f"Parsed color: {color2}")

        # equality
        color3 = XoColor("#FF0000,#00FF00")
        print(f"Colors equal: {color2 == color3}")

        # RGBA conversion
        rgba = color2.to_rgba_tuple()
        print(f"RGBA tuples: {rgba}")

        print("XoColor tests completed!")
