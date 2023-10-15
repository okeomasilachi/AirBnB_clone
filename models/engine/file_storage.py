#!/usr/bin/python3

""" This module contains the FileStorage class """


import json
import os
from json import JSONEncoder
import datetime


class DateTimeEncoder(JSONEncoder):
    """Encodes datetime objects into JSON format.

    This class extends the JSONEncoder class to provide custom encoding for
    datetime objects. It overrides the default behavior to format datetime
    objects as ISO 8601 strings.

    Methods:
        default(obj): Encodes an object into a JSON-compatible format.
    """

    def default(self, obj):
        """Encodes an object into a JSON-compatible format.

        Args:
            obj: The object to be encoded.

        Returns:
            str: The encoded representation of the object.

        If the object is an instance of datetime.datetime, it is formatted
        as an ISO 8601 string using obj.isoformat(). Otherwise, the default
        behavior of JSONEncoder is used.
        """
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super().default(obj)


class FileStorage:
    """
    The FileStorage class is used for storing and managing files.
    """

    __file_path = "models/engine/instances.json"
    __objects = {}

    def all(self):
        """
        Returns all objects stored in a FileStorage object.

        Returns:
            dict: A dictionary containing all stored objects.
        """
        return FileStorage.__objects

    def new(self, obj):
        """
        Adds an object to a dictionary with a key generated
        from the object's class name and id.

        Args:
          obj: Object to be added to the storage.
            It should have "__class__" and "id" attributes.
        """
        key = f"{obj.__class__.__name__}.{obj.id}"
        FileStorage.__objects[key] = obj.to_dict()

    def save(self):
        """
        Saves the contents of the `__objects` dictionary to a file
        in JSON format.
        """
        with open(FileStorage.__file_path, "w", encoding="utf-8") as file:
            json.dump(FileStorage.__objects, file, cls=DateTimeEncoder)

    def reload(self):
        """
        Reads data from a file and loads it into the `FileStorage` object.
        """
        file_path = FileStorage.__file_path
        try:
            if os.path.exists(file_path):
                file = FileStorage.__file_path
                with open(f"{file}", "r", encoding="utf-8") as file:
                    data = file.read()
                    FileStorage.__objects = json.loads(data)
                file.close()
            else:
                FileStorage.__objects = {}
        except Exception:
            pass
