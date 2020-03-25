"""
Orders
Stores orders
"""
 
import os
import sys
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from flask_api import status  # HTTP Status Codes
from werkzeug.exceptions import NotFound
 
# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy
from service.models import Order, Product, DataValidationError
 
# Import Flask application
from . import app
 
######################################################################
# Error Handlers
######################################################################
@app.errorhandler(DataValidationError)
def request_validation_error(error):
	""" Handles Value Errors from bad data """
	return bad_request(error)
 
 
@app.errorhandler(status.HTTP_400_BAD_REQUEST)
def bad_request(error):
	""" Handles bad reuests with 400_BAD_REQUEST """
	message = str(error)
    app.logger.warning(message)
	return (
    	jsonify(
            status=status.HTTP_400_BAD_REQUEST, error="Bad Request", message=message
    	),
    	status.HTTP_400_BAD_REQUEST,
	)
 
 
@app.errorhandler(status.HTTP_404_NOT_FOUND)
def not_found(error):
	""" Handles resources not found with 404_NOT_FOUND """
	message = str(error)
    app.logger.warning(message)
	return (
        jsonify(status=status.HTTP_404_NOT_FOUND, error="Not Found", message=message),
        status.HTTP_404_NOT_FOUND,
	)
 
 
@app.errorhandler(status.HTTP_405_METHOD_NOT_ALLOWED)
def method_not_supported(error):
	""" Handles unsuppoted HTTP methods with 405_METHOD_NOT_SUPPORTED """
	message = str(error)
    app.logger.warning(message)
	return (
    	jsonify(
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
            error="Method not Allowed",
            message=message,
    	),
        status.HTTP_405_METHOD_NOT_ALLOWED,
	)
 
 
@app.errorhandler(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
def mediatype_not_supported(error):
	""" Handles unsuppoted media requests with 415_UNSUPPORTED_MEDIA_TYPE """
	message = str(error)
	app.logger.warning(message)
	return (
    	jsonify(
            status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            error="Unsupported media type",
            message=message,
    	),
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
	update)
 
 
@app.errorhandler(status.HTTP_500_INTERNAL_SERVER_ERROR)
def internal_server_error(error):
	""" Handles unexpected server error with 500_SERVER_ERROR """
	message = str(error)
    app.logger.error(message)
	return (
    	jsonify(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error="Internal Server Error",
            message=message,
    	),
        status.HTTP_500_INTERNAL_SERVER_ERROR,
	)
 
 
######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
	""" Root URL response """
	return (
    	jsonify(
            name="Order REST API Service",
            version="1.0",
            paths=url_for("list_orders", _external=True),
    	),
        status.HTTP_200_OK,
	)
 

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

def init_db():
    """ Initialies the SQLAlchemy app """
    global app
    Orders.init_db(app)

######################################################################
# LIST ALL Orders
######################################################################

######################################################################
# RETRIEVE AN ORDER
######################################################################


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

######################################################################
# DELETE AN ORDER
######################################################################


 
#---------------------------------------------------------------------
#            	P R O D U C T    M E T H O D S
#---------------------------------------------------------------------
 
 
######################################################################
# LIST PRODUCTS
######################################################################


######################################################################
# ADD AN PRODUCT TO AN ORDER
######################################################################


######################################################################
# RETRIEVE AN Product FROM ORDER
######################################################################


######################################################################
# UPDATE AN Product
######################################################################


######################################################################
# DELETE AN PRODUCT
######################################################################


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

