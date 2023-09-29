from http.server import SimpleHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse
import json

routes = {}
route_methods = {}

class Request:
    def __init__(self, request, method):
        self.request = request
        self.method = method
        self.path = urlparse.urlparse(request.path).path
        self.qs = urlparse.parse_qs(urlparse.urlparse(request.path).query)
        self.headers = request.headers

class RequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        request = Request(self, "GET")
        print("hello")
        print(request.path)
        print(routes)
        resp = routes[request.path](request)

        if isinstance(resp, dict):
            resp = json.dumps(resp)

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(str.encode(resp))
    
    def do_POST(self):
        pass

class Router:

    def __init__(self, name):
        self.name = name
    
    def run(self, server_class=HTTPServer, handler_class=RequestHandler):
        server_address = ('', 8000)
        httpd = server_class(server_address, handler_class)
        print("Server running at http://localhost:8000/")
        httpd.serve_forever()
        
    def route(self, path, methods):
        def wrapper(f):
            routes[path] = f
            route_methods[path] = methods
        return wrapper

    