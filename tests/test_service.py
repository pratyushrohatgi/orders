"""
Orders API Service Test Suite
Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from unittest import TestCase
from unittest.mock import MagicMock, patch
from flask_api import status  # HTTP Status Codes
from tests.factories import OrderFactory, ProductFactory
from service.models import db
from service.service import app, init_db
 
# DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///../db/test.db')
DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres"
)
 
######################################################################
#  T E S T   C A S E S
######################################################################
class TestYourResourceServer(TestCase):
    """ Orders Server Tests """
 
	@classmethod
	def setUpClass(cls):
        """ Run once before all tests """
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
    	init_db()
 
	@classmethod
	def tearDownClass(cls):
        """ Runs once before test suite """
    	pass
 
	def setUp(self):
  	  """ Runs before each test """
        db.drop_all()  # clean up the last tests
        db.create_all()  # create new tables
    	self.app = app.test_client()
 
	def tearDown(self):
        """ Runs once after each test case """
    	db.session.remove()
    	db.drop_all()
 
######################################################################
#  H E L P E R   M E T H O D S
######################################################################
 
	def _create_orders(self, count):
        """ Factory method to create orders in bulk """
    	orders = []
    	for _ in range(count):
        	order = OrderFactory()
        	resp = self.app.post(
                "/orders", json=order.serialize(), content_type="application/json"
        	)
            self.assertEqual(
                resp.status_code, status.HTTP_201_CREATED, "Could not create test Order"
        	)
        	new_order = resp.get_json()
        	order.id = new_order["id"]
        	orders.append(order)
    	return orders
 
######################################################################
#  O R D E R   T E S T   C A S E S
######################################################################

	def test_update_order(self):
        """ Update an existing Order """
    	# create an Order to update
    	test_order = OrderFactory()
    	resp = self.app.post(
        	"/orders",
        	json=test_order.serialize(),
            content_type="application/json"
    	)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
 
    	# update the pet
    	new_order = resp.get_json()
    	new_order["name"] = "Happy-Happy Joy-Joy"
    	resp = self.app.put(
        	"/orders/{}".format(new_order["id"]),
        	json=new_order,
            content_type="application/json",
    	)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
    	updated_order = resp.get_json()
        self.assertEqual(updated_order["name"], "Happy-Happy Joy-Joy")
 
	
######################################################################
#  P R O D U C T S   T E S T   C A S E S
######################################################################
 
