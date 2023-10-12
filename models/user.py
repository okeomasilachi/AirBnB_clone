from models.base_model import BaseModel
import datetime
from models import storage


# The above class is a subclass of BaseModel and represents a user.
class User(BaseModel):

    def __init__(self):
        """
        initializes the attributes email, password, first_name,
        and last_name with empty strings.
        """
        self.email = ""
        self.password = ""
        self.first_name = ""
        self.last_name = ""
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
                "email": self.email,
                "password": self.password,
                "first_name": self.first_name,
                "last_name": self.last_name
                }
