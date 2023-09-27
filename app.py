from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
# from models import tasks

class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.render_template("index.html")
        elif parsed_path.path == "/tasks":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.render_template("tasks.html")
        elif parsed_path.path == "/about":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.render_template("about.html")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

    # def do_POST(self):
    #     if self.path == "/add_task":
    #         content_length = int(self.headers["Content-Length"])
    #         post_data = self.rfile.read(content_length).decode("utf-8")
    #         params = parse_qs(post_data)
    #         title = params["title"][0]  # Assuming you have a form field named "title"
    #         tasks.append(Task(len(tasks) + 1, title))
    #         self.send_response(303)  # Redirect after POST
    #         self.send_header("Location", "/tasks")
    #         self.end_headers()
    #     else:
    #         self.send_response(404)
    #         self.end_headers()
    #         self.wfile.write(b"Not Found")

    def render_template(self, template_name):
        with open(f"templates/{template_name}", "r") as file:
            template = file.read()
        self.wfile.write(template.encode("utf-8"))

def run_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyRequestHandler)
    print("Server running at http://localhost:8000/")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
