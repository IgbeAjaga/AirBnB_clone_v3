#!/usr/bin/python3
"""
Unit tests for the FileStorage class.
"""

import unittest
import os
import json
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.user import User
from models.state import State

class TestFileStorage(unittest.TestCase):
    """
    Test cases for the FileStorage class.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the test environment and create a test FileStorage instance.
        """
        cls.storage = FileStorage()
        cls.storage.reload()

    @classmethod
    def tearDownClass(cls):
        """
        Clean up and remove the test JSON file.
        """
        if os.path.exists('file.json'):
            os.remove('file.json')

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
        with open('file.json', 'r') as file:
            data = json.load(file)
            self.assertIsNotNone(data.get(key))

    def test_reload(self):
        """
        Test the reload method.
        """
        user = User(email="test@example.com", password="testpassword")
        self.storage.new(user)
        self.storage.save()
        self.storage.reload()
        key = "User." + user.id
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
