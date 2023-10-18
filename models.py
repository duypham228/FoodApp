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
    
    # setters
    def set_address_id(self, address_id):
        self.address_id = address_id

    def set_street(self, street):
        self.street = street

    def set_city(self, city):
        self.city = city

    def set_state(self, state):
        self.state = state
    
    def set_zip(self, zip):
        self.zip = zip
    
    # getters
    def get_address_id(self):
        return self.address_id
    
    def get_street(self):
        return self.street
    
    def get_city(self):
        return self.city
    
    def get_state(self):
        return self.state
    
    def get_zip(self):
        return self.zip

class User():
    def __init__(self, user_id ,username, password, first_name, last_name, email, user_type):
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
    
    # setters
    def set_user_id(self, user_id):
        self.user_id = user_id

    def set_username(self, username):
        self.username = username

    def set_password(self, password):
        self.password = password

    def set_first_name(self, first_name):
        self.first_name = first_name
    
    def set_last_name(self, last_name):
        self.last_name = last_name
    
    def set_email(self, email):
        self.email = email

    def set_user_type(self, user_type):
        self.user_type = user_type
    
    
    
    # getters
    def get_user_id(self):
        return self.user_id
    
    def get_username(self):
        return self.username
    
    def get_password(self):
        return self.password
    
    def get_first_name(self):
        return self.first_name
    
    def get_last_name(self):
        return self.last_name
    
    def get_email(self):
        return self.email
    
    def get_user_type(self):
        return self.user_type
    
class Restaurant():
    def __init__(self, restaurant_id, name, address_id, phone_number, email, description):
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
    
    # setters
    def set_restaurant_id(self, restaurant_id):
        self.restaurant_id = restaurant_id

    def set_name(self, name):
        self.name = name

    def set_address_id(self, address_id):
        self.address_id = address_id

    def set_phone_number(self, phone_number):
        self.phone_number = phone_number
    
    def set_email(self, email):
        self.email = email
    
    def set_description(self, description):
        self.description = description

    
    # getters
    def get_restaurant_id(self):
        return self.restaurant_id
    
    def get_name(self):
        return self.name
    
    def get_address_id(self):
        return self.address_id
    
    def get_phone_number(self):
        return self.phone_number
    
    def get_email(self):
        return self.email
    
    def get_description(self):
        return self.description

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
    
    # setters
    def set_food_id(self, food_id):
        self.food_id = food_id

    def set_name(self, name):
        self.name = name

    def set_restaurant_id(self, restaurant_id):
        self.restaurant_id = restaurant_id

    def set_price(self, price):
        self.price = price
    
    def set_description(self, description):
        self.description = description

    
    # getters
    def get_food_id(self):
        return self.food_id
    
    def get_name(self):
        return self.name
    
    def get_restaurant_id(self):
        return self.restaurant_id
    
    def get_price(self):
        return self.price
    
    def get_description(self):
        return self.description
    
class Order():
    def __init__(self, order_id, order_date, customer_id, restaurant_id, deliver_id, total_cost, credit_card_id, status):
        self.order_list = None
        self.order_id = order_id
        self.order_date = order_date
        self.customer_id = customer_id
        self.restaurant_id = restaurant_id
        self.deliver_id = deliver_id
        self.total_cost = total_cost
        self.credit_card_id = credit_card_id
        self.status = status
    

    def __str__(self):
        return f"{self.order_id}, {self.order_date}, {self.customer_id}, {self.restaurant_id}, {self.deliver_id}, {self.total_cost}, {self.credit_card_id}, {self.status}"
    
    def __repr__(self):
        return f"{self.order_id}, {self.order_date}, {self.customer_id}, {self.restaurant_id}, {self.deliver_id}, {self.total_cost}, {self.credit_card_id}, {self.status}"
    
    # setters
    def set_order_id(self, order_id):
        self.order_id = order_id
    
    def set_order_date(self, order_date):
        self.order_date = order_date

    def set_customer_id(self, customer_id):
        self.customer_id = customer_id
    
    def set_restaurant_id(self, restaurant_id):
        self.restaurant_id = restaurant_id

    def set_deliver_id(self, deliver_id):    
        self.deliver_id = deliver_id
    
    def set_total_cost(self, total_cost):
        self.total_cost = total_cost

    def set_credit_card_id(self, credit_card_id):
        self.credit_card_id = credit_card_id
    
    def set_status(self, status):
        self.status = status
    
    # getters
    def get_order_id(self):
        return self.order_id
    
    def get_order_date(self):
        return self.order_date
    
    def get_customer_id(self):
        return self.customer_id
    
    def get_restaurant_id(self):
        return self.restaurant_id
    
    def get_deliver_id(self):
        return self.deliver_id
    
    def get_total_cost(self):
        return self.total_cost
    
    def get_credit_card_id(self):
        return self.credit_card_id
    
    def get_status(self):
        return self.status

    def get_order_list(self):
        return self.order_list

class OrderLine():
    def __init__(self, order_line_id, order_id, food_id, quantity, price):
        self.order_line_id = order_line_id
        self.order_id = order_id
        self.food_id = food_id
        self.quantity = quantity
        self.price = price
    
    def __str__(self):
        return f"{self.order_line_id}, {self.order_id}, {self.food_id}, {self.quantity}, {self.price}"
    
    def __repr__(self):
        return f"{self.order_line_id}, {self.order_id}, {self.food_id}, {self.quantity}, {self.price}"
    
    # setters
    def set_order_line_id(self, order_line_id):
        self.order_line_id = order_line_id
    
    def set_order_id(self, order_id):
        self.order_id = order_id
    
    def set_food_id(self, food_id):
        self.food_id = food_id
    
    def set_quantity(self, quantity):
        self.quantity = quantity
    
    def set_price(self, price):
        self.price = price
    
    # getters
    def get_order_line_id(self):
        return self.order_line_id
    
    def get_order_id(self):
        return self.order_id
    
    def get_food_id(self):
        return self.food_id
    
    def get_quantity(self):
        return self.quantity
    
    def get_price(self):
        return self.price
    
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
    
    # setters
    def set_credit_card_id(self, credit_card_id):
        self.credit_card_id = credit_card_id

    def set_card_numbner(self, card_number):
        self.card_number = card_number
    
    def set_holder_name(self, holder_name):
        self.holder_name = holder_name
    
    def set_expiration_date(self, expiration_date):
        self.expiration_date = expiration_date
    
    def set_CVV(self, CVV):
        self.CVV = CVV

    # getters
    def get_credit_card_id(self):
        return self.credit_card_id
    
    def get_card_number(self):
        return self.card_number
    
    def get_holder_name(self):
        return self.holder_name
    
    def get_expiration_date(self):
        return self.expiration_date
    
    def get_CVV(self):
        return self.CVV
    
