# Copyright (C) 2006-2007 Red Hat, Inc.
# Copyright (C) 2025 MostlyK
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

"""
Provides a class for storing activity metadata such as activity id's,
journal object id's.
The ActivityHandle class for managing activity instances and their metadata.
"""

import uuid


class ActivityHandle(object):
    """
    Data structure storing simple activity metadata

    Args:
        activity_id (string): unique id for the activity to be
        created

        object_id (string): identity of the journal object
        associated with the activity.

        When you resume an activity from the journal
        the object_id will be passed in. It is optional
        since new activities does not have an
        associated object.

        uri (string): URI associated with the activity. Used when
        opening an external file or resource in the
        activity, rather than a journal object
        (downloads stored on the file system for
        example or web pages)

        invited (bool): True if the activity is being
        launched for handling an invite from the network
    """

    def __init__(self, activity_id=None, object_id=None, uri=None, invited=False):
        if activity_id is None:
            activity_id = self._create_activity_id()

        self.activity_id = activity_id
        self.object_id = object_id
        self.uri = uri
        self.invited = invited

    def _create_activity_id(self):
        """
        Generate a new unique activity ID.
        """
        # Simple UUID-based ID generation
        return str(uuid.uuid4())

    def get_dict(self):
        """
        Get a dictionary representation of the handle.
        Returns:
            dict: Dictionary containing handle data
        """
        result = {
            'activity_id': self.activity_id,
            'invited': self.invited
        }

        if self.object_id is not None:
            result['object_id'] = self.object_id

        if self.uri is not None:
            result['uri'] = self.uri

        return result

    @classmethod
    def create_from_dict(cls, handle_dict):
        """
        Create an ActivityHandle from a dictionary.
        Args:
            handle_dict (dict): Dictionary containing handle data

        Returns:
            ActivityHandle: New handle instance
        """
        return cls(
            activity_id=handle_dict.get('activity_id'),
            object_id=handle_dict.get('object_id'),
            uri=handle_dict.get('uri'),
            invited=handle_dict.get('invited', False)
        )

    def __repr__(self):
        """String representation of the handle."""
        return f"ActivityHandle(activity_id='{self.activity_id}', " \
               f"object_id='{self.object_id}', uri='{self.uri}', " \
               f"invited={self.invited})"
