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
# UPDATE AN EXISTING ORDER
######################################################################
@app.route("/orders/<int:order_id>", methods=["PUT"])
def update_orders(order_id):
	"""
	Update an Order
	This endpoint will update an Order based the body that is posted
	"""
    app.logger.info("Request to update order with id: %s", order_id)
    check_content_type("application/json")
	order = Order.find(order_id)
	if not order:
    	raise NotFound("Order with id '{}' was not found.".format(order_id))
	order.deserialize(request.get_json())
	order.id = order_id
	order.save()
	return make_response(jsonify(order.serialize()), status.HTTP_200_OK)

