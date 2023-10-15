#!/usr/bin/python3

""" This module contains the BaseModel class """

import uuid
import datetime
from models import storage  # importing the storage variable from __init__


class BaseModel:
    """ This represents the BaseModel class """
    def __init__(self, *args, **kwargs):
        """
        The function initializes an object with optional keyword arguments,
        setting attributes based on the provided values or generating default
        values if not provided.
        """
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    if key in ["created_at", "updated_at"]:
                        value = datetime.datetime.fromisoformat(value)
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.datetime.now()
            self.updated_at = self.created_at
            storage.new(self)

    def __str__(self):
        """ Returns the string representation of an object of the class """
        return f"[{__class__.__name__}] ({self.id}) ({self.__dict__})"

    def save(self):
        """
        Updates the public instance attribute updated_at
        with the current datetime
        """
        self.updated_at = datetime.datetime.now()
        now = self.__dict__
        now['__class__'] = self.__class__.__name__
        now['updated_at'] = str(self.updated_at.isoformat())
        now['created_at'] = str(self.created_at.isoformat())
        new_instance = eval(self.__class__.__name__)(**now)
        storage.new(new_instance)
        storage.save()

    def to_dict(self):
        """
        returns a dictionary containing key/values of
        __dict__ of the instance
        """
        now = self.__dict__
        now['__class__'] = self.__class__.__name__
        return now
