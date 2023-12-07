from redisAdapter import redisAdapter
from models import Order, OrderLine, Food, Restaurant, User, Address, CreditCard
from datetime import datetime

redis_db = redisAdapter()

class accountController:
    # def __init__(cls):
    #     pass
    @classmethod
    def register(cls, username, password, first_name, last_name, email, user_type):
        user = User(None, username, password, first_name, last_name, email, user_type)
        redis_db.saveUser(user)
        return user
    @classmethod
    def login(cls, username, password):
        user = redis_db.getUserByUsername(username)
        if user is not None and user.password == password:
            return user
        return None
    
    @classmethod
    def getUserByUsername(cls, username):
        user = redis_db.getUserByUsername(username)
        return user
    

