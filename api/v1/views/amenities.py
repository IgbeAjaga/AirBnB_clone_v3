#!/usr/bin/python3
"""
New view for Amenity objects.
"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity

@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """
    Retrieves the list of all Amenity objects.

    Returns:
        JSON: A JSON response containing a list of Amenity objects.
    """
    amenities = [amenity.to_dict() for amenity in storage.all(Amenity).values()]
    return jsonify(amenities)

@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """
    Retrieves an Amenity object by ID.

    Args:
        amenity_id (str): The ID of the Amenity object to retrieve.

    Returns:
        JSON: A JSON response containing the Amenity object.
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())

@app_views.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """
    Deletes an Amenity object by ID.

    Args:
        amenity_id (str): The ID of the Amenity object to delete.

    Returns:
        JSON: An empty JSON response.
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({})

@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """
    Creates a new Amenity object.

    Returns:
        JSON: A JSON response containing the newly created Amenity object.
    """
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    if "name" not in data:
        abort(400, description="Missing name")
    new_amenity = Amenity(**data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201

@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """
    Updates an Amenity object by ID.

    Args:
        amenity_id (str): The ID of the Amenity object to update.

    Returns:
        JSON: A JSON response containing the updated Amenity object.
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
