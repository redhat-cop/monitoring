import http.server
import socketserver

from handlers import get_health

class HttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):

        if self.path.startswith("/health"):
            output = get_health(self)
        else:
            output = "unable to parse request type"

        self.wfile.write(bytes(output, "utf8"))

        return

handler = HttpRequestHandler

PORT = 9418
my_server = socketserver.ThreadingTCPServer(("", PORT), handler)
my_server.serve_forever()
