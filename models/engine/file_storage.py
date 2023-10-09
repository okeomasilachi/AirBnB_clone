#!/usr/bin/python3

""" This module contains the FileStorage class """


import json
import os


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
            file.write(json.dumps(FileStorage.__objects))
        file.close()

    def reload(self):
        """
        Reads data from a file and loads it into the `FileStorage` object.
        """
        file_path = FileStorage.__file_path
        if os.path.exists(file_path):
            with open(F"{FileStorage.__file_path}", "r", encoding="utf-8") as file:
                data = file.read()
                FileStorage.__objects = json.loads(data)
            file.close()
