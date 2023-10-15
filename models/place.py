#!/usr/bin/python3

""" This module contains the Place class """

from models.base_model import BaseModel
import datetime
from models import storage


# The above class is a subclass of BaseModel and represents a Place.
class Place(BaseModel):
    """
    The Place class represents a specific lodging location.

    Attributes:
        city_id (str): The unique identifier of the associated city.
        user_id (str): The unique identifier of the associated user.
        name (str): The name of the place.
        description (str): A description of the place.
        number_rooms (int): The number of rooms in the place.
        number_bathrooms (int): The number of bathrooms in the place.
        max_guest (int): The maximum number of guests the
            place can accommodate.
        price_by_night (int): The nightly price for staying at the place.
        latitude (float): The latitude coordinates of the place.
        longitude (float): The longitude coordinates of the place.
        amenity_ids (list): A list of unique identifiers for
            associated amenities.

    Methods:
        __init__(*args, **kwargs): Initializes a Place instance.
        __str__(): Returns the string representation of a Place instance.
        save(): Updates the 'updated_at' attribute and
            saves the instance to storage.
        to_dict(): Returns a dictionary representation of a Place instance.
    """

    city_id = ""
    user_id = ""
    name = ""
    description = ""
    number_rooms = 0
    number_bathrooms = 0
    max_guest = 0
    price_by_night = 0
    latitude = 0.0
    longitude = 0.0
    amenity_ids = []

    def __init__(self, *args, **kwargs):
        """Initializes a Place instance.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        If keyword arguments are provided, attributes are set accordingly.
        If no arguments are provided, calls the superclass's __init__ method.

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
        """Updates the 'updated_at' attribute and saves
        the instance to storage.
        """
        self.updated_at = datetime.datetime.now()
        now = self.__dict__
        now['__class__'] = self.__class__.__name__
        now['updated_at'] = self.updated_at.isoformat()
        now['created_at'] = self.created_at.isoformat()
        update_instance = eval(self.__class__.__name__)(**now)
        storage.new(update_instance)
        storage.save()

    def to_dict(self):
        """Returns a dictionary representation of a Place instance."""
        now = self.__dict__
        now['__class__'] = self.__class__.__name__
        return now
