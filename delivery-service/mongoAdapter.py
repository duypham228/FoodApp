import sqlite3
import pymongo
import certifi
from models import Address, User, Restaurant, Food, Order, OrderLine, CreditCard

def custom_unpack(input_dict, exclude_key="_id"):
    return {k: v for k, v in input_dict.items() if k != exclude_key}

class mongoAdapter:
    def __init__(self, database_name="food"):
        uri = "mongodb+srv://duypham228:test123@cluster0.au3p8q2.mongodb.net/?retryWrites=true&w=majority"

        self.client = pymongo.MongoClient(uri, tlsCAFile=certifi.where())
        self.database = self.client[database_name]

    def createCollection(self, collection_name):
        self.database.create_collection(collection_name)


    def getCollection(self, collection_name):
        return self.database[collection_name]

    def saveAddress(self, address):
        collection = self.getCollection("Addresses")
        address_id = collection.count_documents({}) + 1
        address.address_id = address_id
        collection.insert_one(address.__dict__)
        return address_id

    def getAddress(self, address_id):
        collection = self.getCollection("Addresses")
        return collection.find_one({"address_id": int(address_id)})

    def deleteAddress(self, address_id):
        collection = self.getCollection("Addresses")
        collection.delete_one({"address_id": int(address_id)})
    
    def saveShipping(self, customer_id, address_id):
        collection = self.getCollection("Shipping")
        shipping_id = collection.count_documents({}) + 1
        collection.insert_one({"shipping_id": int(shipping_id), "customer_id": int(customer_id), "address_id": int(address_id)})
        return shipping_id
    
    def getShippingAddresses(self, customer_id):
        shipping = self.getCollection("Shipping")
        addresses = self.getCollection("Addresses")
        documents = shipping.find({"customer_id": int(customer_id)})
        address_ids = [document["address_id"] for document in documents]
        address_list = []
        for address_id in address_ids:
            address_doc = addresses.find_one({"address_id": int(address_id)})
            if address_doc is not None:
                address = Address(**custom_unpack(address_doc))
                address_list.append(address)
        return address_list

    def getPaymentCards(self, customer_id):
        payments = self.getCollection("Payments")
        credit_cards = self.getCollection("CreditCards")
        documents = payments.find({"user_id": int(customer_id)})
        credit_card_ids = [document["credit_card_id"] for document in documents]
        credit_card_list = []
        for credit_card_id in credit_card_ids:
            credit_card_doc = credit_cards.find_one({"credit_card_id": int(credit_card_id)})
            if credit_card_doc is not None:
                credit_card = CreditCard(**custom_unpack(credit_card_doc))
                credit_card_list.append(credit_card)
        return credit_card_list

    def saveOwnership(self, user_id, restaurant_id):
        collection = self.getCollection("Ownerships")
        ownership_id = collection.count_documents({}) + 1
        collection.insert_one({"ownership_id": int(ownership_id), "owner_id": int(user_id), "restaurant_id": int(restaurant_id)})
        return ownership_id

    def saveCreditCard(self, credit_card):
        collection = self.getCollection("CreditCards")
        credit_card_id = collection.count_documents({}) + 1
        credit_card.credit_card_id = int(credit_card_id)
        collection.insert_one(credit_card.__dict__)
        return int(credit_card_id)

    def savePayment(self, user_id, credit_card_id):
        collection = self.getCollection("Payments")
        payment_id = collection.count_documents({}) + 1
        collection.insert_one({"payment_id": int(payment_id), "user_id": int(user_id), "credit_card_id": int(credit_card_id)})
        return int(payment_id)

    def saveRestaurant(self, restaurant):
        collection = self.getCollection("Restaurants")
        restaurant_id = collection.count_documents({}) + 1
        restaurant.restaurant_id = int(restaurant_id)
        collection.insert_one(restaurant.__dict__)
        return int(restaurant_id)
    
    def getRestaurantsByOwner(self, owner_id):
        restaurants = self.getCollection("Restaurants")
        ownerships = self.getCollection("Ownerships")
        documents = ownerships.find({"owner_id": int(owner_id)})
        restaurant_ids = [document["restaurant_id"] for document in documents]
        restaurant_list = []
        for restaurant_id in restaurant_ids:
            restaurant_doc = restaurants.find_one({"restaurant_id": int(restaurant_id)})
            restaurant = Restaurant(**custom_unpack(restaurant_doc))
            restaurant_list.append(restaurant)
        return restaurant_list

    def getRestaurant(self, restaurant_id):
        collection = self.getCollection("Restaurants")
        document = collection.find_one({"restaurant_id": int(restaurant_id)})
        print(document)
        return Restaurant(**custom_unpack(document))

    def getAllRestaurants(self):
        collection = self.getCollection("Restaurants")
        restaurants = []
        for restaurant_doc in collection.find():
            restaurant = Restaurant(**custom_unpack(restaurant_doc))
            print(restaurant)
            print(type(restaurant))
            if restaurant is not None:
                restaurants.append(restaurant)
        return restaurants

    def deleteRestaurant(self, restaurant_id):
        collection = self.getCollection("Restaurants")
        collection.delete_one({"restaurant_id": int(restaurant_id)})


    def saveFood(self, food):
        collection = self.getCollection("Foods")
        food_id = collection.count_documents({}) + 1
        food.food_id = food_id
        collection.insert_one(food.__dict__)
        return int(food_id)

    def getFood(self, food_id):
        collection = self.getCollection("Foods")
        document = collection.find_one({"food_id": int(food_id)})
        return Food(**custom_unpack(document))
    
    def getTotalFoods(self):
        collection = self.getCollection("Foods")
        return collection.count_documents({})

    def deleteFood(self, food_id):
        collection = self.getCollection("Foods")
        collection.delete_one({"food_id": int(food_id)})
    
    def getFoodByRestaurant(self, restaurant_id):
        collection = self.getCollection("Foods")
        foods = []
        for food_doc in collection.find({"restaurant_id": int(restaurant_id)}):
            food = Food(**custom_unpack(food_doc))
            foods.append(food)
        return foods

    def saveOrder(self, order):
        order_list = order.order_list
        collection = self.getCollection("Orders")
        order_id = collection.count_documents({}) + 1
        order.order_id = order_id
        order_doc = order.__dict__
        del order_doc["order_list"]
        collection.insert_one(order_doc)
        order_lines = self.getCollection("OrderLines")
        for order_line in order_list:
            order_line.order_id = order_id
            order_lines.insert_one(order_line.__dict__)
        return order_id

    
    def updateOrder(self, order):
        collection = self.getCollection("Orders")
        order_doc = order.__dict__
        del order_doc["order_list"]
        collection.update_one({"order_id": order.order_id}, {"$set": order.__dict__})

    
    def getOrder(self, order_id):
        collection = self.getCollection("Orders")
        order_doc = collection.find_one({"order_id": int(order_id)})
        order = Order(**custom_unpack(order_doc))
        order_lines = self.getCollection("OrderLines")
        order_lines_docs = order_lines.find({"order_id": int(order_id)})
        order_list = []
        for order_line_doc in order_lines_docs:
            order_line = OrderLine(**custom_unpack(order_line_doc))
            order_list.append(order_line)
        order.order_list = order_list
        return order

    
    def getPendingOrdersByRestaurant(self, restaurant_id):
        collection = self.getCollection("Orders")
        order_lines = self.getCollection("OrderLines")
        orders = []
        for order_doc in collection.find({"restaurant_id": int(restaurant_id), "status": "pending"}):
            order_lines_docs = order_lines.find({"order_id": int(order_doc["order_id"])})
            order_list = []
            for order_line_doc in order_lines_docs:
                order_line = OrderLine(**custom_unpack(order_line_doc))
                order_list.append(order_line)
            order = Order(**custom_unpack(order_doc))
            order.order_list = order_list
            orders.append(order)
        return orders

    
    def getProcessingOrdersByRestaurant(self, restaurant_id):
        collection = self.getCollection("Orders")
        orders = []
        for order_doc in collection.find({"restaurant_id": int(restaurant_id), "status": "processing"}):
            order = Order(**custom_unpack(order_doc))
            orders.append(order)
        return orders


    def getReadyOrdersByRestaurant(self, restaurant_id):
        collection = self.getCollection("Orders")
        orders = []
        for order_doc in collection.find({"restaurant_id": int(restaurant_id), "status": "ready"}):
            order = Order(**custom_unpack(order_doc))
            orders.append(order)
        return orders
    
    def getReadyOrders(self):
        collection = self.getCollection("Orders")
        orders = []
        for order_doc in collection.find({"status": "ready"}):
            order = Order(**custom_unpack(order_doc))
            orders.append(order)
        return orders

    
    def getDeliveringOrdersByDeliver(self, deliver_id):
        collection = self.getCollection("Orders")
        orders = []
        for order_doc in collection.find({"deliver_id": int(deliver_id), "status": "delivering"}):
            order = Order(**custom_unpack(order_doc))
            orders.append(order)
        return orders


    def getDeliveredOrdersByDeliver(self, deliver_id):
        collection = self.getCollection("Orders")
        orders = []
        for order_doc in collection.find({"deliver_id": int(deliver_id), "status": "delivered"}):
            order = Order(**custom_unpack(order_doc))
            orders.append(order)
        return orders

    def getFoodByRestaurant(self, restaurant_id):
        collection = self.getCollection("Foods")
        foods = []
        for food_doc in collection.find({"restaurant_id": int(restaurant_id)}):
            food = Food(**custom_unpack(food_doc))
            foods.append(food)
        return foods

    
    def close(self):
        self.client.close()

