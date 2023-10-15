#!/usr/bin/python3

""" This module contains the BaseModel class """

from models.base_model import BaseModel
import datetime
from models import storage


# The above class is a subclass of BaseModel and represents Amenity.
class Amenity(BaseModel):

    name = ""

    def __init__(self, *args, **kwargs):
        """
        initializes the attributes email, password, first_name,
        and last_name with empty strings.
        """
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    if key in ["created_at", "updated_at"]:
                        value = datetime.datetime.fromisoformat(value)
                    setattr(self, key, value)
        else:
            super().__init__()

    def __str__(self):
        """ Returns the string representation of an object of the class """
        return f"[{__class__.__name__}] ({self.id}) ({self.__dict__})"

    def save(self):
        self.updated_at = datetime.datetime.now()
        now = self.__dict__
        now['__class__'] = self.__class__.__name__
        now['updated_at'] = self.updated_at.isoformat()
        now['created_at'] = self.created_at.isoformat()
        update_instance = eval(self.__class__.__name__)(**now)
        storage.new(update_instance)
        storage.save()

    def to_dict(self):
        now = self.__dict__
        now['__class__'] = self.__class__.__name__
        return now
