#!/usr/bin/python3

""" This module contains the BaseModel class """

from models.base_model import BaseModel
import datetime
from models import storage


class Place(BaseModel):

    def __init__(self):
        self.city_id = ""
        self.user_id = ""
        self.name = ""
        self.description = ""
        self.number_rooms = 0
        self.number_bathrooms = 0
        self.max_guest = 0
        self.price_by_night = 0
        self.latitude = 0.0
        self.longitude = 0.0
        self.amenity_ids = []
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
                "city_id": self.city_id,
                "user_id": self.user_id,
                "name": self.name,
                "description": self.description,
                "number_rooms": self.number_rooms,
                "number_bathrooms": self.number_bathrooms,
                "max_guest": self.max_guest,
                "price_by_night": self.price_by_night,
                "latitude": self.latitude,
                "longitude": self.longitude,
                "amenity_ids": self.amenity_ids
                }
