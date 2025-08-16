# Copyright (C) 2007, Red Hat, Inc.
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

"""Activity Bundle management"""

import os
import logging


class ActivityBundle:
    """Represents an activity bundle."""

    def __init__(self, path):
        self.path = path
        self._icon = None
        self._max_participants = 1

    def get_icon(self):
        """Get the activity icon name."""
        return self._icon or "activity-generic"

    def get_max_participants(self):
        """Get maximum participants for collaboration."""
        return self._max_participants


# Global bundle instance
_bundle_instance = None


def get_bundle_instance(bundle_path=None):
    """
    Get the global bundle instance.

    Args:
        bundle_path (str): Path to bundle directory

    Returns:
        ActivityBundle: Bundle instance
    """
    global _bundle_instance

    if _bundle_instance is None:
        if bundle_path is None:
            bundle_path = os.environ.get("SUGAR_BUNDLE_PATH", "/tmp")
        _bundle_instance = ActivityBundle(bundle_path)

    return _bundle_instance
