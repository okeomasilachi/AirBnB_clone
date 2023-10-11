#!/usr/bin/python3

""" This module contains the BaseModel class """

from models.base_model import BaseModel
import datetime
from models import storage


class Review(BaseModel):

    def __init__(self):
        self.place_id = ""
        self.user_id = ""
        self.text = ""
        super().__init__()

    def __str__(self):
        """ Returns the string representation of an object of the class """
        return f"[{__class__.__name__}] ({self.id}) ({self.__dict__})"

    def save(self):
        """
        Updates the public instance attribute updated_at
        with the current datetime
        """
        self.updated_at = datetime.datetime.now()
        storage.save()

    def to_dict(self):
        """
        returns a dictionary containing key/values of
        __dict__ of the instance
        """
        return {
                "__class__": __class__.__name__,
                "updated_at": self.updated_at.isoformat(),
                "created_at": self.created_at.isoformat(),
                "id": self.id,
                "place_id": self.place_id,
                "user_id": self.user_id,
                "text": self.text
                }
