"""
Models for Order
All of the models are stored in this module
"""
import logging
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app") # pylint: disable=locally-disabled, invalid-name

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy() # pylint: disable=locally-disabled, invalid-name

class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """
    pass

# DATETIME_FORMAT='%Y-%m-%d %H:%M:%S.%f'

######################################################################
#  P E R S I S T E N T   B A S E   M O D E L
######################################################################
class PersistentBase():
    """ Base class added persistent methods """

    def create(self):
        """
        Creates a Order to the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def save(self):
        """ Updates a Order to the database """
        logger.info("Saving %s", self.name)
        db.session.commit()

    def delete(self):
        """ Removes a Order from the data store """
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def init_db(cls, app):
        """ Initializes the database session """
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """ Returns all of the records in the database """
        logger.info("Processing all records")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """ Finds a record by it's ID """
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_or_404(cls, by_id):
        """ Find a record by it's id """
        logger.info("Processing lookup or 404 for id %s ...", by_id)
        return cls.query.get_or_404(by_id)


######################################################################
#  P R O D U C T   M O D E L
######################################################################
class Product(db.Model, PersistentBase):
    """
    Class that represents a Product
    """
    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Integer)
    name = db.Column(db.String(64))
    def __repr__(self):
        return "<Product %r id=[%s] order[%s]>" % (self.name, self.id, self.order_id)
    def __str__(self):
        return "%s: %s, %s" % (self.name, self.quantity, self.price)
    def serialize(self):
        """ Serializes a Product into a dictionary """
        return {
            "id": self.id,
            "order_id": self.order_id,
            "name": self.name,
            "quantity": self.quantity,
            "price": self.price
        }

    def deserialize(self, data):
        """
        Deserializes a Product from a dictionary
        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.order_id = data["order_id"]
            self.name = data["name"]
            self.quantity = data["quantity"]
            self.price = data["price"]
        except KeyError as error:
            raise DataValidationError("Invalid Item: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError(
                "Invalid Item: body of request contained" "bad or no data"
            )
        return self
######################################################################
#  O R D E R   M O D E L
######################################################################
class Order(db.Model, PersistentBase):
    """
    Class that represents an Order
    """
    app = None
    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    status = db.Column(db.String(64))
    products = db.relationship('Product', backref='order', lazy=True)
    def __repr__(self):
        return "<Order %r id=[%s]>" % (self.name, self.id)
    def serialize(self):
        """ Serializes a Account into a dictionary """
        order = {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "products": []
        }
        for product in self.products:
            order['products'].append(product.serialize())
        return order
    def deserialize(self, data):
        """
        Deserializes a Order from a dictionary
        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.name = data["name"]
            self.status = data["status"]
            # handle inner list of products
            product_list = data.get("products")
            for json_product in product_list:
                product = Product()
                product.deserialize(json_product)
                self.products.append(product)
        except KeyError as error:
            raise DataValidationError("Invalid Order: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError(
                "Invalid Order: body of request contained" "bad or no data"
            )
        return self

    @classmethod
    def find_by_name(cls, name):
        """ Returns all Orders with the given customer_id
        Args:
            name(string): the name on the Orders you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)
