from router import Router, render_template, redirect
from dataAdapter import dataAdapter
import session_manager
from functools import wraps

from controllers import accountController, customerController, ownerController, deliverController

app = Router(__name__)
database_path = "database/food.db"

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
 
@app.route('/', ['GET'])
def index(request):
    return render_template("index.html")

@app.route('/login', ['GET','POST'])
def login(request):
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        # print(request.headers)
        if 'username' in request.json and 'password' in request.json:
            username = request.json['username'][0]
            password = request.json['password'][0]

            user = accountController.login(username, password)
            if user is not None:
                session_cookie = session_manager.create_session(username)
                if user.user_type == "customer":
                    return redirect('/customer_home', session_cookie)
                elif user.user_type == "owner":
                    return redirect('/owner_home', session_cookie)
                elif user.user_type == "deliver":
                    return redirect('/deliver_home', session_cookie)
            return redirect('/login')
        else:
            return redirect('/login')
        
@app.route('/register', ['GET','POST'])
def register(request):
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        if 'username' in request.json and 'password' in request.json:
            username = request.json['username'][0]
            password = request.json['password'][0]
            first_name = request.json['firstname'][0]
            last_name = request.json['lastname'][0]
            email = request.json['email'][0]
            user_type = request.json['usertype'][0]
            accountController.register(username, password, first_name, last_name, email, user_type)
            return redirect('/login')
        else:
            return redirect('/register')
        



# @login_required TODO: later after session management is implemented



###################################################
################# Customer Routes #################
###################################################
@app.route('/customer_home', ['GET', 'POST'])
@login_required
def customer_home(request):
    if request.method == "GET":
        username = request.get_authenticated_username()
        user = accountController.getUserByUsername(username)

        customerController.setUser(user)

        restaurants = customerController.getRestaurants()
        restaurants_list = ""
        for restaurant in restaurants:
            restaurants_list += f"<li><a href='/customter_restaurant?id={restaurant.restaurant_id}'>{restaurant.name}</a></li>"
        restaurants_text = f"<ul>{restaurants_list}</ul>"

        addresses = customerController.getAddresses()
        addresses_list = ""
        for address in addresses:
            addresses_list += f"<li>{address.address_id}: {address.street}, {address.city}, {address.state}, {address.zip}</li>"
        addresses_text = f"<ul>{addresses_list}</ul>"

        payments = customerController.getPayments()
        payments_list = ""
        for payment in payments:
            payments_list += f"<li>{payment.credit_card_id}: {payment.card_number}: {payment.holder_name}, {payment.expiration_date}, {payment.CVV}</li>"        
        payments_text = f"<ul>{payments_list}</ul>"

        context = {
            "username": user.username,
            "custom": restaurants_text,
            "address": addresses_text,
            "payment": payments_text
        }
        return render_template("customer_home.html", **context)
    
@app.route('/addAddress', ['GET', 'POST'])
@login_required
def addAddress(request):
    if request.method == "GET":
        return render_template("addAddress.html")
    elif request.method == "POST":
        user = accountController.getUserByUsername(request.get_authenticated_username())
        customerController.setUser(user)
        street = request.json['street'][0]
        city = request.json['city'][0]
        state = request.json['state'][0]
        zipcode = request.json['zip'][0]
        customerController.addAddress(street, city, state, zipcode)
        return redirect('/customer_home')
    
@app.route('/addPayment', ['GET', 'POST'])
@login_required
def addPayment(request):
    if request.method == "GET":
        return render_template("addPayment.html")
    elif request.method == "POST":
        user = accountController.getUserByUsername(request.get_authenticated_username())
        customerController.setUser(user)
        card_number = request.json['card_number'][0]
        card_holder = request.json['card_holder'][0]
        expiration_date = request.json['expiration_date'][0]
        cvv = request.json['cvv'][0]
        customerController.addPayment(card_number, card_holder, expiration_date, cvv)
        return redirect('/customer_home')
    
@app.route('/customter_restaurant', ['GET', 'POST'])
@login_required
def customter_restaurant(request):
    if request.method == "GET":
        username = request.get_authenticated_username()
        user = accountController.getUserByUsername(username)
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
@login_required
def createOrder(request):
    if request.method == "POST":
        print(request.json)
        restaurant_id = request.json['restaurant_id'][0]

        user = accountController.getUserByUsername(request.get_authenticated_username())
        customerController.setUser(user)
        customerController.pickRestaurant(restaurant_id)

        food_ids = request.json['itemIds']
        quantities = request.json['quantities']
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
@login_required
def checkout(request):
    if request.method == "POST":
        user = accountController.getUserByUsername(request.get_authenticated_username())
        customerController.setUser(user)

        print(request.json)
        credit_card_id = request.json['payment'][0]
        address_id = request.json['address'][0]
        restaurant_id = request.json['restaurant_id'][0]
        customerController.pickRestaurant(restaurant_id)

        customerController.checkout(address_id, credit_card_id)        

        return redirect('/customer_home')
    



###################################################
################# Owner Routes ####################
###################################################
@app.route('/owner_home', ['GET', 'POST'])
@login_required
def owner_home(request):
    if request.method == "GET":
        username = request.get_authenticated_username()
        user = accountController.getUserByUsername(username)
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
@login_required
def addRestaurant(request):
    if request.method == "GET":
        return render_template("addRestaurant.html")
    elif request.method == "POST":
        name = request.json['name'][0]
        phone_number = request.json['phone_number'][0]
        email = request.json['email'][0]
        description = request.json['description'][0]

        street = request.json['street'][0]
        city = request.json['city'][0]
        state = request.json['state'][0]
        zipcode = request.json['zip'][0]

        
        ownerController.addRestaurant(name, phone_number, email, description, street, city, state, zipcode)
        return redirect('/owner_home')

    
@app.route('/owner_restaurant', ['GET', 'POST'])
@login_required
def owner_restaurant(request):
    if request.method == "GET":
        username = request.get_authenticated_username()
        user = accountController.getUserByUsername(username)
        restaurant_id = request.qs['id'][0]

        ownerController.setUser(user)
        ownerController.setRestaurant(restaurant_id)

        # restaurants_list = ""
        # for restaurant in restaurants:
        #     restaurants_list += f"<li>{restaurant.name}</li>"
        # restaurants_text = f"<ul>{restaurants_list}</ul>"
        address_id = ownerController.restaurant.address_id
        adapter = dataAdapter(database_path)
        address = adapter.getAddress(address_id)
        foods = adapter.getFoodByRestaurant(restaurant_id)
        foods_list = ""
        for food in foods:
            foods_list += f"<li>{food.name} - {food.price} - {food.description}</li>"
        foods_text = f"<ul>{foods_list}</ul>"

        pending_orders = ownerController.getPendingOrders()
        pending_orders_list = ""
        for order in pending_orders:
            pending_orders_list += f"<li>{order.order_id} - {ownerController.getCustomerById(order.customer_id).first_name} - {order.status} <a href='/order_detail?id={order.order_id}&restaurant_id={restaurant_id}'>View Detail</a></li>"
        pending_orders_text = f"<ul>{pending_orders_list}</ul>"

        processing_orders = ownerController.getProcessingOrders()
        processing_orders_list = ""
        for order in processing_orders:
            processing_orders_list += f"<li>{order.order_id} - {ownerController.getCustomerById(order.customer_id).first_name} - {order.status} <a href='/order_detail?id={order.order_id}&restaurant_id={restaurant_id}'>View Detail</a></li>"
        processing_orders_text = f"<ul>{processing_orders_list}</ul>"
        
        ready_orders = ownerController.getReadyOrders()
        ready_orders_list = ""
        for order in ready_orders:
            ready_orders_list += f"<li>{order.order_id} - {ownerController.getCustomerById(order.customer_id).first_name} - {order.status} <a href='/order_detail?id={order.order_id}&restaurant_id={restaurant_id}'>View Detail</a></li>"
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
@login_required
def order_detail(request):
    if request.method == "GET":
        username = request.get_authenticated_username()
        user = accountController.getUserByUsername(username)
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
@login_required
def processOrder(request):
    if request.method == "GET":
        order_id = request.qs['id'][0]
        restaurant_id = request.qs['restaurant_id'][0]
        ownerController.processOrder(order_id)
        return redirect('/owner_restaurant?id=' + restaurant_id)
    
@app.route('/completeOrder', ['GET', 'POST'])
@login_required
def completeOrder(request):
    if request.method == "GET":
        order_id = request.qs['id'][0]
        restaurant_id = request.qs['restaurant_id'][0]
        ownerController.completeOrder(order_id)
        return redirect('/owner_restaurant?id=' + restaurant_id)

    
@app.route('/addFood', ['GET', 'POST'])
@login_required
def addFood(request):
    user = accountController.getUserByUsername(request.get_authenticated_username())
    ownerController.setUser(user)
    if request.method == "GET":
        restaurant_id = request.qs['id'][0]
        context = {
            "id": restaurant_id
        }
        return render_template("addFood.html", **context)
    elif request.method == "POST":
        restaurant_id = request.json['id'][0]
        ownerController.setRestaurant(restaurant_id)
        name = request.json['name'][0]
        price = request.json['price'][0]
        description = request.json['description'][0]
        ownerController.addFood(name, price, description)
        return redirect('/owner_restaurant?id=' + restaurant_id)
    
# @app.route('/completeOrder', ['GET', 'POST'])
# @login_required
# def completeOrder(request):
#     if request.method == "GET":
#         order_id = request.json['id'][0]
#         ownerController.completeOrder(order_id)
#         return redirect('/owner_restaurant?id=' + restaurant_id)



###################################################
################# Deliver Routes ##################
###################################################
@app.route('/deliver_home', ['GET', 'POST'])
@login_required
def deliver_home(request):
    if request.method == "GET":
        username = request.get_authenticated_username()
        user = accountController.getUserByUsername(username)
        deliverController.setUser(user)

        ready_orders = deliverController.getReadyOrders()
        ready_orders_list = ""
        for order in ready_orders:
            ready_orders_list += f"<li>{order.order_id} - {deliverController.getCustomerById(order.customer_id).first_name} - {order.status} <a href='/deliver_order_detail?id={order.order_id}'>View Detail</a></li>"
        ready_orders_text = f"<ul>{ready_orders_list}</ul>"

        delivering_orders = deliverController.getDeliveringOrders()
        delivering_orders_list = ""
        for order in delivering_orders:
            delivering_orders_list += f"<li>{order.order_id} - {deliverController.getCustomerById(order.customer_id).first_name} - {order.status} <a href='/deliver_order_detail?id={order.order_id}'>View Detail</a></li>"
        delivering_orders_text = f"<ul>{delivering_orders_list}</ul>"
        
        delivered_orders = deliverController.getDeliveredOrders()
        delivered_orders_list = ""
        for order in delivered_orders:
            delivered_orders_list += f"<li>{order.order_id} - {deliverController.getCustomerById(order.customer_id).first_name} - {order.status} <a href='/deliver_order_detail?id={order.order_id}'>View Detail</a></li>"
        delivered_orders_text = f"<ul>{delivered_orders_list}</ul>"

        context = {
            "username": user.username,
            "ready": ready_orders_text,
            "delivering": delivering_orders_text,
            "delivered": delivered_orders_text
        }
        return render_template("deliver_home.html", **context)
    
@app.route('/deliver_order_detail', ['GET', 'POST'])
@login_required
def deliver_order_detail(request):
    if request.method == "GET":
        username = request.get_authenticated_username()
        user = accountController.getUserByUsername(username)
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
@login_required
def pickupOrder(request):
    if request.method == "GET":
        user = accountController.getUserByUsername(request.get_authenticated_username())
        deliverController.setUser(user)
        order_id = request.qs['id'][0]
        deliverController.pickupOrder(order_id)
        return redirect('/deliver_home')
    
@app.route('/deliveredOrder', ['GET', 'POST'])
@login_required
def deliveredOrder(request):
    if request.method == "GET":
        order_id = request.qs['id'][0]
        deliverController.completeOrder(order_id)
        return redirect('/deliver_home')
    
if __name__ == "__main__":
    app.run()