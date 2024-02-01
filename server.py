import http.server
import socketserver

PORT = 9999


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # The path to the root of your static files
        self.directory = "./output/html"
        return super().do_GET()


# Create an object of the above class
handler_object = MyHttpRequestHandler

with socketserver.TCPServer(("", PORT), handler_object) as httpd:
    print(f"Serving HTTP on 0.0.0.0 port {PORT} (http://0.0.0.0:{PORT}/)...")
    httpd.serve_forever()
