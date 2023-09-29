from router import Router

app = Router(__name__)

@app.route('/', ['GET'])
def hello(request):
    # localhost:8000/?name=<yourname>
    return f"hello {request.qs['name'][0]}"

if __name__ == "__main__":
    app.run()