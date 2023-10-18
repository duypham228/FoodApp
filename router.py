from http.server import SimpleHTTPRequestHandler, HTTPServer, ThreadingHTTPServer
import urllib.parse as urlparse
import json
import session_manager

routes = {}
route_methods = {}


class Request:
    def __init__(self, request, method, session_manager=session_manager):
        self.request = request
        self.method = method
        self.path = urlparse.urlparse(request.path).path
        self.qs = urlparse.parse_qs(urlparse.urlparse(request.path).query)
        self.headers = request.headers
        self.content_length = int(self.headers.get('content-length', 0))
        self.body = request.rfile.read(self.content_length).decode('utf-8')
        self.session_manager = session_manager
        try:
            self.json = urlparse.parse_qs(self.body)
        except json.decoder.JSONDecodeError: 
            self.json = {}
        
        def is_authenticated(self):
            return self.session_manager.is_valid_session(self.session_id)

        def get_authenticated_username(self):
            return self.session_manager.get_username(self.session_id)


def render_template(template_name, **context):
    with open(f"templates/{template_name}", "r") as file:
        template = file.read()
    if context:
        template = template.format(**context)
    return template

class RequestHandler(SimpleHTTPRequestHandler):

    def not_found(self, request):
        return self.write_response(f"{request.path} 404 NOT FOUND", 404)
    
    def method_not_supported(self, request):
        return self.write_response(f"{request.path} {request.method} not supported", 401)

    def write_response(self, response, status_code):
        self.send_response(status_code)
        if isinstance(response, dict):
            self.send_header("Content-type", "application/json")
            response = json.dumps(response)
        else:
            self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(str.encode(response))

    def process_request(self, request):
        if request.path not in routes:
            return self.not_found(request)
        if request.method not in route_methods[request.path]:
            return self.method_not_supported(request)
        resp = routes[request.path](request)
        self.write_response(resp, 200)
    
    def redirect(self, location, status_code=302):
        self.send_response(status_code)
        self.send_header("Location", location)
        self.end_headers()

    def do_GET(self):
        request = Request(self, method='GET')
        return self.process_request(request)
    
    def do_POST(self):
        request = Request(self, method='POST')
        return self.process_request(request)


class Router:

    def __init__(self, name):
        self.name = name
        self.server_class = ThreadingHTTPServer
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