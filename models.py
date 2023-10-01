class Address():
    def __init__(self, address_id, street, city, state, zip):
        self.address_id = address_id
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state}, {self.zip}"

    def __repr__(self):
        return f"{self.street}, {self.city}, {self.state}, {self.zip}"
    
    # setters
    def set_street(self, street):
        self.street = street

    def set_city(self, city):
        self.city = city

    def set_state(self, state):
        self.state = state
    
    def set_zip(self, zip):
        self.zip = zip
    
    # getters
    def get_street(self):
        return self.street
    
    def get_city(self):
        return self.city
    
    def get_state(self):
        return self.state
    
    def get_zip(self):
        return self.zip
    