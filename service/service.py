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
	)
 
 
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
    Order.init_db(app)

######################################################################
# LIST ALL Orders
######################################################################
@app.route("/orders", methods=["GET"])
def list_orders():
	""" Returns all of the Orders """
	app.logger.info("Request for Order list")
	orders = []
	name = request.args.get("name")
	if name:
		orders = Order.find_by_name(name)
	else:
		orders = Order.all()

	results = [order.serialize() for order in orders]
	return make_response(jsonify(results), status.HTTP_200_OK)
 
######################################################################
# RETRIEVE AN ORDER
######################################################################
@app.route("/orders/<int:order_id>", methods=["GET"])
def get_orders(order_id):
	"""
	Retrieve a single Order
	This endpoint will return an Order based on it's id
	"""
	app.logger.info("Request for Order with id: %s", order_id)
	order = Order.find_or_404(order_id)
	return make_response(jsonify(order.serialize()), status.HTTP_200_OK)


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
@app.route("/orders/<int:order_id>", methods=["DELETE"])
def delete_orders(order_id):
	"""
	Delete an Order
	This endpoint will delete an Order based the id specified in the path
	"""
	app.logger.info("Request to delete order with id: %s", order_id)
	order = Order.find(order_id)
	if order:
		order.delete()
	return make_response("", status.HTTP_204_NO_CONTENT)
 
 
#---------------------------------------------------------------------
#            	P R O D U C T    M E T H O D S
#---------------------------------------------------------------------
 
 
######################################################################
# LIST PRODUCTS
######################################################################
@app.route("/orders/<int:order_id>/products", methods=["GET"])
def list_products(order_id):
	""" Returns all of the Products for an Order """
	app.logger.info("Request for Order Products...")
	order = Order.find_or_404(order_id)
	results = [product.serialize() for product in order.products]
	return make_response(jsonify(results), status.HTTP_200_OK)
 
######################################################################
# ADD AN PRODUCT TO AN ORDER
######################################################################
@app.route('/orders/<int:order_id>/products', methods=['POST'])
def create_products(order_id):
	"""
	Create an Product on an Order
	This endpoint will add an product to an order
	"""
	app.logger.info("Request to add an product to an order")
	check_content_type("application/json")
	order = Order.find_or_404(order_id)
	product = Product()
	product.deserialize(request.get_json())
	order.products.append(product)
	order.save()
	message = product.serialize()
	return make_response(jsonify(message), status.HTTP_201_CREATED)
 
######################################################################
# RETRIEVE AN Product FROM ORDER
######################################################################
@app.route('/orders/<int:order_id>/products/<int:product_id>', methods=['GET'])
def get_products(order_id, product_id):
	"""
	Get an Product
	This endpoint returns just an product
	"""
	app.logger.info("Request to get an product with id: %s", product_id)
	product = Product.find_or_404(product_id)
	return make_response(jsonify(product.serialize()), status.HTTP_200_OK)
 
######################################################################
# UPDATE AN Product
######################################################################
@app.route("/orders/<int:order_id>/products/<int:product_id>", methods=["PUT"])
def update_products(order_id, product_id):
	"""
	Update an Product
	This endpoint will update an Product based the body that is posted
	"""
	app.logger.info("Request to update product with id: %s", product_id)
	check_content_type("application/json")
	product = Product.find_or_404(product_id)
	product.deserialize(request.get_json())
	product.id = product_id
	product.save()
	return make_response(jsonify(product.serialize()), status.HTTP_200_OK)
 
######################################################################
# DELETE AN PRODUCT
######################################################################
@app.route("/orders/<int:order_id>/products/<int:product_id>", methods=["DELETE"])
def delete_products(order_id, product_id):
	"""
	Delete an Product
	This endpoint will delete an Product based the id specified in the path
	"""
	app.logger.info("Request to delete order with id: %s", order_id)
	product = Product.find(product_id)
	if product:
		product.delete()
	return make_response("", status.HTTP_204_NO_CONTENT)
 
 
 
######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################
 
def init_db():
	""" Initialies the SQLAlchemy app """
	global app
	Order.init_db(app)
 
def check_content_type(content_type):
	""" Checks that the media type is correct """
	if request.headers["Content-Type"] == content_type:
		return
	app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
	abort(415, "Content-Type must be {}".format(content_type))
