from router import Router, render_template
from dataAdapter import dataAdapter

app = Router(__name__)
database_path = "database/food.db"

# authenticated_users = {}

# def is_authenticated(username):
#     return username in authenticated_users

# def login_required(route_function):
#     def wrapper(request):
#         if 'username' in request.json and is_authenticated(request.json['username'][0]):
#             return route_function(request)
#         else:
#             return render_template("index.html")

@app.route('/', ['GET'])
def index(request):\
    return render_template("index.html")

@app.route('/login', ['GET','POST'])
def login(request):
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        if 'username' in request.json and 'password' in request.json:
            username = request.json['username'][0]
            password = request.json['password'][0]

            db = dataAdapter(database_path)
            user = db.getUserByUsername(username)
            db.close()
            if user is not None and user.password == password:
                # authenticated_users[username] = user
                context = {
                    "username": username,
                    "user_type": user.user_type
                }
                if user.user_type == "customer":
                    return render_template("customer_home.html", **context)
                elif user.user_type == "owner":
                    return render_template("owner_home.html", **context)
                elif user.user_type == "deliver":
                    return render_template("deliver_home.html", **context)
            return render_template("login.html")
        else:
            return render_template("login.html")
        
@app.route('/register', ['GET','POST'])
def register(request):
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        print(request.json)
        if 'username' in request.json and 'password' in request.json:
            username = request.json['username'][0]
            password = request.json['password'][0]
            context = {
                "username": username
            }
            return render_template("login.html")
        else:
            return render_template("register.html")
        
# @app.route('/home', ['GET'])
# def home(request):

# @login_required TODO: later after session management is implemented

    
if __name__ == "__main__":
    app.run()