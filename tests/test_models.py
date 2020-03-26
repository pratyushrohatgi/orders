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
		order.status = "Cancelled"
		order.save()
		# Fetch it back again
		order = Order.find(order.id)
		self.assertEqual(order.status, "Cancelled")

		
	def test_delete_an_order(self):
		""" Delete an order from the database """
		orders = Order.all()
		self.assertEqual(orders, [])
		order = self._create_order()
		order.create()
		# Assert that it was assigned an id and shows up in the database
		self.assertEqual(order.id, 1)
		orders = Order.all()
		self.assertEqual(len(orders), 1)
		order = orders[0]
		order.delete()
		orders = Order.all()
		self.assertEqual(len(orders), 0)
 
	def test_find_or_404(self):
		""" Find or throw 404 error """
		order = self._create_order()
		order.create()
		# Assert that it was assigned an id and shows up in the database
		self.assertEqual(order.id, 1)
 
		# Fetch it back
		order = Order.find_or_404(order.id)
		self.assertEqual(order.id, 1)
 
	def test_find_by_name(self):
		""" Find by name """
		order = self._create_order()
		order.create()
 
		# Fetch it back by name
		same_order = Order.find_by_name(order.name)[0]
		self.assertEqual(same_order.id, order.id)
		self.assertEqual(same_order.name, order.name)
 
	def test_serialize_an_order(self):
		""" Serialize an order """
		product = self._create_product()
		order = self._create_order(products=[product])
		serial_order = order.serialize()
		self.assertEqual(serial_order['id'], order.id)
		self.assertEqual(serial_order['name'], order.name)
		self.assertEqual(serial_order['status'], order.status)
		self.assertEqual(len(serial_order['products']), 1)
		products = serial_order['products']
		self.assertEqual(products[0]['id'], product.id)
		self.assertEqual(products[0]['order_id'], product.order_id)
		self.assertEqual(products[0]['product_name'], product.product_name)
		self.assertEqual(products[0]['quantity'], product.quantity)
		self.assertEqual(products[0]['price'], product.price)
 
	def test_deserialize_an_order(self):
		""" Deserialize an order """
		product = self._create_product()
		order = self._create_order(products=[product])
		serial_order = order.serialize()
		new_order = Order()
		new_order.deserialize(serial_order)
		self.assertEqual(new_order.id, order.id)
		self.assertEqual(new_order.name, order.name)
		self.assertEqual(new_order.status, order.status)
 
	def test_deserialize_with_key_error(self):
		""" Deserialize an order with a KeyError """
		order = Order()
		self.assertRaises(DataValidationError, order.deserialize, {})
 
	def test_deserialize_with_type_error(self):
		""" Deserialize an order with a TypeError """
		order = Order()
		self.assertRaises(DataValidationError, order.deserialize, [])
 
	def test_deserialize_product_key_error(self):
		""" Deserialize an product with a KeyError """
		product = Product()
		self.assertRaises(DataValidationError, product.deserialize, {})
 
	def test_deserialize_product_type_error(self):
		""" Deserialize an product with a TypeError """
		product = Product()
		self.assertRaises(DataValidationError, product.deserialize, [])
 
	def test_add_order_product(self):
		""" Create an order with an product and add it to the database """
		orders = Order.all()
		self.assertEqual(orders, [])
		order = self._create_order()
		product = self._create_product()
		order.products.append(product)
		order.create()
		# Assert that it was assigned an id and shows up in the database
		self.assertEqual(order.id, 1)
		orders = Order.all()
		self.assertEqual(len(orders), 1)
 
		new_order = Order.find(order.id)
		self.assertEqual(order.products[0].product_name, product.product_name)
 
		product2 = self._create_product()
		order.products.append(product2)
		order.save()
 
		new_order = Order.find(order.id)
		self.assertEqual(len(order.products), 2)
		self.assertEqual(order.products[1].name, product2.product_name)
 
	def test_update_order_product(self):
		"""" Update an orders product """
		orders = Order.all()
		self.assertEqual(orders, [])

		product = self._create_product()
		order = self._create_order(products=[product])
		order.create()
		# Assert that it was assigned an id and shows up in the database
		self.assertEqual(order.id, 1)
		orders = Order.all()
		self.assertEqual(len(orders), 1)

		# Fetch it back
		order = Order.find(order.id)
		old_product = order.products[0]
		self.assertEqual(old_product.price, product.price)

		old_product.price = "XX"
		order.save()

		# Fetch it back again
		order = Order.find(order.id)
		product = order.products[0]
		self.assertEqual(product.price, "XX")

	def test_delete_order_product(self):
		""" Delete an orders product """
		orders = Order.all()
		self.assertEqual(orders, [])

		product = self._create_product()
		order = self._create_order(products=[product])
		order.create()
		# Assert that it was assigned an id and shows up in the database
		self.assertEqual(order.id, 1)
		orders = Order.all()
		self.assertEqual(len(orders), 1)

		# Fetch it back
		order = Order.find(order.id)
		product = order.products[0]
		product.delete()
		order.save()

		# Fetch it back again
		order = Order.find(order.id)
		self.assertEqual(len(order.products), 0)
