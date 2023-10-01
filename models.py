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
    