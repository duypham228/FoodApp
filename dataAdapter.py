import sqlite3
from models import Address, User, Restaurant


class dataAdapter():
    def __init__(self, db):
        self.db = db
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()
    
    def close(self):
        self.conn.close()

    
    def saveAddress(self, address):
        self.cursor.execute("INSERT INTO addresses (street, city, state, zip) VALUES (?,?,?,?)", (address.street, address.city, address.state, address.zip))
        self.conn.commit()
    
    def getAddress(self, address_id):
        self.cursor.execute("SELECT * FROM addresses WHERE address_id=?", (address_id,))
        row = self.cursor.fetchone()
        return Address(row[0], row[1], row[2], row[3], row[4])
    
    def deleteAddress(self, address_id):
        self.cursor.execute("DELETE FROM addresses WHERE address_id=?", (address_id,))
        self.conn.commit()
    
    def saveUser(self, user):
        self.cursor.execute("INSERT INTO users (username, password, first_name, last_name, email, user_type) VALUES (?,?,?,?,?,?)", (user.username, user.password, user.first_name, user.last_name, user.email, user.user_type))
        self.conn.commit()

    def getUser(self, user_id):
        self.cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
        row = self.cursor.fetchone()
        return User(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
    
    def deleteUser(self, user_id):
        self.cursor.execute("DELETE FROM users WHERE user_id=?", (user_id,))
        self.conn.commit()

    def saveRestaurant(self, restaurant):
        self.cursor.execute("INSERT INTO restaurants (name, address_id, phone_number, email, description) VALUES (?,?,?,?,?)", (restaurant.name, restaurant.address_id, restaurant.phone_number, restaurant.email, restaurant.description))
        self.conn.commit()

    def getRestaurant(self, restaurant_id):
        self.cursor.execute("SELECT * FROM restaurants WHERE restaurant_id=?", (restaurant_id,))
        row = self.cursor.fetchone()
        return Restaurant(row[0], row[1], row[2], row[3], row[4], row[5])
    
    



# TESTING DATA ADAPTER

dataAdapter = dataAdapter("food.db")

# dataAdapter.saveAddress(Address(None, "123 Main St", "New York", "NY", "10001"))
# dataAdapter.saveUser(User(None, "johndoe", "password", "John", "Doe", "johndoe@gmail.com", "customer"))
# dataAdapter.saveRestaurant(Restaurant(None, "McDonalds", 1, "123-456-7890", "", "Fast Food"))

# address = dataAdapter.getAddress(1)
# user = dataAdapter.getUser(1)
restaurant = dataAdapter.getRestaurant(1)

print(restaurant)


dataAdapter.close()
