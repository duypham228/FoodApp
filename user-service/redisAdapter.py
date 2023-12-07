from models import Address, User, Restaurant, Food, Order, OrderLine, CreditCard

import redis


class redisAdapter():
    def __init__(self):
        self.host = "redis-14710.c281.us-east-1-2.ec2.cloud.redislabs.com"
        self.port = 14710
        self.r = redis.Redis(host=self.host, port=self.port, password="test123")

    def saveUser(self, user):
        if user.user_id is None:
            user.user_id = self.r.incr('count')
        user_key = f"user:{user.user_id}"
        user_data = {
            'user_id': user.user_id,
            'username': user.username,
            'password': user.password,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'user_type': user.user_type
        }
        # Save user data to Redis
        self.r.hmset(user_key, user_data)

        # Save the username separately
        username_key = f"username:{user.username}"
        self.r.set(username_key, user.user_id)

    def getUser(self, user_id):
        user_key = f"user:{user_id}"
        user_data = self.r.hgetall(user_key)

        if user_data:
            decoded_user_data = {key.decode(): value.decode() for key, value in user_data.items()}

            # Convert user_id to int if it's stored as an integer
            user_id_value = int(decoded_user_data['user_id']) if decoded_user_data.get('user_id') else None

            return User(
                user_id=user_id_value,
                username=decoded_user_data.get('username', ''),
                password=decoded_user_data.get('password', ''),
                first_name=decoded_user_data.get('first_name', ''),
                last_name=decoded_user_data.get('last_name', ''),
                email=decoded_user_data.get('email', ''),
                user_type=decoded_user_data.get('user_type', '')
            )

        return None
    

    def getUserByUsername(self, username):
        username_key = f"username:{username}"
        print(username_key)
        user_id = self.r.get(username_key).decode()

        if user_id:
            return self.getUser(user_id)

        return None

    def deleteUser(self, user_id):
        user_key = f"user:{user_id}"
        # Delete user data from Redis
        self.r.delete(user_key)

        user = self.getUser(user_id)
        username = user.username

        username_key = f"username:{username}"

        # Delete the username key
        self.r.delete(username_key)


   