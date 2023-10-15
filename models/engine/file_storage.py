#!/usr/bin/python3

""" This module contains the FileStorage class """


import json
import os
from json import JSONEncoder
import datetime


class DateTimeEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super().default(obj)



class FileStorage:
    """
    The FileStorage class is used for storing and managing files.
    """

    __file_path = "instances.json"
    __objects = {}

    def all(self):
        """
        The function returns all objects stored in a FileStorage object.

        Returns:
            Attribute of the `FileStorage` class.
        """
        return FileStorage.__objects

    def new(self, obj):
        """
        The function adds an object to a dictionary with a key generated
        from the object's class name and id.

        Args:
          obj: Object that is being passed to the "new" method.
          It is expected to have a "__class__" attribute,
          which represents the class of the object, and an "id"
          attribute, which represents the unique identifier of the object.
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
        if os.path.exists(file_path):
            file = FileStorage.__file_path
            with open(f"{file}", "r", encoding="utf-8") as file:
                data = file.read()
                FileStorage.__objects = json.loads(data)
            file.close()
