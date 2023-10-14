"""
Models for Order

All of the models are stored in this module
"""
import logging
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


# Function to initialize the database
def init_db(app):
    """Initializes the SQLAlchemy app"""
    Order.init_db(app)


class DataValidationError(Exception):
    """Used for an data validation errors when deserializing"""


class Order(db.Model):
    """
    Class that represents a Order
    """

    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63))
    created_at = db.Column(db.datetime, default=datetime.utcnow)
    address = db.Column(db.String(255), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    cost_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    items = db.relationship("Item", backref="order", lazy=True)

    def __repr__(self):
        return f"<Order {self.name} id=[{self.id}]>"

    def create(self):
        """
        Creates a Order to the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # pylint: disable=invalid-name
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a Order to the database
        """
        logger.info("Saving %s", self.name)
        db.session.commit()

    def delete(self):
        """Removes a Order from the data store"""
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """Serializes a Order into a dictionary"""
        return {"id": self.id, "name": self.name}

    def deserialize(self, data):
        """
        Deserializes a Order from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.name = data["name"]
        except KeyError as error:
            raise DataValidationError(
                "Invalid Order: missing " + error.args[0]
            ) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid Order: body of request contained bad or no data - "
                "Error message: " + error
            ) from error
        return self

    @classmethod
    def init_db(cls, app):
        """Initializes the database session"""
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """Returns all of the Orders in the database"""
        logger.info("Processing all Orders")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """Finds a Order by it's ID"""
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_by_name(cls, name):
        """Returns all Orders with the given name

        Args:
            name (string): the name of the Orders you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)


class Item(db.Model):
    """
    Class that represents an Item
    """

    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    url = db.Column(db.String(255), nullable=True)
    product_id = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Item {self.name} id=[{self.id}]>"

    def create(self):
        """
        Creates a Item to the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # pylint: disable=invalid-name
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a Item to the database
        """
        logger.info("Saving %s", self.name)
        db.session.commit()

    def delete(self):
        """Removes a Item from the data store"""
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """Serializes a Item into a dictionary"""
        return {"id": self.id, "name": self.name}

    def deserialize(self, data):
        """
        Deserializes a Item from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.name = data["name"]
        except KeyError as error:
            raise DataValidationError(
                "Invalid Item: missing " + error.args[0]
            ) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid Item: body of request contained bad or no data - "
                "Error message: " + error
            ) from error
        return self

    @classmethod
    def init_db(cls, app):
        """Initializes the database session"""
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """Returns all of the Items in the database"""
        logger.info("Processing all Items")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """Finds a Item by it's ID"""
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_by_name(cls, name):
        """Returns all Items with the given name

        Args:
            name (string): the name of the Items you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)
