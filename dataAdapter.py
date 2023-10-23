import sqlite3
from models import Address, User, Restaurant, Food, Order, OrderLine, CreditCard


class dataAdapter():
    def __init__(self, db):
        self.db = db
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.close()

    def saveAddress(self, address):
        self.cursor.execute("INSERT INTO addresses (address_id, street, city, state, zip) VALUES (?,?,?,?,?)",
                            (address.address_id, address.street, address.city, address.state, address.zip))
        address_id = self.cursor.lastrowid
        self.conn.commit()
        return address_id

    def getAddress(self, address_id):
        self.cursor.execute(
            "SELECT * FROM addresses WHERE address_id=?", (address_id,))
        row = self.cursor.fetchone()
        if row:
            return Address(row[0], row[1], row[2], row[3], row[4])
        return None

    def deleteAddress(self, address_id):
        self.cursor.execute(
            "DELETE FROM addresses WHERE address_id=?", (address_id,))
        self.conn.commit()

    def saveShipping(self, customer_id, address_id):
        self.cursor.execute("INSERT INTO shipping (customer_id, address_id) VALUES (?,?)",
                            (customer_id, address_id))
        shipping_id = self.cursor.lastrowid
        self.conn.commit()
        return shipping_id

    def saveUser(self, user):
        self.cursor.execute("INSERT INTO users (user_id, username, password, first_name, last_name, email, user_type) VALUES (?,?,?,?,?,?,?)",
                            (user.user_id, user.username, user.password, user.first_name, user.last_name, user.email, user.user_type))
        self.conn.commit()

    def getUser(self, user_id):
        self.cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
        row = self.cursor.fetchone()
        if row:
            return User(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
        return None

    def getUserByUsername(self, username):
        self.cursor.execute(
            "SELECT * FROM users WHERE username=?", (username,))
        row = self.cursor.fetchone()
        if row:
            return User(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
        return None

    def deleteUser(self, user_id):
        self.cursor.execute("DELETE FROM users WHERE user_id=?", (user_id,))
        self.conn.commit()

    def saveCreditCard(self, credit_card):
        self.cursor.execute("INSERT INTO creditcards (card_number, holder_name, expiration_date, CVV) VALUES (?,?,?,?)",
                            (credit_card.card_number, credit_card.holder_name, credit_card.expiration_date, credit_card.CVV))
        credit_card_id = self.cursor.lastrowid
        self.conn.commit()
        return credit_card_id

    def savePayment(self, user_id, credit_card_id):
        self.cursor.execute("INSERT INTO payments (user_id, credit_card_id) VALUES (?,?)",
                            (user_id, credit_card_id))
        payment_id = self.cursor.lastrowid
        self.conn.commit()
        return payment_id

    def saveRestaurant(self, restaurant):
        self.cursor.execute("INSERT INTO restaurants (restaurant_id, name, address_id, phone_number, email, description) VALUES (?,?,?,?,?,?)", (
            restaurant.restaurant_id, restaurant.name, restaurant.address_id, restaurant.phone_number, restaurant.email, restaurant.description))
        self.conn.commit()

    def getRestaurant(self, restaurant_id):
        self.cursor.execute(
            "SELECT * FROM restaurants WHERE restaurant_id=?", (restaurant_id,))
        row = self.cursor.fetchone()
        if row:
            return Restaurant(row[0], row[1], row[2], row[3], row[4], row[5])
        return None

    def getAllRestaurants(self):
        self.cursor.execute("SELECT * FROM restaurants")
        rows = self.cursor.fetchall()
        restaurants = []
        for row in rows:
            restaurants.append(Restaurant(
                row[0], row[1], row[2], row[3], row[4], row[5]))
        return restaurants

    def deleteRestaurant(self, restaurant_id):
        self.cursor.execute(
            "DELETE FROM restaurants WHERE restaurant_id=?", (restaurant_id,))
        self.conn.commit()

    def saveFood(self, food):
        self.cursor.execute("INSERT INTO foods (food_id, name, restaurant_id, price, description) VALUES (?,?,?,?,?)",
                            (food.food_id, food.name, food.restaurant_id, food.price, food.description))
        self.conn.commit()

    def getFood(self, food_id):
        self.cursor.execute("SELECT * FROM foods WHERE food_id=?", (food_id,))
        row = self.cursor.fetchone()
        if row:
            return Food(row[0], row[1], row[2], row[3], row[4])
        return None
    
    def getTotalFoods(self):
        self.cursor.execute("SELECT COUNT(*) FROM foods")
        row = self.cursor.fetchone()
        if row:
            return row[0]
        return 0

    def deleteFood(self, food_id):
        self.cursor.execute("DELETE FROM foods WHERE food_id=?", (food_id,))
        self.conn.commit()
    
    def getFoodByRestaurant(self, restaurant_id):
        self.cursor.execute("SELECT * FROM foods WHERE restaurant_id=?", (restaurant_id,))
        rows = self.cursor.fetchall()
        foods = []
        for row in rows:
            foods.append(Food(row[0], row[1], row[2], row[3], row[4]))
        return foods

    def saveOrder(self, order):
        order_list = order.get_order_list()
        self.cursor.execute("INSERT INTO orders (order_date, customer_id, restaurant_id, deliver_id, total_cost, status) VALUES (?,?,?,?,?,?)",
                            (order.order_date, order.customer_id, order.restaurant_id, order.deliver_id, order.total_cost, order.status))
        order_id = self.cursor.lastrowid
        for order_line in order_list:
            self.cursor.execute("INSERT INTO OrderLines (order_id, food_id, quantity, price) VALUES (?,?,?,?)", (
                order_id, order_line.food_id, order_line.quantity, order_line.price))
        
        self.conn.commit()
        return order_id
    
    def updateOrder(self, order):
        self.cursor.execute("UPDATE orders SET order_date=?, customer_id=?, restaurant_id=?, deliver_id=?, total_cost=?, status=? WHERE order_id=?",
                            (order.order_date, order.customer_id, order.restaurant_id, order.deliver_id, order.total_cost, order.status, order.order_id))
        
        self.conn.commit()
    
    def getOrder(self, order_id):
        self.cursor.execute("SELECT * FROM orders WHERE order_id=?", (order_id,))
        row = self.cursor.fetchone()
        if row:
            return Order(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        return None
    
    def getPendingOrdersByRestaurant(self, restaurant_id):
        self.cursor.execute("SELECT * FROM orders WHERE restaurant_id=? AND status='pending'", (restaurant_id,))
        rows = self.cursor.fetchall()
        orders = []
        for row in rows:
            orders.append(Order(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
        return orders
    
    def getProcessingOrdersByRestaurant(self, restaurant_id):
        self.cursor.execute("SELECT * FROM orders WHERE restaurant_id=? AND status='processing'", (restaurant_id,))
        rows = self.cursor.fetchall()
        orders = []
        for row in rows:
            orders.append(Order(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
        return orders

    def getReadyOrdersByRestaurant(self, restaurant_id):
        self.cursor.execute("SELECT * FROM orders WHERE restaurant_id=? AND status='ready'", (restaurant_id,))
        rows = self.cursor.fetchall()
        orders = []
        for row in rows:
            orders.append(Order(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
        return orders
    
    def getReadyOrders(self):
        self.cursor.execute("SELECT * FROM orders WHERE status='ready'")
        rows = self.cursor.fetchall()
        orders = []
        for row in rows:
            orders.append(Order(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
        return orders
    
    def getDeliveredOrdersByDeliver(self, deliver_id):
        self.cursor.execute("SELECT * FROM orders WHERE deliver_id=? AND status='delivered'", (deliver_id,))
        rows = self.cursor.fetchall()
        orders = []
        for row in rows:
            orders.append(Order(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
        return orders
    
    
    


# TESTING DATA ADAPTER

# dataAdapter = dataAdapter("food.db")

# # dataAdapter.saveAddress(Address(None, "123 Main St", "New York", "NY", "10001"))
# # dataAdapter.saveUser(User(None, "johndoe", "password", "John", "Doe", "johndoe@gmail.com", "customer"))
# # dataAdapter.saveUser(User(None, "bobbytables", "password", "Bobby", "Tables", "", "owner"))
# # dataAdapter.saveUser(User(None, "davidsmith", "password", "David", "Smith", "", "deliver"))
# # dataAdapter.saveRestaurant(Restaurant(None, "McDonalds", 1, "123-456-7890", "", "Fast Food"))
# # dataAdapter.saveFood(Food(None, "Big Mac", 1, 3.99, "Most popular burger"))


# address = dataAdapter.getAddress(1)
# user = dataAdapter.getUser(1)
# restaurant = dataAdapter.getRestaurant(1)
# food = dataAdapter.getFood(1)

# print(address)
# print(user)
# print(restaurant)
# print(food)


# dataAdapter.close()
