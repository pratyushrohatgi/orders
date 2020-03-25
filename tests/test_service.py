"""
<your resource name> API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from unittest import TestCase
from unittest.mock import MagicMock, patch
from flask_api import status  # HTTP Status Codes
from service.models import db
from service.service import app, init_db

######################################################################
#  T E S T   C A S E S
######################################################################
class TestYourResourceServer(TestCase):
    """ <your resource name> Server Tests """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        pass

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        pass

    def setUp(self):
        """ This runs before each test """
        self.app = app.test_client()


    def tearDown(self):
        """ This runs after each test """
        pass

######################################################################
#  P L A C E   T E S T   C A S E S   H E R E 
######################################################################

    def test_index(self):
        """ Test index call """
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        
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
