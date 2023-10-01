from router import Router, render_template

app = Router(__name__)

@app.route('/', ['GET'])
def index(request):\
    return render_template("index.html")

@app.route('/login', ['GET'])
def login(request):
    context = {
        "name": "John"
    }
    return render_template("login.html", **context)

    
if __name__ == "__main__":
    app.run()