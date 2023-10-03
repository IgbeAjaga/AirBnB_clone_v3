#!/usr/bin/python3
"""
Creates a Blueprint instance with `url_prefix` set to `/api/v1`.
"""


from flask import Blueprint

# Create a Blueprint instance for the views in this package
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Import the view modules to make them accessible when this package is imported
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
from api.v1.views.places_amenities import *

# You can add more imports for other views as needed

# Import the views to register them with the Blueprint
from api.v1.views import (states, cities, amenities, users, places,
                         places_reviews, places_amenities)

