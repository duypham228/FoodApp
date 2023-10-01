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


def render_template(template_name, **context):
    with open(f"templates/{template_name}", "r") as file:
        template = file.read()
    if context:
        template = template.format(**context)
    return template

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
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(str.encode(resp))
    
    def do_POST(self):
        pass


class Router:

    def __init__(self, name):
        self.name = name
        self.server_class = HTTPServer
        self.handler_class = RequestHandler
    
    def run(self):
        server_address = ('', 8000)
        httpd = self.server_class(server_address, self.handler_class)
        print("Server running at http://localhost:8000/")
        httpd.serve_forever()
        
    def route(self, path, methods):
        def wrapper(f):
            routes[path] = f
            route_methods[path] = methods
        return wrapper

    def get_handler(self, request):
        return self.handler_class(request)



