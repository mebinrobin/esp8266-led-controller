from http.server import HTTPServer, BaseHTTPRequestHandler


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hi!')


httpd = HTTPServer(('localhost', 8080), Handler)
httpd.serve_forever()
