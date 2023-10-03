#!/usr/bin/python3
"""
API status and statistics.
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def api_status():
    """
    Return the status of your API.

    This endpoint returns a JSON response indicating that the API
    """
    return jsonify({"status": "OK"})

@app_views.route('/api/v1/stats', methods=['GET'], strict_slashes=False)
def api_stats():
    """
    Retrieve the number of each object by type.

    This endpoint retrieves and returns the count of each object type
    (e.g., amenities, cities, places) in the storage.
    """
    classes = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User),
    }
    return jsonify(classes)
