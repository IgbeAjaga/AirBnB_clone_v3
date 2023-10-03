#!/usr/bin/python3
"""
New view for State objects.
"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """
    Retrieves the list of all State objects.

    Returns:
        JSON: A JSON response containing a list of State objects.
    """
    states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(states)

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """
    Retrieves a State object by ID.

    Args:
        state_id (str): The ID of the State object to retrieve.

    Returns:
        JSON: A JSON response containing the State object.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """
    Deletes a State object by ID.

    Args:
        state_id (str): The ID of the State object to delete.

    Returns:
        JSON: An empty JSON response.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({})

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """
    Creates a new State.

    Returns:
        JSON: A JSON response containing the newly created State object.
    """
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    if "name" not in data:
        abort(400, description="Missing name")
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """
    Updates a State object by ID.

    Args:
        state_id (str): The ID of the State object to update.

    Returns:
        JSON: A JSON response containing the updated State object.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
