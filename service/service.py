"""
My Service

Describe what your service does here
"""

import os
import sys
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from flask_api import status  # HTTP Status Codes

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy
from service.models import Orders, DataValidationError

# Import Flask application
from . import app

######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    return "Reminder: return some useful information in json format about the service here", status.HTTP_200_OK


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

def init_db():
    """ Initialies the SQLAlchemy app """
    global app
    Orders.init_db(app)

    
######################################################################
# CREATE A NEW ORDER
######################################################################
@app.route("/orders", methods=["POST"])
def create_orders():
	"""
	Creates an Order
    This endpoint will create an Order based the data in the body that is posted
	"""
    app.logger.info("Request to create an Order")
    check_content_type("application/json")
	order = Order()
	order.deserialize(request.get_json())
	order.create()
	message = order.serialize()
	location_url = url_for("get_orders", order_id=order.id, _external=True)
	return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
	)
