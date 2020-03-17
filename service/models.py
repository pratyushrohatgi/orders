"""
Models for Orders

All of the models are stored in this module
"""
import logging
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()

class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """
    pass


class Orders(db.Model):
    """
    Class that represents a Orders
    """

    app = None

    # Table Schema
    order_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer)
    customer_id = db.Column(db.Integer)
    price = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    status = db.Column(db.Enum('Delivered', 'In Progress', 'Cancelled'))


    def __repr__(self):
        return "<Orders %r id=[%s]>" % (self.name, self.id)

    def create(self):
        """
        Creates a Orders to the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def save(self):
        """
        Updates a Orders to the database
        """
        logger.info("Saving %s", self.name)
        db.session.commit()

    def delete(self):
        """ Removes a Orders from the data store """
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a Orders into a dictionary """
        return {
            "order_id": self.order_id,
            "product_id": self.product_id,
            "customer_id": self.order_id,
            
        }

    def deserialize(self, data):
        """
        Deserializes a Orders from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.order_id = data["order_id"]
            self.product_id = data["product_id"]
            self.customer_id = data["customer_id"]
        except KeyError as error:
            raise DataValidationError("Invalid Orders: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError(
                "Invalid Orders: body of request contained" "bad or no data"
            )
        return self

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
        """ Returns all of the Orderss in the database """
        logger.info("Processing all Orderss")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """ Finds a Orders by it's ID """
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_or_404(cls, by_id):
        """ Find a Orders by it's id """
        logger.info("Processing lookup or 404 for id %s ...", by_id)
        return cls.query.get_or_404(by_id)

    @classmethod
    def find_by_order_id(cls, order_id):
        """ Returns all Orders with the given name

        Args:
            name (string): the name of the Orders you want to match
        """
        logger.info("Processing name query for %s ...", order_id)
        return cls.query.filter(cls.order_id == order_id)
