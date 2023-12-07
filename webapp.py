from router import Router, render_template, redirect
import session_manager
from functools import wraps
import requests
from models import *

app = Router(__name__, 8000)
database_path = "database/food.db"

###################################################
################# Service Registry ################
###################################################
user_service = "http://localhost:8001"
delivery_service = "http://localhost:8002"


###################################################
################# User Service ####################
###################################################
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

            response = requests.post(user_service + "/login", data={"username": username, "password": password}).json()
            if response["status"] == "success":
                session_cookie = session_manager.create_session(username)
                user = response["user"]
                if user["user_type"] == "customer":
                    return redirect('/customer_home', session_cookie)
                elif user["user_type"] == "owner":
                    return redirect('/owner_home', session_cookie)
                elif user["user_type"] == "deliver":
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
            response = requests.post(user_service + "/register", data={"username": username, "password": password, "firstname": first_name, "lastname": last_name, "email": email, "usertype": user_type}).json()
            if response["status"] == "success":
                return redirect('/login')
            else:
                return redirect('/register')
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
        response = requests.get(user_service + "/getUserByUsername", params={"username": username}).json()
        user = User(response["user"]["username"], response["user"]["password"], response["user"]["first_name"], response["user"]["last_name"], response["user"]["email"], response["user"]["user_type"])
        template = requests.get(delivery_service + "/customer_home", params={"username": username}).text
        return template, None
    
@app.route('/addAddress', ['GET', 'POST'])
@login_required
def addAddress(request):
    if request.method == "GET":
        return render_template("addAddress.html")
    elif request.method == "POST":
        username = request.get_authenticated_username()
        response = requests.get(user_service + "/getUserByUsername", params={"username": username}).json()
        user = User(**response["user"])

        response = requests.post(delivery_service + "/addAddress", data={"username": username, "street": request.json['street'][0], "city": request.json['city'][0], "state": request.json['state'][0], "zip": request.json['zip'][0]}).json()
        if "status" in response and response["status"] == "success":
            return redirect('/customer_home')
 
    
@app.route('/addPayment', ['GET', 'POST'])
@login_required
def addPayment(request):
    if request.method == "GET":
        return render_template("addPayment.html")
    elif request.method == "POST":
        # user = accountController.getUserByUsername(request.get_authenticated_username())
        username = request.get_authenticated_username()
        response = requests.get(user_service + "/getUserByUsername", params={"username": username}).json()
        user = User(**response["user"])

        response = requests.post(delivery_service + "/addPayment", data={"username": username, "card_number": request.json['card_number'][0], "card_holder": request.json['card_holder'][0], "expiration_date": request.json['expiration_date'][0], "cvv": request.json['cvv'][0]}).json()
        if "status" in response and response["status"] == "success":
            return redirect('/customer_home')
    
@app.route('/customer_restaurant', ['GET', 'POST'])
@login_required
def customer_restaurant(request):
    if request.method == "GET":
        username = request.get_authenticated_username()
        response = requests.get(user_service + "/getUserByUsername", params={"username": username}).json()
        user = User(**response["user"])
        restaurant_id = request.qs['id'][0]
        template = requests.get(delivery_service + "/customer_restaurant", params={"username": username, "id": restaurant_id}).text
        return template, None
    
@app.route('/createOrder', ['GET', 'POST'])
@login_required
def createOrder(request):
    if request.method == "POST":
        print(request.json)
        restaurant_id = request.json['restaurant_id'][0]
        username = request.get_authenticated_username()
        response = requests.get(user_service + "/getUserByUsername", params={"username": username}).json()
        user = User(**response["user"])
        food_ids = request.json['itemIds']
        quantities = request.json['quantities']
        template = requests.post(delivery_service + "/createOrder", data={"username": username, "restaurant_id": restaurant_id, "itemIds": food_ids, "quantities": quantities}).text
        return template, None
    
    
@app.route('/checkout', ['GET', 'POST'])
@login_required
def checkout(request):
    if request.method == "POST":
        username = request.get_authenticated_username()
        response = requests.get(user_service + "/getUserByUsername", params={"username": username}).json()
        user = User(**response["user"])


        print(request.json)
        credit_card_id = request.json['payment'][0]
        address_id = request.json['address'][0]
        restaurant_id = request.json['restaurant_id'][0]

        response = requests.post(delivery_service + "/checkout", data={"username": username, "address": address_id, "payment": credit_card_id, "restaurant_id": restaurant_id}).json()
        if "status" in response and response["status"] == "success":
            return redirect('/customer_home')

    



###################################################
################# Owner Routes ####################
###################################################
@app.route('/owner_home', ['GET', 'POST'])
@login_required
def owner_home(request):
    if request.method == "GET":
        username = request.get_authenticated_username()
        template = requests.get(delivery_service + "/owner_home", params={"username": username}).text
        return template, None

@app.route('/addRestaurant', ['GET', 'POST'])
@login_required
def addRestaurant(request):
    if request.method == "GET":
        return render_template("addRestaurant.html")
    elif request.method == "POST":
        username = request.get_authenticated_username()

        name = request.json['name'][0]
        phone_number = request.json['phone_number'][0]
        email = request.json['email'][0]
        description = request.json['description'][0]

        street = request.json['street'][0]
        city = request.json['city'][0]
        state = request.json['state'][0]
        zip = request.json['zip'][0]
        
        response = requests.post(delivery_service + "/addRestaurant", data={"username": username, "name": name, "phone_number": phone_number, "email": email, "description": description, "street": street, "city": city, "state": state, "zip": zip}).json()
        if "status" in response and response["status"] == "success":
            return redirect('/owner_home')

    
@app.route('/owner_restaurant', ['GET', 'POST'])
@login_required
def owner_restaurant(request):
    if request.method == "GET":
        username = request.get_authenticated_username()
        restaurant_id = request.qs['id'][0]
        template = requests.get(delivery_service + "/owner_restaurant", params={"username": username, "id": restaurant_id}).text
        return template, None

@app.route('/order_detail', ['GET', 'POST'])
@login_required
def order_detail(request):
    if request.method == "GET":
        username = request.get_authenticated_username()
        order_id = request.qs['id'][0]
        restaurant_id = request.qs['restaurant_id'][0]

        template = requests.get(delivery_service + "/order_detail", params={"username": username, "restaurant_id": restaurant_id, "id": order_id}).text
        return template, None
    
@app.route('/processOrder', ['GET', 'POST'])
@login_required
def processOrder(request):
    if request.method == "GET":
        order_id = request.qs['id'][0]
        restaurant_id = request.qs['restaurant_id'][0]
        response = requests.get(delivery_service + "/processOrder", params={"id": order_id}).json()
        if "status" in response and response["status"] == "success":
            return redirect('/owner_restaurant?id=' + restaurant_id)
    
@app.route('/completeOrder', ['GET', 'POST'])
@login_required
def completeOrder(request):
    if request.method == "GET":
        order_id = request.qs['id'][0]
        restaurant_id = request.qs['restaurant_id'][0]
        response = requests.get(delivery_service + "/completeOrder", params={"id": order_id}).json()
        if "status" in response and response["status"] == "success":
            return redirect('/owner_restaurant?id=' + restaurant_id)

    
@app.route('/addFood', ['GET', 'POST'])
@login_required
def addFood(request):
    username = request.get_authenticated_username()
    if request.method == "GET":
        restaurant_id = request.qs['id'][0]
        template = requests.get(delivery_service + "/addFood", params={"id": restaurant_id}).text
        return template, None
    elif request.method == "POST":
        restaurant_id = request.json['id'][0]
        name = request.json['name'][0]
        price = request.json['price'][0]
        description = request.json['description'][0]
        response = requests.post(delivery_service + "/addFood", data={"username": username, "id": restaurant_id, "name": name, "price": price, "description": description}).json()
        if "status" in response and response["status"] == "success":
            return redirect('/owner_restaurant?id=' + restaurant_id)
    


###################################################
################# Deliver Routes ##################
###################################################
@app.route('/deliver_home', ['GET', 'POST'])
@login_required
def deliver_home(request):
    if request.method == "GET":
        username = request.get_authenticated_username()
        template = requests.get(delivery_service + "/deliver_home", params={"username": username}).text
        return template, None
    
@app.route('/deliver_order_detail', ['GET', 'POST'])
@login_required
def deliver_order_detail(request):
    if request.method == "GET":
        username = request.get_authenticated_username()
        order_id = request.qs['id'][0]
        template = requests.get(delivery_service + "/deliver_order_detail", params={"username": username, "id": order_id}).text
        return template, None

@app.route('/pickupOrder', ['GET', 'POST'])
@login_required
def pickupOrder(request):
    if request.method == "GET":
        username = request.get_authenticated_username()
        order_id = request.qs['id'][0]
        response = requests.get(delivery_service + "/pickupOrder", params={"username": username, "id": order_id}).json()
        if "status" in response and response["status"] == "success":
            return redirect('/deliver_home')
    
@app.route('/deliveredOrder', ['GET', 'POST'])
@login_required
def deliveredOrder(request):
    if request.method == "GET":
        order_id = request.qs['id'][0]
        response = requests.get(delivery_service + "/deliveredOrder", params={"id": order_id}).json()
        if "status" in response and response["status"] == "success":
            return redirect('/deliver_home')

if __name__ == "__main__":
    app.run()