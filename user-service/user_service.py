from router import Router, render_template, redirect
import session_manager
from functools import wraps
import json

from controllers import accountController

app = Router(__name__, 8001)
database_path = "database/food.db"

def login_required(route_function):
    @wraps(route_function)
    def wrapper(request):
        # Get the session ID from the cookie
        # if request.cookies is not None:
        if request.is_authenticated():
            print("Authenticated")
            return route_function(request)
        else:
            print("Not authenticated")
            return redirect("/")
    return wrapper
 
@app.route('/', ['GET'])
def index(request):
    return render_template("index.html")

@app.route('/login', ['GET','POST'])
def login(request):
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        # print(request.headers)
        print(request.json)
        if 'username' in request.json and 'password' in request.json:
            username = request.json['username'][0]
            password = request.json['password'][0]
            
            user = accountController.login(username, password)
            if user is not None:
                return {"status": "success", "user": user.__dict__}, None
            return {"status": "fail"}, None
        else:
            return {"status": "fail"}, None
        
@app.route('/register', ['GET','POST'])
def register(request):
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        print(request.json)
        if 'username' in request.json and 'password' in request.json:
            username = request.json['username'][0]
            password = request.json['password'][0]
            first_name = request.json['firstname'][0]
            last_name = request.json['lastname'][0]
            email = request.json['email'][0]
            user_type = request.json['usertype'][0]
            accountController.register(username, password, first_name, last_name, email, user_type)
            return {"status": "success"}, None
        else:
            return {"status": "fail"}, None

@app.route('/getUserByUsername', ['GET'])
def getUserByUsername(request):
    if request.method == "GET":
        if 'username' in request.qs:
            username = request.qs['username'][0]
            user = accountController.getUserByUsername(username)
            if user is not None:
                return {"status": "success", "user": user.__dict__}, None
            return {"status": "fail"}, None
        else:
            return {"status": "fail"}, None
    
if __name__ == "__main__":
    app.run()