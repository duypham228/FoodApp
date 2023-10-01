import sqlite3
from models import Address


class dataAdapter():
    def __init__(self, db):
        self.db = db
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()

    
    def saveAddress(self, address):
        self.cursor.execute("INSERT INTO addresses VALUES (?,?,?,?,?)", (address.address_id, address.street, address.city, address.state, address.zip))
        self.conn.commit()
    
    def getAddress(self, address_id):
        self.cursor.execute("SELECT * FROM addresses WHERE address_id=?", (address_id,))
        row = self.cursor.fetchone()
        return Address(row[0], row[1], row[2], row[3], row[4])
    



# TESTING DATA ADAPTER

dataAdapter = dataAdapter("food.db")


dataAdapter.saveAddress(Address(1, "123 Main St", "New York", "NY", "10001"))