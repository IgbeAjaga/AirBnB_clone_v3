#!/usr/bin/python3
"""
Unit tests for the DBStorage class.
"""

import unittest
import os
from models.engine.db_storage import DBStorage
from models.base_model import BaseModel
from models.user import User
from models.state import State

class TestDBStorage(unittest.TestCase):
    """
    Test cases for the DBStorage class.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up a test database for testing.
        """
        os.environ['HBNB_ENV'] = 'test'
        os.environ['HBNB_MYSQL_USER'] = 'your_test_db_user'
        os.environ['HBNB_MYSQL_PWD'] = 'your_test_db_password'
        os.environ['HBNB_MYSQL_HOST'] = 'localhost'
        os.environ['HBNB_MYSQL_DB'] = 'test_db_name'
        cls.storage = DBStorage()
        cls.storage.reload()

    @classmethod
    def tearDownClass(cls):
        """
        Remove the test database.
        """
        os.environ['HBNB_ENV'] = 'test'
        os.environ['HBNB_MYSQL_USER'] = 'your_test_db_user'
        os.environ['HBNB_MYSQL_PWD'] = 'your_test_db_password'
        os.environ['HBNB_MYSQL_HOST'] = 'localhost'
        os.environ['HBNB_MYSQL_DB'] = 'test_db_name'
        cls.storage.close()

    def test_all(self):
        """
        Test the all method.
        """
        all_objs = self.storage.all()
        self.assertTrue(isinstance(all_objs, dict))

    def test_new(self):
        """
        Test the new method.
        """
        user = User(email="test@example.com", password="testpassword")
        self.storage.new(user)
        key = "User." + user.id
        self.assertIsNotNone(self.storage.all().get(key))

    def test_save(self):
        """
        Test the save method.
        """
        user = User(email="test@example.com", password="testpassword")
        self.storage.new(user)
        self.storage.save()
        key = "User." + user.id
        self.assertTrue(os.path.exists('file.json'))
        self.assertIsNotNone(self.storage.all().get(key))

    def test_delete(self):
        """
        Test the delete method.
        """
        user = User(email="test@example.com", password="testpassword")
        self.storage.new(user)
        key = "User." + user.id
        self.assertIsNotNone(self.storage.all().get(key))
        self.storage.delete(user)
        self.assertIsNone(self.storage.all().get(key))

    def test_get(self):
        """
        Test the get method.
        """
        user = User(email="test@example.com", password="testpassword")
        self.storage.new(user)
        retrieved_user = self.storage.get(User, user.id)
        self.assertEqual(user, retrieved_user)

    def test_count(self):
        """
        Test the count method.
        """
        user = User(email="test@example.com", password="testpassword")
        self.storage.new(user)
        user_count = self.storage.count(User)
        self.assertEqual(user_count, 1)

if __name__ == '__main__':
    unittest.main()
