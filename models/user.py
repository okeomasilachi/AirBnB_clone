#!/usr/bin/python3

""" This module contains the User class That represents a user"""

from models.base_model import BaseModel
import datetime
from models import storage


class User(BaseModel):
    """A class representing a user.

    This class inherits from BaseModel and extends it to represent specific
    attributes of a user, such as email, password, first name, and last name.

    Attributes:
        email (str): The email address of the user.
        password (str): The password associated with the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.

    Methods:
        __init__(*args, **kwargs): Initializes a User instance.
        __str__(): Returns the string representation of a User instance.
        save(): Updates the 'updated_at' attribute and
            saves the instance to storage.
        to_dict(): Returns a dictionary representation of a User instance.
    """

    email = ""
    password = ""
    first_name = ""
    last_name = ""

    def __init__(self, *args, **kwargs):
        """Initializes a User instance.

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
        """Returns a dictionary representation of a User instance."""
        now = self.__dict__
        now['__class__'] = self.__class__.__name__
        return now
