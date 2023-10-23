from dataAdapter import dataAdapter
from models import Order, OrderLine, Food, Restaurant, User, Address, CreditCard
from datetime import datetime

database_path = "database/food-clone.db"

class accountController:
    def __init__(self):
        pass
    
    def register(self, username, password, first_name, last_name, email, user_type):
        db = dataAdapter(database_path)
        user = User(None, username, password, first_name, last_name, email, user_type)
        db.saveUser(user)
        db.close()
    
    def login(self, username, password):
        db = dataAdapter(database_path)
        user = db.getUserByUsername(username)
        db.close()
        if user is not None and user.password == password:
            return True
        return False
    

class customerController:
    def __init__(self):
        self.user = User()
        self.order = Order()
        self.current_restaurant_id = None

    # Assume Login is successful
    def setUser(self):
        db = dataAdapter(database_path)
        self.user = db.getUser(1)

    def getRestaurants(self):
        db = dataAdapter(database_path)
        restaurants = db.getAllRestaurants()
        db.close()
        return restaurants

    def getRestaurant(self, restaurant_id):
        db = dataAdapter(database_path)
        restaurant = db.getRestaurant(restaurant_id)
        db.close()
        return restaurant
    
    def pickRestaurant(self, restaurant_id):
        self.current_restaurant_id = restaurant_id

    def getFoodsByRestaurant(self, restaurant_id):
        db = dataAdapter(database_path)
        foods = db.getFoodByRestaurant(restaurant_id)
        db.close()
        return foods

    def getFood(self, food_id):
        db = dataAdapter(database_path)
        food = db.getFood(food_id)
        db.close()
        return food
    
    def addToCart(self, food_id, quantity):
        db = dataAdapter(database_path)
        food = self.getFood(food_id)
        order_line = OrderLine(None, self.order.order_id, food_id, food.name, quantity, food.price * quantity)
        self.order.order_list.append(order_line)
    
    def removeFromCart(self, food_id):
        for order_line in self.cart:
            if order_line.food_id == food_id:
                self.cart.remove(order_line)
    
    def showCart(self):
        for order_line in self.order.order_list:
            print(f"{order_line.food_id}: {order_line.food_name} - {order_line.quantity} - ${order_line.price}")

    def addAddress(self):
        street = input("Please enter your street: ")
        city = input("Please enter your city: ")
        state = input("Please enter your state: ")
        zip_code = input("Please enter your zip code: ")
        address = Address(None, street, city, state, zip_code)
        db = dataAdapter(database_path)
        address_id = db.saveAddress(address)
        shipping_id = db.saveShipping(self.user.user_id, address_id)
        db.close()

    def addPayment(self):
        card_number = input("Please enter your card number: ")
        card_holder = input("Please enter your card holder: ")
        expiration_date = input("Please enter your expiration date: ")
        security_code = input("Please enter your security code: ")
        db = dataAdapter(database_path)
        credit_card = CreditCard(None, card_number, card_holder, expiration_date, security_code)
        credit_card_id = db.saveCreditCard(credit_card)
        payment_id = db.savePayment(self.user.user_id, credit_card_id)
        db.close()

        

        

    def checkout(self):
        db = dataAdapter(database_path)
        self.order.order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.order.customer_id = self.user.user_id
        self.order.restaurant_id = self.current_restaurant_id
        self.order.total_cost = 0
        for order_line in self.order.order_list:
            self.order.total_cost += order_line.price
        self.order.status = "pending"

        # Remember to update status of order after delivery
        order_id = db.saveOrder(self.order)
        db.close()
        self.order.order_id = order_id

        print("Your Total is: ", self.order.total_cost)
        print("Your Order is Placed!")
        print("--------------------------")
        print("Order Summary:")
        print(f"Order ID: {self.order.order_id}")
        print(f"Order Date: {self.order.order_date}")
        print(f"Customer ID: {self.order.customer_id}")
        print(f"Restaurant ID: {self.order.restaurant_id}")
        print(f"Total Cost: {self.order.total_cost}")
        print(f"Status: {self.order.status}")
        print("--------------------------")
        print()
        self.order = Order()

class ownerController:
    def __init__(self):
        self.user = User()
        self.restaurant = Restaurant()


    # Assume Login is successful
    def setUser(self):
        db = dataAdapter(database_path)
        self.user = db.getUser(2)


    def setRestaurant(self):
        db = dataAdapter(database_path)
        self.restaurant = db.getRestaurant(1)


    def getOrders(self):
        db = dataAdapter(database_path)
        orders = db.getOrdersByRestaurant(self.restaurant.restaurant_id)
        db.close()
        return orders

    def getPendingOrders(self):
        db = dataAdapter(database_path)
        orders = db.getPendingOrdersByRestaurant(self.restaurant.restaurant_id)
        db.close()
        return orders
    
    def getProcessingOrders(self):
        db = dataAdapter(database_path)
        orders = db.getProcessingOrdersByRestaurant(self.restaurant.restaurant_id)
        db.close()
        return orders

    def getReadyOrders(self):
        db = dataAdapter(database_path)
        orders = db.getReadyOrdersByRestaurant(self.restaurant.restaurant_id)
        db.close()
        return orders
    
    def processOrder(self, order_id):
        db = dataAdapter(database_path)
        order = db.getOrder(order_id)
        order.status = "processing"
        db.updateOrder(order)
        db.close()
    
    def completeOrder(self, order_id):
        db = dataAdapter(database_path)
        order = db.getOrder(order_id)
        order.status = "ready"
        db.updateOrder(order)
        db.close()
    
class deliverController:
    def __init__(self):
        self.user = User()
        self.current_delivering_orders = []

    def setUser(self):
        db = dataAdapter(database_path)
        self.user = db.getUser(3)
        db.close()

    def getReadyOrders(self):
        db = dataAdapter(database_path)
        orders = db.getReadyOrders()
        db.close()
        return orders

    def pickupOrder(self, order_id):
        db = dataAdapter(database_path)
        order = db.getOrder(order_id)
        order.status = "delivering"
        order.deliver_id = self.user.user_id
        self.current_delivering_orders.append(order_id)
        db.updateOrder(order)
        db.close()

    def completeOrder(self, order_id):
        db = dataAdapter(database_path)
        order = db.getOrder(order_id)
        order.status = "delivered"
        db.updateOrder(order)
        db.close()
        self.current_delivering_orders.remove(order_id)
    
    def getDeliveredOrdersByDeliver(self):
        db = dataAdapter(database_path)
        orders = db.getDeliveredOrdersByDeliver(self.user.user_id)
        db.close()
        return orders

        

    
    


def showOrdersByRestaurant(controller):    
    pendingOrders = controller.getPendingOrders()
    print("--------------------------")
    print("Pending Orders:")
    for order in pendingOrders:
        print(f"{order.order_id}: {order.order_date} - {order.customer_id} - ${order.total_cost}")
    print("--------------------------")
    processingOrders = controller.getProcessingOrders()
    print("Processing Orders:")
    for order in processingOrders:
        print(f"{order.order_id}: {order.order_date} - {order.customer_id} - ${order.total_cost}")
    print("--------------------------")
    readyOrders = controller.getReadyOrders()
    print("Ready Orders:")
    for order in readyOrders:
        print(f"{order.order_id}: {order.order_date} - {order.customer_id} - ${order.total_cost}")

def showOrdersForDelivery(controller):
    readyOrders = controller.getReadyOrders()
    print("--------------------------")
    print("Ready Orders:")
    for order in readyOrders:
        print(f"{order.order_id}: {order.order_date} - {order.customer_id} - ${order.total_cost}")
    print("--------------------------")
    print("Delivering Orders:")
    for order_id in controller.current_delivering_orders:
        db = dataAdapter(database_path)
        order = db.getOrder(order_id)
        db.close()
        print(f"{order.order_id}: {order.order_date} - {order.customer_id} - ${order.total_cost}")
    print("--------------------------")
    print("Delivered Orders:")
    deliveredOrders = controller.getDeliveredOrdersByDeliver()
    for order in deliveredOrders:
        print(f"{order.order_id}: {order.order_date} - {order.customer_id} - ${order.total_cost}")
    print("--------------------------")



if __name__ == "__main__":
    # Assume Login is successful
    print("Welcome to Food Delivery App!")
    print("Choose one of the following:")
    print("1. Register")
    print("2. Login")
    print("3. Testing User Types")
    accountController = accountController()
    choice = input("Please enter your choice: ")
    if choice == "1":
        username = input("Please enter your username: ")
        password = input("Please enter your password: ")
        first_name = input("Please enter your first name: ")
        last_name = input("Please enter your last name: ")
        email = input("Please enter your email: ")
        user_type = input("Please enter your user type (customer, owner, deliver): ")
        accountController.register(username, password, first_name, last_name, email, user_type)
        print("You are registered successfully!")
    elif choice == "2":
        username = input("Please enter your username: ")
        password = input("Please enter your password: ")
        if accountController.login(username, password):
            print("You are logged in successfully!")
        else:
            print("Login failed!")
            exit(0)
    elif choice == "3":
        print("Login As:")
        print("1. Customer")
        print("2. Owner")
        print("3. Deliver")
        user_type = input("Please enter the user type: ")
        if user_type == "1":
            print("CUSTOMER USE CASE")
            print("--------------------------")
            customerController = customerController()
            customerController.setUser()
            while (True):

                
                print("Here are the restaurants:")
                restaurants = customerController.getRestaurants()
                for restaurant in restaurants:
                    print(f"{restaurant.restaurant_id}: {restaurant.name}")
                restaurant_id = input("Please enter the restaurant ID: ")
                customerController.pickRestaurant(restaurant_id)
                restaurant = customerController.getRestaurant(restaurant_id)
                print(f"{restaurant.name}: {restaurant.description}")
                foods = customerController.getFoodsByRestaurant(restaurant_id)
                for food in foods:
                    print(f"{food.food_id}: {food.name} - ${food.price}")
                while (input("Do you want to order more? (y/n): ") == "y"):
                    food_id = input("Please enter the food ID: ")
                    quantity = int(input("Please enter the quantity: "))
                    customerController.addToCart(food_id, quantity)
                    customerController.showCart()
                input("Press Enter to checkout")
                customerController.checkout()
                print("--------------------------")

        
        elif user_type == "2":
            print("OWNER USE CASE")
            print("--------------------------")
            ownerController = ownerController()
            ownerController.setUser()
            ownerController.setRestaurant()
            while (True):
                
                showOrdersByRestaurant(ownerController)
                
                # processing the order
                order_id = input("Please enter the order ID to process: ")
                ownerController.processOrder(order_id)
                showOrdersByRestaurant(ownerController)

                # Completing the order
                order_id = input("Please enter the order ID to mark Ready: ")
                ownerController.completeOrder(order_id)
                showOrdersByRestaurant(ownerController)

        elif user_type == "3":
            print("DELIVER USE CASE")
            print("--------------------------")
            deliverController = deliverController()
            deliverController.setUser()
            while (True):
                
                showOrdersForDelivery(deliverController)
                while (input("Do you want to pickup an order? (y/n): ") == "y"):
                    order_id = input("Please enter the order ID to pickup: ")
                    deliverController.pickupOrder(order_id)
                    showOrdersForDelivery(deliverController)
                while (input("Do you want to complete an order? (y/n): ") == "y"):
                    order_id = input("Please enter the order ID to complete: ")
                    deliverController.completeOrder(order_id)
                    showOrdersForDelivery(deliverController)
                print("--------------------------")
                print()




    




