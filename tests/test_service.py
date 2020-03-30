"""
Orders API Service Test Suite
Test cases can be run with the following:
    nosetests -v --with-spec --spec-color
    coverage report -m
"""
import os
import logging
from unittest import TestCase
#from unittest.mock import MagicMock #, patch
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
        app.logger.setLevel(logging.CRITICAL) # pylint: disable=maybe-no-member
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
                "/orders", json=order.serialize(), content_type="application/json") # pylint: disable=maybe-no-member
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

    def test_index(self):
        """ Test index call """
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_get_order_list(self):
        """ Get a list of Orders """
        self._create_orders(5)
        resp = self.app.get("/orders")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 5)

    def test_get_order_by_name(self):
        """ Get a Order by Name """
        orders = self._create_orders(3)
        resp = self.app.get("/orders?name={}".format(orders[1].name))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data[0]["name"], orders[1].name)

    def test_get_order(self):
        """ Get a single Order """
        # get the id of an order
        order = self._create_orders(1)[0]
        resp = self.app.get(
            "/orders/{}".format(order.id),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], order.name)

    def test_get_order_not_found(self):
        """ Get an Order that is not found """
        resp = self.app.get("/orders/0")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_order(self):
        """ Create a new Order """
        order = OrderFactory()
        resp = self.app.post(
            "/orders", json=order.serialize(), content_type="application/json") # pylint: disable=maybe-no-member
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set
        location = resp.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_order = resp.get_json()
        self.assertEqual(new_order["name"], order.name, "Names does not match")
        self.assertEqual(new_order["products"], order.products, "Product does not match") # pylint: disable=maybe-no-member
        self.assertEqual(new_order["status"], order.status, "Status does not match")# pylint: disable=maybe-no-member

        # Check that the location header was correct by getting it
        resp = self.app.get(location, content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_order = resp.get_json()
        self.assertEqual(new_order["name"], order.name, "Names does not match")
        self.assertEqual(new_order["products"], order.products, "Product does not match") # pylint: disable=maybe-no-member
        self.assertEqual(new_order["status"], order.status, "Status does not match") # pylint: disable=maybe-no-member

    def test_update_order(self):
        """ Update an existing Order """
        # create an Order to update
        test_order = OrderFactory()
        resp = self.app.post(
            "/orders", json=test_order.serialize(), content_type="application/json") # pylint: disable=maybe-no-member
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # update the pet
        new_order = resp.get_json()
        new_order["name"] = "Happy-Happy Joy-Joy"
        resp = self.app.put(
            "/orders/{}".format(new_order["id"]), json=new_order,
            content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_order = resp.get_json()
        self.assertEqual(updated_order["name"], "Happy-Happy Joy-Joy")

    def test_delete_order(self):
        """ Delete an Order """
        # get the id of an order
        order = self._create_orders(1)[0]
        resp = self.app.delete(
            "/orders/{}".format(order.id),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_bad_request(self):
        """ Send wrong media type """
        #order = OrderFactory()
        resp = self.app.post(
            "/orders",
            json={"name": "not enough data"},
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unsupported_media_type(self):
        """ Send wrong media type """
        order = OrderFactory()
        resp = self.app.post("/orders", json=order.serialize(), content_type="test/html") # pylint: disable=maybe-no-member
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE) # pylint: disable=maybe-no-member

    def test_method_not_allowed(self):
        """ Make an illegal method call """
        resp = self.app.put(
            "/orders", json={"not": "today"}, content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

######################################################################
#  P R O D U C T S   T E S T   C A S E S
######################################################################

    def test_get_product_list(self):
        """ Get a list of Products """
        # add two products to order
        order = self._create_orders(1)[0]
        product_list = ProductFactory.create_batch(2)

        # Create product 1
        resp = self.app.post(
            "/orders/{}/products".format(order.id), json=product_list[0].serialize(),
            content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # Create product 2
        resp = self.app.post(
            "/orders/{}/products".format(order.id), json=product_list[1].serialize(),
            content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # get the list back and make sure there are 2
        resp = self.app.get("/orders/{}/products".format(order.id), content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = resp.get_json()
        self.assertEqual(len(data), 2)


    def test_add_product(self):
        """ Add a product to an order """
        order = self._create_orders(1)[0]
        product = ProductFactory()
        resp = self.app.post(
            "/orders/{}/products".format(order.id), json=product.serialize(), content_type="application/json") # pylint: disable=maybe-no-member
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED) # pylint: disable=maybe-no-member
        data = resp.get_json()
        logging.debug(data)
        self.assertEqual(data["order_id"], order.id)
        self.assertEqual(data["price"], product.price)
        self.assertEqual(data["quantity"], product.quantity)
        self.assertEqual(data["name"], product.name)

    def test_get_product(self):
        """ Get an product from an order """
        # create a known product
        order = self._create_orders(1)[0]
        product = ProductFactory()
        resp = self.app.post(
            "/orders/{}/products".format(order.id), json=product.serialize(), content_type="application/json")# pylint: disable=maybe-no-member
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        data = resp.get_json()
        logging.debug(data)
        product_id = data["id"]

        # retrieve it back
        resp = self.app.get(
            "/orders/{}/products/{}".format(order.id, product_id),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = resp.get_json()
        logging.debug(data)
        self.assertEqual(data["order_id"], order.id)
        self.assertEqual(data["name"], product.name)
        self.assertEqual(data["price"], product.price)
        self.assertEqual(data["quantity"], product.quantity)

    def test_update_product(self):
        """ Update an product on an order """
        # create a known product
        order = self._create_orders(1)[0]
        product = ProductFactory()
        resp = self.app.post(
            "/orders/{}/products".format(order.id), json=product.serialize(), content_type="application/json") # pylint: disable=maybe-no-member
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED) # pylint: disable=maybe-no-member

        data = resp.get_json()
        logging.debug(data)
        product_id = data["id"]
        data["name"] = "XXXX"

        # send the update back
        resp = self.app.put(
            "/orders/{}/products/{}".format(order.id, product_id), json=data,
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # retrieve it back
        resp = self.app.get(
            "/orders/{}/products/{}".format(order.id, product_id),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = resp.get_json()
        logging.debug(data)
        self.assertEqual(data["id"], product_id)
        self.assertEqual(data["order_id"], order.id)
        self.assertEqual(data["name"], "XXXX")

    def test_delete_product(self):
        """ Delete an Product """
        order = self._create_orders(1)[0]
        product = ProductFactory()
        resp = self.app.post(
            "/orders/{}/products".format(order.id), json=product.serialize(), content_type="application/json" # pylint: disable=maybe-no-member
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED) # pylint: disable=maybe-no-member
        data = resp.get_json() # pylint: disable=maybe-no-member
        logging.debug(data)
        product_id = data["id"]

        # send delete request
        resp = self.app.delete(
            "/orders/{}/products/{}".format(order.id, product_id),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

        # retrieve it back and make sure product is not there
        resp = self.app.get(
            "/orders/{}/products/{}".format(order.id, product_id),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
