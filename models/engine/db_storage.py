#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import models
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import hashlib  # Added hashlib for password hashing

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class DBStorage:
    """
    Interacts with the MySQL database.

    This class provides methods to interact with a MySQL database
    to store and retrieve objects from the database.
    """

    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(HBNB_MYSQL_USER,
                                             HBNB_MYSQL_PWD,
                                             HBNB_MYSQL_HOST,
                                             HBNB_MYSQL_DB))
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Query objects from the current database session.

        Args:
            cls (class, optional): The class of objects to query.
                If None, queries all classes.

        Returns:
            dict: A dictionary of objects, where the keys are in the
                format 'ClassName.id' and the values are the objects themselves.
        """
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return new_dict

    def new(self, obj):
        """
        Add the object to the current database session.

        Args:
            obj: The object to be added to the database.
        """
        if obj:
            if hasattr(obj, 'password') and obj.password:
                obj.password = hashlib.md5(obj.password.encode()).hexdigest()
            self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """
        Delete an object from the current database session.

        Args:
            obj (object, optional): The object to be deleted from the database.
        """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Reload data from the database."""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def get(self, cls, id):
    """
    Retrieve one object.

    Args:
        cls (class): The class of the object to retrieve.
        id (str): The ID of the object to retrieve.

    Returns:
        object: The object if found, None otherwise.
    """
    if cls and id:
        key = "{}.{}".format(cls.__name__, id)
        all_objects = self.all(cls)
        return all_objects.get(key)
    else:
        return None

    def count(self, cls=None):
    """
    Count the number of objects in storage.

    Args:
        cls (class, optional): The class to count objects for. If not provided, count all objects.

    Returns:
        int: The number of objects of the specified class or all objects.
    """
    if cls:
        return len(self.all(cls))
    else:
        return len(self.all())

    def close(self):
        """Call remove() method on the private session attribute."""
        self.__session.remove()
