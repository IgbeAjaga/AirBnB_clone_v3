#!/usr/bin/python3
"""
Contains the FileStorage class
"""

import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import hashlib  # Added hashlib for password hashing

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class FileStorage:
    """
    Serializes instances to a JSON file & deserializes back to instances.

    This class provides methods to serialize Python objects (instances of classes)
    to a JSON file and to deserialize JSON data from the file back into Python objects.
    """

    # string - path to the JSON file
    __file_path = "file.json"
    # dictionary - empty but will store all objects by <class name>.id
    __objects = {}

    def all(self, cls=None):
        """
        Returns a dictionary of all objects or objects of a specific class.

        Args:
            cls (class, optional): The class of objects to filter by.
                If None, returns all objects.

        Returns:
            dict: A dictionary where keys are in the format 'ClassName.id'
                and values are the objects themselves.
        """
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict
        return self.__objects

    def new(self, obj):
        """
        Adds the object to the dictionary of objects.

        Args:
            obj: The object to be added to the dictionary.
        """
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)."""
        new_dict = {}
        for key, value in self.__objects.items():
            new_dict[key] = value.to_dict()
            if isinstance(value, User) and hasattr(value, 'password') and value.password:
                new_dict[key]['password'] = hashlib.md5(value.password.encode()).hexdigest()

    def reload(self):
        """Deserializes the JSON file to __objects."""
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)
            for key in jo:
                self.__objects[key] = classes[jo[key]["__class__"]](**jo[key])
        except:
            pass

    def delete(self, obj=None):
        """
        Deletes an object from __objects if it's inside.

        Args:
            obj (object, optional): The object to be deleted from the dictionary.
        """
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """Calls reload() method for deserializing the JSON file to objects."""
        self.reload()

    def get(self, cls, id):
        """
        Retrieves one object by its class and ID.

        Args:
            cls (class): The class of the object to retrieve.
            id (str): The ID of the object to retrieve.

        Returns:
            object: The retrieved object, or None if not found.
        """
        if cls and id:
            takeObj = '{}.{}'.format(cls, id)
            everyObj = self.all(cls)
            return everyObj.get(takeObj)
        else:
            return None

    def count(self, cls=None):
        """
        Counts the number of objects in the storage.

        Args:
            cls (class, optional): The class of objects to count.
                If None, counts all classes.

        Returns:
            int: The number of objects in storage.
        """
        return len(self.all(cls))
