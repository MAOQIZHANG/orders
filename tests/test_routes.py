"""
TestYourResourceModel API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from unittest import TestCase
from service import app
from datetime import datetime
from service.models import Order, db, init_db
from service.common import status  # HTTP Status Codes
from tests.factories import OrderFactory, ItemFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)

BASE_URL = "/orders"


######################################################################
#  T E S T   C A S E S
######################################################################
class TestOrderService(TestCase):
    """Order Service Tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)

    @classmethod
    def tearDownClass(cls):
        """Runs once before test suite"""

    def setUp(self):
        """Runs before each test"""
        db.session.query(Order).delete()  # clean up the last tests
        db.session.commit()

        self.client = app.test_client()

    def tearDown(self):
        """Runs once after each test case"""
        db.session.remove()

    ######################################################################
    #  H E L P E R   M E T H O D S
    ######################################################################

    def _create_orders(self, count):
        """Factory method to create orders in bulk"""
        orders = []
        for _ in range(count):
            order = OrderFactory()
            resp = self.client.post(BASE_URL, json=order.serialize())
            self.assertEqual(
                resp.status_code,
                status.HTTP_201_CREATED,
                "Could not create test Order",
            )
            new_order = resp.get_json()
            order.id = new_order["id"]
            orders.append(order)
        return orders

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """It should call the home page"""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_get_order_list(self):
        """It should Get a list of Accounts"""
        self._create_orders(5)
        resp = self.client.get(BASE_URL)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 5)

    def test_create_order(self):
        """It should Create a new Order"""
        order = OrderFactory()
        logging.debug("Test order: %s", order.serialize())
        resp = self.client.post(
            BASE_URL, json=order.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = resp.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_order = resp.get_json()
        print(new_order)
        self.assertEqual(new_order["name"], order.name, "Names does not match")
        self.assertEqual(
            datetime.fromisoformat(new_order["create_time"]),
            order.create_time,
            "Time does not match",
        )
        self.assertEqual(new_order["address"], order.address, "Address does not match")
        self.assertEqual(
            new_order["cost_amount"], order.cost_amount, "Cost does not match"
        )
        self.assertEqual(
            new_order["status"], order.status.name, "Status does not match"
        )

        # Check that the location header was correct by getting it
        # resp = self.client.get(location, content_type="application/json")
        resp = self.client.get(location)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_order = resp.get_json()
        print(new_order)
        self.assertEqual(new_order["name"], order.name, "Names does not match")
        self.assertEqual(
            datetime.fromisoformat(new_order["create_time"]),
            order.create_time,
            "Time does not match",
        )
        self.assertEqual(new_order["address"], order.address, "Address does not match")
        self.assertEqual(
            new_order["cost_amount"], order.cost_amount, "Cost does not match"
        )
        self.assertEqual(
            new_order["status"], order.status.name, "Status does not match"
        )
