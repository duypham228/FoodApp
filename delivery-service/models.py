class Address():
    def __init__(self, address_id ,street, city, state, zip):
        self.address_id = address_id
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip

    def __str__(self):
        return f"{self.address_id}, {self.street}, {self.city}, {self.state}, {self.zip}"

    def __repr__(self):
        return f"{self.address_id}, {self.street}, {self.city}, {self.state}, {self.zip}"
    

class User():
    def __init__(self, user_id=None ,username=None, password=None, first_name=None, last_name=None, email=None, user_type=None):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.user_type = user_type

    def __str__(self):
        return f"{self.user_id}, {self.username}, {self.password}, {self.first_name}, {self.last_name}, {self.email}, {self.user_type}"

    def __repr__(self):
        return f"{self.user_id}, {self.username}, {self.password}, {self.first_name}, {self.last_name}, {self.email}, {self.user_type}"
    
    
    
class Restaurant():
    def __init__(self, restaurant_id=None, name=None, address_id=None, phone_number=None, email=None, description=None):
        self.restaurant_id = restaurant_id
        self.name = name
        self.address_id = address_id
        self.phone_number = phone_number
        self.email = email
        self.description = description


    def __str__(self):
        return f"{self.restaurant_id}, {self.name}, {self.address_id}, {self.phone_number}, {self.email}, {self.description}"

    def __repr__(self):
        return f"{self.restaurant_id}, {self.name}, {self.address_id}, {self.phone_number}, {self.email}, {self.description}"
    

class Food():
    def __init__(self, food_id, name, restaurant_id, price, description):
        self.food_id = food_id
        self.name = name
        self.restaurant_id = restaurant_id
        self.price = price
        self.description = description

    def __str__(self):
        return f"{self.food_id}, {self.name}, {self.restaurant_id}, {self.price}, {self.description}"

    def __repr__(self):
        return f"{self.food_id}, {self.name}, {self.restaurant_id}, {self.price}, {self.description}"
    
    
class Order():
    def __init__(self, order_id=None, order_date=None, customer_id=None, restaurant_id=None, total_cost=None, deliver_id=None, credit_card_id=None, status=None):
        self.order_list = []
        self.order_id = order_id
        self.order_date = order_date
        self.customer_id = customer_id
        self.restaurant_id = restaurant_id
        self.total_cost = total_cost
        self.deliver_id = deliver_id
        self.credit_card_id = credit_card_id
        self.status = status
    

    def __str__(self):
        return f"{self.order_id}, {self.order_date}, {self.customer_id}, {self.restaurant_id}, {self.deliver_id}, {self.total_cost}, {self.credit_card_id}, {self.status}"
    
    def __repr__(self):
        return f"{self.order_id}, {self.order_date}, {self.customer_id}, {self.restaurant_id}, {self.deliver_id}, {self.total_cost}, {self.credit_card_id}, {self.status}"
    

class OrderLine():
    def __init__(self, order_line_id=None, order_id=None, food_id=None, food_name=None, quantity=None, price=None):
        self.order_line_id = order_line_id
        self.order_id = order_id
        self.food_id = food_id
        self.food_name = food_name
        self.quantity = quantity
        self.price = price
    
    def __str__(self):
        return f"{self.order_line_id}, {self.order_id}, {self.food_id}, {self.food_name}, {self.quantity}, {self.price}"
    
    def __repr__(self):
        return f"{self.order_line_id}, {self.order_id}, {self.food_id}, {self.food_name}, {self.quantity}, {self.price}"
    
    
class CreditCard():
    def __init__(self, credit_card_id, card_number, holder_name, expiration_date, CVV):
        self.credit_card_id = credit_card_id
        self.card_number = card_number
        self.holder_name = holder_name
        self.expiration_date = expiration_date
        self.CVV = CVV
    
    def __str__(self):
        return f"{self.credit_card_id}, {self.card_number}, {self.holder_name}, {self.expiration_date}, {self.CVV}"
    
    def __repr__(self):
        return f"{self.credit_card_id}, {self.card_number}, {self.holder_name}, {self.expiration_date}, {self.CVV}"
    
    
