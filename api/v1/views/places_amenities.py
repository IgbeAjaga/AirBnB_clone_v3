#!/usr/bin/python3
"""
New view for the link between Place objects and Amenity objects.
"""

from flask import jsonify, abort, request
from models.place import Place
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views

@app_views.route('/places/<place_id>/amenities', methods=['GET'], strict_slashes=False)
def get_place_amenities(place_id):
    """
    Get a list of Amenity objects linked to a Place.

    Args:
        place_id (str): The ID of the Place to retrieve linked Amenity objects from.

    Returns:
        JSON: A JSON response containing a list of linked Amenity objects.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenities = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenities)

@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """
    Delete an Amenity object from a Place.

    Args:
        place_id (str): The ID of the Place from which to remove the Amenity.
        amenity_id (str): The ID of the Amenity to be removed.

    Returns:
        JSON: An empty JSON response.
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if not place or not amenity:
        abort(404)

    if amenity not in place.amenities:
        abort(404)

    place.amenities.remove(amenity)
    storage.save()
    return jsonify({}), 200

@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'], strict_slashes=False)
def link_place_amenity(place_id, amenity_id):
    """
    Link an Amenity object to a Place.

    Args:
        place_id (str): The ID of the Place to which the Amenity will be linked.
        amenity_id (str): The ID of the Amenity to be linked.

    Returns:
        JSON: A JSON response containing the linked Amenity object.
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if not place or not amenity:
        abort(404)

    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200

    place.amenities.append(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201
