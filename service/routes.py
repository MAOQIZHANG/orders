"""
My Service

Describe what your service does here
"""
from flask import jsonify, request, url_for, abort, make_response
from service.common import status  # HTTP Status Codes
from service.models import Order, Item
from datetime import datetime, timezone, timedelta

# Import Flask application
from . import app


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    return (
        jsonify(
            name="Order REST API Service",
            version="1.0",
            paths=url_for("list_orders", _external=True),
        ),
        status.HTTP_200_OK,
    )


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {media_type}",
    )


######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################
######################################################################
# FIND AN ORDER BY ID OR RETURN ALL ORDERS
######################################################################
@app.route("/orders", methods=["GET"])
def list_orders():
    """Find an order by ID or Returns all of the Orders"""
    app.logger.info("Request for Order list")
    orders = []

    # print("request.args = {}".format(request.args.to_dict(flat=False)))

    # Process the query string if any

    if len(request.args) == 0:  # This corresponds to "/orders"
        orders = Order.all()

        # Return as an array of dictionaries
        results = [order.serialize() for order in orders]

    elif "order_id" in request.args:
        order_id = request.args.get("order_id")
        order = Order.find(order_id)
        results = order.serialize()

    else:
        return make_response(jsonify(None), status.HTTP_404_NOT_FOUND)

    return make_response(jsonify(results), status.HTTP_200_OK)


######################################################################
# CREATE A NEW ORDER
######################################################################
@app.route("/orders", methods=["POST"])
def create_orders():
    """
    Creates an Order
    This endpoint will create an Order based the data in the body that is posted
    """
    app.logger.info("Request to create an Order")
    check_content_type("application/json")

    # Create the order
    order = Order()
    order.deserialize(request.get_json())
    order.create()

    # Create a message to return
    message = order.serialize()
    location_url = url_for("create_orders", order_id=order.id, _external=True)
    # print(location_url)

    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )

######################################################################
# UPDATE AN ORDER
######################################################################

@app.route("/orders/<int:order_id>", methods=["PUT"])
def update_an_order(order_id):
    """
    Update information (e.g., address, name) within 24 hours of placing the order.
    """
    app.logger.info(f"Update order information with ID {order_id}")

    # Find the order by ID
    order = Order.find(order_id)
    order.create_time = datetime.now(timezone.utc)

    if not order:
        abort(status.HTTP_404_NOT_FOUND, "Order not found")
    
    # Calcultate the time difference
    time_difference = datetime.now(timezone.utc) - order.create_time

    # Cannot update information on an order placed over 24 hours
    if time_difference > timedelta(hours = 24):
        return make_response("Cannot update order", status.HTTP_400_BAD_REQUEST)
    
    # Update the 'name' and 'address' fields of the order
    data = request.get_json()
    if "name" in data:
        order.name = data["name"]
    if "address" in data:
        order.address = data["address"]

    order.update()

    return make_response(
        jsonify(order.serialize()), status.HTTP_200_OK, {"Updated_order_id": order_id}
    )