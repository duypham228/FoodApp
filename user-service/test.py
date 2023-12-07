from controllers import *
from models import *
from dataAdapter import dataAdapter


dataAdapter = dataAdapter("database/food.db")

user = accountController.login("duyphamo", "123")

ownerController.setUser(user)

# restaurants = ownerController.getRestaurants()

# restaurants = dataAdapter.getAllRestaurants()

# addr = Address(None, "111 Maple St", "Boston", "MA", "02115")

# addr_id = dataAdapter.saveAddress(addr)

# print(addr_id)

# res = Restaurant(None, "Burger King", addr_id, "1236543443", "", "Best Burger in Town")

# res_id = dataAdapter.saveRestaurant(res)

# print(res_id)

# restaurants = dataAdapter.getAllRestaurants()

# # print(restaurants)

# for restaurant in restaurants:
#     print(restaurant.name)

# restaurant = dataAdapter.getRestaurant(2)
# print(restaurant.restaurant_id)
# ownerController.addRestaurant(restaurant)

restaurants = ownerController.getRestaurants()
print(restaurants)



