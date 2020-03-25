"""
Test cases for Orders Model

"""
import logging
import unittest
import os
from service.models import Orders, DataValidationError, db

######################################################################
#  Orders   M O D E L   T E S T   C A S E S
######################################################################
class TestOrders(unittest.TestCase):
    """ Test Cases for Orders Model """

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
        pass

    def tearDown(self):
        """ This runs after each test """
        pass

######################################################################
#  P L A C E   T E S T   C A S E S   H E R E 
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

    def test_XXXX(self):
        """ Test something """
        self.assertTrue(True)
