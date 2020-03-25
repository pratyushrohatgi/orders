"""
Test cases for Order Model
"""
import logging
import unittest
import os
from service import app
from service.models import Order, Product, DataValidationError, db
from tests.factories import OrderFactory, ProductFactory
 
DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres"
)
 
######################################################################
#  Order   M O D E L   T E S T   C A S E S
######################################################################
class TestOrder(unittest.TestCase):
	""" Test Cases for Order Model """
 
	@classmethod
	def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
    	Order.init_db(app)
 
	@classmethod
	def tearDownClass(cls):
        """ This runs once after the entire test suite """
    	pass
 
	def setUp(self):
        """ This runs before each test """
        db.drop_all()  # clean up the last tests
        db.create_all()  # make our sqlalchemy tables
 
	def tearDown(self):
        """ This runs after each test """
        db.session.remove()
    	db.drop_all()
 
######################################################################
#  H E L P E R   M E T H O D S
######################################################################
 
	def _create_order(self, products=[]):
        """ Creates an order from a Factory """
    	fake_order = OrderFactory()
    	order = Order(
        	name=fake_order.name,
     	   status=fake_order.status,
        	products=products
    	)
        self.assertTrue(order != None)
        self.assertEqual(order.id, None)
    	return order

######################################################################
#  T E S T   C A S E S
######################################################################
 
	def test_create_an_order(self):
        """ Create a Order and assert that it exists """
    	fake_order = OrderFactory()
    	order = Order(
        	name=fake_order.name,
        	status=fake_order.status
    	)
        self.assertTrue(order != None)
        self.assertEqual(order.id, None)
        self.assertEqual(order.name, fake_order.name)
        self.assertEqual(order.status, fake_order.status)
 
	def test_add_a_order(self):
        """ Create an order and add it to the database """
    	orders = Order.all()
        self.assertEqual(orders, [])
    	order = self._create_order()
    	order.create()
    	# Assert that it was assigned an id and shows up in the database
        self.assertEqual(order.id, 1)
    	orders = Order.all()
        self.assertEqual(len(orders), 1)
 
 
	def test_update_order(self):
        """ Update an order """
    	order = self._create_order()
    	order.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertEqual(order.id, 1)
 
    	# Fetch it back
    	order = Order.find(order.id)
    	order.status = "XXX@YYY.COM"
    	order.save()
 
    	# Fetch it back again
    	order = Order.find(order.id)
        self.assertEqual(order.status, "Cancelled")
 
 
