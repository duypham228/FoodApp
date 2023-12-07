# from dataAdapter import dataAdapter
from mongoAdapter import mongoAdapter
from models import Order, OrderLine, Food, Restaurant, User, Address, CreditCard
from datetime import datetime

database_path = "database/food.db"


class customerController:
    # def __init__(cls):
    user = User()
    order = Order()
    restaurant = Restaurant()

    # Assume Login is successful
    @classmethod
    def setUser(cls, current_user):
        cls.user = current_user

    @classmethod
    def getRestaurants(cls):
        db = mongoAdapter()
        restaurants = db.getAllRestaurants()
        db.close()
        restaurants = [restaurant for restaurant in restaurants if restaurant is not None]

        return restaurants
    
    @classmethod
    def getRestaurant(cls, restaurant_id):
        db = mongoAdapter()
        restaurant = db.getRestaurant(restaurant_id)
        db.close()
        return restaurant
    
    @classmethod
    def pickRestaurant(cls, restaurant_id):
        db = mongoAdapter()
        cls.restaurant = db.getRestaurant(restaurant_id)
        db.close()

    @classmethod
    def getFoods(cls):
        db = mongoAdapter()
        foods = db.getFoodByRestaurant(cls.restaurant.restaurant_id)
        db.close()
        return foods

    @classmethod
    def getFoodsByRestaurant(cls, restaurant_id):
        db = mongoAdapter()
        foods = db.getFoodByRestaurant(restaurant_id)
        db.close()
        return foods

    @classmethod
    def getFood(cls, food_id):
        db = mongoAdapter()
        food = db.getFood(food_id)
        db.close()
        return food

    @classmethod
    def addToCart(cls, food_id, quantity):
        db = mongoAdapter()
        food = cls.getFood(food_id)
        order_line = OrderLine(None, cls.order.order_id, food_id, food.name, quantity, float(food.price) * int(quantity))
        cls.order.order_list.append(order_line)
    
    @classmethod
    def removeFromCart(cls, food_id):
        for order_line in cls.cart:
            if order_line.food_id == food_id:
                cls.cart.remove(order_line)
    
    @classmethod
    def showCart(cls):
        for order_line in cls.order.order_list:
            print(f"{order_line.food_id}: {order_line.food_name} - {order_line.quantity} - ${order_line.price}")
    
    @classmethod
    def getCartTotal(cls):
        total = 0
        for order_line in cls.order.order_list:
            total += order_line.price * order_line.quantity
        return total

    @classmethod
    def addAddress(cls, street, city, state, zip_code):

        address = Address(None, street, city, state, zip_code)
        db = mongoAdapter()
        address_id = db.saveAddress(address)
        shipping_id = db.saveShipping(cls.user.user_id, address_id)
        db.close()
        return address_id

    @classmethod
    def addPayment(cls, card_number, card_holder, expiration_date, security_code):
        db = mongoAdapter()
        credit_card = CreditCard(None, card_number, card_holder, expiration_date, security_code)
        credit_card_id = db.saveCreditCard(credit_card)
        payment_id = db.savePayment(cls.user.user_id, credit_card_id)
        db.close()
        return credit_card_id
    
    @classmethod
    def getAddresses(cls):
        db = mongoAdapter()
        addresses = db.getShippingAddresses(cls.user.user_id)
        db.close()
        return addresses

    @classmethod
    def getPayments(cls):
        db = mongoAdapter()
        payments = db.getPaymentCards(cls.user.user_id)
        db.close()
        return payments

        
    @classmethod
    def checkout(cls, address_id, credit_card_id):
        db = mongoAdapter()
        cls.order.order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cls.order.customer_id = cls.user.user_id
        cls.order.restaurant_id = cls.restaurant.restaurant_id
        cls.order.total_cost = 0
        for order_line in cls.order.order_list:
            cls.order.total_cost += int(order_line.price)
        cls.order.status = "pending"
        # cls.order.address_id = int(address_id)
        cls.order.credit_card_id = int(credit_card_id)

        # Remember to update status of order after delivery
        order_id = db.saveOrder(cls.order)
        db.close()
        cls.order.order_id = order_id
        cls.order = Order()

class ownerController:
    # def __init__(cls):
    user = User()
    restaurant = Restaurant()


    # Assume Login is successful
    @classmethod
    def setUser(cls, current_user):
        db = mongoAdapter()
        cls.user = current_user

    @classmethod
    def setRestaurant(cls, restaurant_id):
        db = mongoAdapter()
        cls.restaurant = db.getRestaurant(restaurant_id)
        db.close()

    @classmethod
    def addRestaurant(cls, name, phone_number, email, description, street, city, state, zipcode):
        db = mongoAdapter()
        address = Address(None, street, city, state, zipcode)
        address_id = db.saveAddress(address)
        restaurant = Restaurant(None, name, address_id, phone_number, email, description)
        restaurant_id = db.saveRestaurant(restaurant)
        db.saveOwnership(cls.user.user_id, restaurant_id)
        db.close()
        return restaurant
    
    @classmethod
    def getRestaurantAddress(cls):
        db = mongoAdapter()
        return db.getAddress(cls.restaurant.address_id)

    @classmethod
    def getFoods(cls):
        db = mongoAdapter()
        foods = db.getFoodByRestaurant(cls.restaurant.restaurant_id)
        db.close()
        return foods

    @classmethod
    def addFood(cls, name, price, description):
        db = mongoAdapter()
        food = Food(None, name, cls.restaurant.restaurant_id, price, description)
        db.saveFood(food)
        db.close()


    @classmethod
    def getRestaurants(cls):
        db = mongoAdapter()
        restaurants = db.getRestaurantsByOwner(cls.user.user_id)
        db.close()
        return restaurants

    @classmethod
    def getOrders(cls):
        db = mongoAdapter()
        orders = db.getOrdersByRestaurant(cls.restaurant.restaurant_id)
        db.close()
        return orders
    
    @classmethod
    def getOrderById(cls, order_id):
        db = mongoAdapter()
        order = db.getOrder(order_id)
        db.close()
        return order

    @classmethod
    def getPendingOrders(cls):
        db = mongoAdapter()
        orders = db.getPendingOrdersByRestaurant(cls.restaurant.restaurant_id)
        db.close()
        return orders
    
    @classmethod
    def getProcessingOrders(cls):
        db = mongoAdapter()
        orders = db.getProcessingOrdersByRestaurant(cls.restaurant.restaurant_id)
        db.close()
        return orders

    @classmethod
    def getReadyOrders(cls):
        db = mongoAdapter()
        orders = db.getReadyOrdersByRestaurant(cls.restaurant.restaurant_id)
        db.close()
        return orders
    
    @classmethod
    def processOrder(cls, order_id):
        db = mongoAdapter()
        order = db.getOrder(order_id)
        order.status = "processing"
        db.updateOrder(order)
        db.close()
    
    @classmethod
    def completeOrder(cls, order_id):
        db = mongoAdapter()
        order = db.getOrder(order_id)
        order.status = "ready"
        db.updateOrder(order)
        db.close()

    @classmethod
    def getCustomerById(cls, customer_id):
        db = mongoAdapter()
        customer = db.getUser(customer_id)
        db.close()
        return customer

    @classmethod
    def getFoodByRestaurant(cls, restaurant_id):
        db = mongoAdapter()
        foods = db.getFoodByRestaurant(restaurant_id)
        db.close()
        return foods
    
class deliverController:
    # def __init__(cls):
    user = User()

    @classmethod
    def setUser(cls, current_user):
        cls.user = current_user

    @classmethod
    def getReadyOrders(cls):
        db = mongoAdapter()
        orders = db.getReadyOrders()
        db.close()
        return orders
    

    @classmethod
    def getCustomerById(cls, customer_id):
        db = mongoAdapter()
        customer = db.getUser(customer_id)
        db.close()
        return customer
    
    @classmethod
    def getOrderById(cls, order_id):
        db = mongoAdapter()
        order = db.getOrder(order_id)
        db.close()
        return order

    @classmethod
    def pickupOrder(cls, order_id):
        db = mongoAdapter()
        order = db.getOrder(order_id)
        order.status = "delivering"
        order.deliver_id = cls.user.user_id
        db.updateOrder(order)
        db.close()

    @classmethod
    def completeOrder(cls, order_id):
        db = mongoAdapter()
        order = db.getOrder(order_id)
        order.status = "delivered"
        db.updateOrder(order)
        db.close()

    @classmethod
    def getDeliveringOrders(cls):
        db = mongoAdapter()
        orders = db.getDeliveringOrdersByDeliver(cls.user.user_id)
        db.close()
        return orders
    
    @classmethod
    def getDeliveredOrders(cls):
        db = mongoAdapter()
        orders = db.getDeliveredOrdersByDeliver(cls.user.user_id)
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
        db = mongoAdapter()
        order = db.getOrder(order_id)
        db.close()
        print(f"{order.order_id}: {order.order_date} - {order.customer_id} - ${order.total_cost}")
    print("--------------------------")
    print("Delivered Orders:")
    deliveredOrders = controller.getDeliveredOrdersByDeliver()
    for order in deliveredOrders:
        print(f"{order.order_id}: {order.order_date} - {order.customer_id} - ${order.total_cost}")
    print("--------------------------")



# if __name__ == "__main__":
#     # Assume Login is successful
#     print("Welcome to Food Delivery App!")
#     print("Choose one of the following:")
#     print("1. Register")
#     print("2. Login")
#     print("3. Testing User Types")
#     accountController = accountController()
#     choice = input("Please enter your choice: ")
#     if choice == "1":
#         username = input("Please enter your username: ")
#         password = input("Please enter your password: ")
#         first_name = input("Please enter your first name: ")
#         last_name = input("Please enter your last name: ")
#         email = input("Please enter your email: ")
#         user_type = input("Please enter your user type (customer, owner, deliver): ")
#         accountController.register(username, password, first_name, last_name, email, user_type)
#         print("You are registered successfully!")
#     elif choice == "2":
#         username = input("Please enter your username: ")
#         password = input("Please enter your password: ")
#         if accountController.login(username, password):
#             print("You are logged in successfully!")
#         else:
#             print("Login failed!")
#             exit(0)
#     elif choice == "3":
#         print("Login As:")
#         print("1. Customer")
#         print("2. Owner")
#         print("3. Deliver")
#         user_type = input("Please enter the user type: ")
#         if user_type == "1":
#             print("CUSTOMER USE CASE")
#             print("--------------------------")
#             customerController = customerController()
#             customerController.setUser()
#             while (True):

                
#                 print("Here are the restaurants:")
#                 restaurants = customerController.getRestaurants()
#                 for restaurant in restaurants:
#                     print(f"{restaurant.restaurant_id}: {restaurant.name}")
#                 restaurant_id = input("Please enter the restaurant ID: ")
#                 customerController.pickRestaurant(restaurant_id)
#                 restaurant = customerController.getRestaurant(restaurant_id)
#                 print(f"{restaurant.name}: {restaurant.description}")
#                 foods = customerController.getFoodsByRestaurant(restaurant_id)
#                 for food in foods:
#                     print(f"{food.food_id}: {food.name} - ${food.price}")
#                 while (input("Do you want to order more? (y/n): ") == "y"):
#                     food_id = input("Please enter the food ID: ")
#                     quantity = int(input("Please enter the quantity: "))
#                     customerController.addToCart(food_id, quantity)
#                     customerController.showCart()
#                 input("Press Enter to checkout")
#                 customerController.checkout()
#                 print("--------------------------")

        
#         elif user_type == "2":
#             print("OWNER USE CASE")
#             print("--------------------------")
#             ownerController = ownerController()
#             ownerController.setUser()
#             ownerController.setRestaurant()
#             while (True):
                
#                 showOrdersByRestaurant(ownerController)
                
#                 # processing the order
#                 order_id = input("Please enter the order ID to process: ")
#                 ownerController.processOrder(order_id)
#                 showOrdersByRestaurant(ownerController)

#                 # Completing the order
#                 order_id = input("Please enter the order ID to mark Ready: ")
#                 ownerController.completeOrder(order_id)
#                 showOrdersByRestaurant(ownerController)

#         elif user_type == "3":
#             print("DELIVER USE CASE")
#             print("--------------------------")
#             deliverController = deliverController()
#             deliverController.setUser()
#             while (True):
                
#                 showOrdersForDelivery(deliverController)
#                 while (input("Do you want to pickup an order? (y/n): ") == "y"):
#                     order_id = input("Please enter the order ID to pickup: ")
#                     deliverController.pickupOrder(order_id)
#                     showOrdersForDelivery(deliverController)
#                 while (input("Do you want to complete an order? (y/n): ") == "y"):
#                     order_id = input("Please enter the order ID to complete: ")
#                     deliverController.completeOrder(order_id)
#                     showOrdersForDelivery(deliverController)
#                 print("--------------------------")
#                 print()




    




