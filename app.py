from router import Router, render_template
from dataAdapter import dataAdapter
import session_manager
from functools import wraps

app = Router(__name__)
database_path = "database/food.db"

def login_required(route_function):
    @wraps(route_function)
    def wrapper(request):
        # Get the session ID from the cookie
        # if request.cookies is not None:
        if request.is_authenticated():
            print("Authenticated")
            print(route_function(request))
            return route_function(request)
        else:
            return render_template("login.html"), None
    return wrapper
 
@app.route('/', ['GET'])
def index(request):
    return render_template("index.html"), None

@app.route('/login', ['GET','POST'])
def login(request):
    if request.method == "GET":
        return render_template("login.html"), None
    elif request.method == "POST":
        # print(request.headers)
        if 'username' in request.json and 'password' in request.json:
            username = request.json['username'][0]
            password = request.json['password'][0]

            db = dataAdapter(database_path)
            user = db.getUserByUsername(username)
            db.close()
            if user is not None and user.password == password:
                session_cookie = session_manager.create_session(username)
                print("Server sessions: ",session_manager.sessions)
                context = {
                    "username": username,
                    "user_type": user.user_type
                }
                if user.user_type == "customer":
                    return render_template("customer_home.html", **context), session_cookie
                elif user.user_type == "owner":
                    return render_template("owner_home.html", **context), session_cookie
                elif user.user_type == "deliver":
                    return render_template("deliver_home.html", **context), session_cookie
            return render_template("login.html"), None
        else:
            return render_template("login.html"), None
        
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
            return render_template("login.html"), None
        else:
            return render_template("register.html"), None
        
@app.route('/home', ['GET'])
@login_required
def home(request):
    return render_template("index.html"), None


# @login_required TODO: later after session management is implemented

    
if __name__ == "__main__":
    app.run()