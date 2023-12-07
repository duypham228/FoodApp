from router import Router, render_template, redirect
from dataAdapter import dataAdapter
import session_manager
from functools import wraps
import requests
from models import *

from controllers import customerController, ownerController, deliverController

app = Router(__name__, 8002)
database_path = "database/food.db"

###################################################
################# Service Registry ################
###################################################
user_service = "http://localhost:8001"
delivery_service = "http://localhost:8002"

def login_required(route_function):
    @wraps(route_function)
    def wrapper(request):
        # Get the session ID from the cookie
        # if request.cookies is not None:
        if request.is_authenticated():
            print("Authenticated")
            return route_function(request)
        else:
            print("Not authenticated")
            return redirect("/")
    return wrapper
 

# @login_required TODO: later after session management is implemented



###################################################
################# Customer Routes #################
###################################################
@app.route('/customer_home', ['GET', 'POST'])
def customer_home(request):
    if request.method == "GET":
        username = request.qs['username'][0]
        response = requests.get(user_service + "/getUserByUsername", params={"username": username}).json()
        user = User(**response["user"])
        # user = accountController.getUserByUsername(username)

        customerController.setUser(user)

        restaurants = customerController.getRestaurants()
        restaurants_list = ""
        for restaurant in restaurants:
            restaurants_list += f"<a class='list-group-item list-group-item-action' href='/customer_restaurant?id={restaurant.restaurant_id}'>{restaurant.name}</a>"
        restaurants_text = f"<div class='list-group'>{restaurants_list}</div>"


        addresses = customerController.getAddresses()
        addresses_list = ""
        for address in addresses:
            addresses_list += (
                f"<li class='list-group-item'>{address.address_id}: {address.street}, {address.city}, {address.state}, {address.zip}</li>"
            )
        addresses_text = f"<div class='list-group'>{addresses_list}</div>"


        payments = customerController.getPayments()
        payments_list = ""
        for payment in payments:
            payments_list += (
                f"<li class='list-group-item'>{payment.credit_card_id}: {payment.card_number}: {payment.holder_name}, {payment.expiration_date}, {payment.CVV}</li>"
            )
        payments_text = f"<div class='list-group'>{payments_list}</div>"
        context = {
            "username": user.username,
            "custom": restaurants_text,
            "address": addresses_text,
            "payment": payments_text
        }
        return render_template("customer_home.html", **context)
    
@app.route('/addAddress', ['GET', 'POST'])
def addAddress(request):
    if request.method == "GET":
        return render_template("addAddress.html")
    elif request.method == "POST":
        # user = accountController.getUserByUsername(request.get_authenticated_username())
        username = request.json['username'][0]
        response = requests.get(user_service + "/getUserByUsername", params={"username": username}).json()
        user = User(**response["user"])

        customerController.setUser(user)
        street = request.json['street'][0]
        city = request.json['city'][0]
        state = request.json['state'][0]
        zipcode = request.json['zip'][0]
        customerController.addAddress(street, city, state, zipcode)
        return {"status": "success"}, None
    
@app.route('/addPayment', ['GET', 'POST'])
def addPayment(request):
    if request.method == "GET":
        return render_template("addPayment.html")
    elif request.method == "POST":
        # user = accountController.getUserByUsername(request.get_authenticated_username())
        username = request.json['username'][0]
        response = requests.get(user_service + "/getUserByUsername", params={"username": username}).json()
        user = User(**response["user"])

        customerController.setUser(user)
        card_number = request.json['card_number'][0]
        card_holder = request.json['card_holder'][0]
        expiration_date = request.json['expiration_date'][0]
        cvv = request.json['cvv'][0]
        customerController.addPayment(card_number, card_holder, expiration_date, cvv)
        return {"status": "success"}, None
    
@app.route('/customer_restaurant', ['GET', 'POST'])
def customer_restaurant(request):
    if request.method == "GET":
        username = request.qs['username'][0]
        response = requests.get(user_service + "/getUserByUsername", params={"username": username}).json()
        user = User(**response["user"])

        customerController.setUser(user)
        restaurant_id = request.qs['id'][0]
        customerController.pickRestaurant(restaurant_id)


        foods = customerController.getFoodsByRestaurant(restaurant_id)
        foods_list = ""
        for food in foods:
            foods_list += f"<li>{food.food_id}) {food.name} - {food.price} - {food.description}></li>"
        foods_text = f"<ul>{foods_list}</ul>"
        context = {
            "name": customerController.restaurant.name,
            "menu": foods_text,
            "id": restaurant_id
        }
        return render_template("customer_restaurant.html", **context)
    
@app.route('/createOrder', ['GET', 'POST'])
def createOrder(request):
    if request.method == "POST":
        print(request.json)
        restaurant_id = request.json['restaurant_id'][0]
        username = request.json['username'][0]
        food_ids = request.json['itemIds']
        quantities = request.json['quantities']

        response = requests.get(user_service + "/getUserByUsername", params={"username": username}).json()
        user = User(**response["user"])
        customerController.setUser(user)
        customerController.pickRestaurant(restaurant_id)

        for i in range(len(food_ids)):
            customerController.addToCart(food_ids[i], int(quantities[i]))
        
        # order list input with food id and quantity
        order_list = ""
        order_list_input = ""
        for order_line in customerController.order.order_list:
            order_list += f"<li>{order_line.food_name} - {order_line.quantity} - {order_line.price}</li>"
        order_list_text = f"<ul>{order_list}</ul>"


        # radio for payment
        payments = customerController.getPayments()
        payments_list = ""
        for payment in payments:
            payments_list += f"<input type='radio' name='payment' value='{payment.credit_card_id}'> {payment.credit_card_id}: {payment.card_number}: {payment.holder_name}, {payment.expiration_date}, {payment.CVV}<br>"
        
        # radio for address
        addresses = customerController.getAddresses()
        addresses_list = ""
        for address in addresses:
            addresses_list += f"<input type='radio' name='address' value='{address.address_id}'> {address.address_id}: {address.street}, {address.city}, {address.state}, {address.zip}<br>"

        context = {
            "order": order_list_text,
            "payment": payments_list,
            "address": addresses_list,
            "restaurant_id": restaurant_id
        }

        return render_template("checkout.html", **context)
    
    
@app.route('/checkout', ['GET', 'POST'])
def checkout(request):
    if request.method == "POST":
        username = request.json['username'][0]
        response = requests.get(user_service + "/getUserByUsername", params={"username": username}).json()
        user = User(**response["user"])

        customerController.setUser(user)

        print(request.json)
        credit_card_id = request.json['payment'][0]
        address_id = request.json['address'][0]
        restaurant_id = request.json['restaurant_id'][0]
        customerController.pickRestaurant(restaurant_id)

        customerController.checkout(address_id, credit_card_id)        

        return {"status": "success"}, None
    



###################################################
################# Owner Routes ####################
###################################################
@app.route('/owner_home', ['GET', 'POST'])
def owner_home(request):
    if request.method == "GET":
        username = request.qs['username'][0]
        response = requests.get(user_service + "/getUserByUsername", params={"username": username}).json()
        user = User(**response["user"])

        ownerController.setUser(user)
        restaurants = ownerController.getRestaurants()
        restaurants_list = ""
        for restaurant in restaurants:
            restaurants_list += f"<li><a href='/owner_restaurant?id={restaurant.restaurant_id}'>{restaurant.name}</a></li>"
        restaurants_text = f"<ul>{restaurants_list}</ul>"
        context = {
            "username": user.username,
            "custom": restaurants_text
        }
        return render_template("owner_home.html", **context)

@app.route('/addRestaurant', ['GET', 'POST'])
def addRestaurant(request):
    if request.method == "GET":
        return render_template("addRestaurant.html")
    elif request.method == "POST":
        username = request.json['username'][0]
        response = requests.get(user_service + "/getUserByUsername", params={"username": username}).json()
        user = User(**response["user"])
        ownerController.setUser(user)

        name = request.json['name'][0]
        phone_number = request.json['phone_number'][0]
        email = request.json['email'][0]
        description = request.json['description'][0]

        street = request.json['street'][0]
        city = request.json['city'][0]
        state = request.json['state'][0]
        zipcode = request.json['zip'][0]

        ownerController.addRestaurant(name, phone_number, email, description, street, city, state, zipcode)
        return {"status": "success"}, None

    
@app.route('/owner_restaurant', ['GET', 'POST'])
def owner_restaurant(request):
    if request.method == "GET":
        username = request.qs['username'][0]
        response = requests.get(user_service + "/getUserByUsername", params={"username": username}).json()
        user = User(**response["user"])
        restaurant_id = request.qs['id'][0]

        ownerController.setUser(user)
        ownerController.setRestaurant(restaurant_id)

        address_id = ownerController.restaurant.address_id
        adapter = dataAdapter(database_path)
        address = adapter.getAddress(address_id)
        foods = ownerController.getFoodByRestaurant(restaurant_id)
        foods_list = ""
        for food in foods:
            foods_list += f"<li>{food.name} - {food.price} - {food.description}</li>"
        foods_text = f"<ul>{foods_list}</ul>"

        pending_orders = ownerController.getPendingOrders()
        pending_orders_list = ""
        for order in pending_orders:
            pending_orders_list += f"<li>{order.order_id} - {order.status} <a href='/order_detail?id={order.order_id}&restaurant_id={restaurant_id}'>View Detail</a></li>"
        pending_orders_text = f"<ul>{pending_orders_list}</ul>"

        processing_orders = ownerController.getProcessingOrders()
        processing_orders_list = ""
        for order in processing_orders:
            processing_orders_list += f"<li>{order.order_id} - {order.status} <a href='/order_detail?id={order.order_id}&restaurant_id={restaurant_id}'>View Detail</a></li>"
        processing_orders_text = f"<ul>{processing_orders_list}</ul>"
        
        ready_orders = ownerController.getReadyOrders()
        ready_orders_list = ""
        for order in ready_orders:
            ready_orders_list += f"<li>{order.order_id} - {order.status} <a href='/order_detail?id={order.order_id}&restaurant_id={restaurant_id}'>View Detail</a></li>"
        ready_orders_text = f"<ul>{ready_orders_list}</ul>"

        context = {
            "name": ownerController.restaurant.name,
            "address": address,
            "menu": foods_text,
            "pending": pending_orders_text,
            "processing": processing_orders_text,
            "ready": ready_orders_text,
            "id": restaurant_id
        }
        return render_template("owner_restaurant.html", **context)

@app.route('/order_detail', ['GET', 'POST'])
def order_detail(request):
    if request.method == "GET":
        username = request.qs['username'][0]
        response = requests.get(user_service + "/getUserByUsername", params={"username": username}).json()
        user = User(**response["user"])
        order_id = request.qs['id'][0]
        restaurant_id = request.qs['restaurant_id'][0]

        ownerController.setUser(user)
        ownerController.setRestaurant(restaurant_id)

        order = ownerController.getOrderById(order_id)
        order_list = ""
        for order_line in order.order_list:
            order_list += f"<li>{order_line.food_name} - {order_line.quantity} - {order_line.price}</li>"
        order_list_text = f"<ul>{order_list}</ul>"
        context = {
            "order": order_list_text,
            "order_id": order_id,
            "restaurant_id": restaurant_id
        }
        return render_template("orderDetail.html", **context)
    
@app.route('/processOrder', ['GET', 'POST'])
def processOrder(request):
    if request.method == "GET":
        order_id = request.qs['id'][0]
        ownerController.processOrder(order_id)
        return {"status": "success"}, None
    
@app.route('/completeOrder', ['GET', 'POST'])
def completeOrder(request):
    if request.method == "GET":
        order_id = request.qs['id'][0]
        ownerController.completeOrder(order_id)
        return {"status": "success"}, None

    
@app.route('/addFood', ['GET', 'POST'])
def addFood(request):
    if request.method == "GET":
        restaurant_id = request.qs['id'][0]
        context = {
            "id": restaurant_id
        }
        return render_template("addFood.html", **context)
    elif request.method == "POST":
        restaurant_id = request.json['id'][0]
        username = request.json['username'][0]
        response = requests.get(user_service + "/getUserByUsername", params={"username": username}).json()
        user = User(**response["user"])
        ownerController.setUser(user)
        ownerController.setRestaurant(restaurant_id)
        name = request.json['name'][0]
        price = request.json['price'][0]
        description = request.json['description'][0]
        ownerController.addFood(name, price, description)
        return {"status": "success"}, None




###################################################
################# Deliver Routes ##################
###################################################
@app.route('/deliver_home', ['GET', 'POST'])
def deliver_home(request):
    if request.method == "GET":
        username = request.qs["username"][0]
        response = requests.get(user_service + "/getUserByUsername", params={"username": username}).json()
        user = User(**response["user"])
        deliverController.setUser(user)

        ready_orders = deliverController.getReadyOrders()
        ready_orders_list = ""
        for order in ready_orders:
            ready_orders_list += f"<li>{order.order_id} - {order.status} <a href='/deliver_order_detail?id={order.order_id}'>View Detail</a></li>"
        ready_orders_text = f"<ul>{ready_orders_list}</ul>"

        delivering_orders = deliverController.getDeliveringOrders()
        delivering_orders_list = ""
        for order in delivering_orders:
            delivering_orders_list += f"<li>{order.order_id} - {order.status} <a href='/deliver_order_detail?id={order.order_id}'>View Detail</a></li>"
        delivering_orders_text = f"<ul>{delivering_orders_list}</ul>"
        
        delivered_orders = deliverController.getDeliveredOrders()
        delivered_orders_list = ""
        for order in delivered_orders:
            delivered_orders_list += f"<li>{order.order_id} - {order.status} <a href='/deliver_order_detail?id={order.order_id}'>View Detail</a></li>"
        delivered_orders_text = f"<ul>{delivered_orders_list}</ul>"

        context = {
            "username": user.username,
            "ready": ready_orders_text,
            "delivering": delivering_orders_text,
            "delivered": delivered_orders_text
        }
        return render_template("deliver_home.html", **context)
    
@app.route('/deliver_order_detail', ['GET', 'POST'])
def deliver_order_detail(request):
    if request.method == "GET":
        username = request.qs['username'][0]
        response = requests.get(user_service + "/getUserByUsername", params={"username": username}).json()
        user = User(**response["user"])

        order_id = request.qs['id'][0]

        deliverController.setUser(user)

        order = deliverController.getOrderById(order_id)
        order_list = ""
        for order_line in order.order_list:
            order_list += f"<li>{order_line.food_name} - {order_line.quantity} - {order_line.price}</li>"
        order_list_text = f"<ul>{order_list}</ul>"
        context = {
            "order": order_list_text,
            "order_id": order_id
        }
        return render_template("deliverOrderDetail.html", **context)
    
@app.route('/pickupOrder', ['GET', 'POST'])
def pickupOrder(request):
    if request.method == "GET":
        username = request.qs['username'][0]
        response = requests.get(user_service + "/getUserByUsername", params={"username": username}).json()
        user = User(**response["user"])
        deliverController.setUser(user)
        order_id = request.qs['id'][0]
        deliverController.pickupOrder(order_id)
        return {"status": "success"}, None
    
@app.route('/deliveredOrder', ['GET', 'POST'])
def deliveredOrder(request):
    if request.method == "GET":
        order_id = request.qs['id'][0]
        deliverController.completeOrder(order_id)
        return {"status": "success"}, None
    
if __name__ == "__main__":
    app.run()