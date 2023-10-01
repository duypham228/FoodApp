import sqlite3

class dataAdapter():
    def __init__(self, db):
        self.db = db
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()

dataAdapter = dataAdapter("food.db")