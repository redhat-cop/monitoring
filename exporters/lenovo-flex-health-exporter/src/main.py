import http.server
import socketserver

from handlers import cmm, imm

class HttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):

        if self.path.startswith("/cmmhealth"):
            output = cmm.get_health(self)
        elif self.path.startswith("/immhealth"):
            output = imm.get_health(self)
        else:
            output = "unable to parse request type"

        self.wfile.write(bytes(output, "utf8"))

        return

handler = HttpRequestHandler

PORT = 9417
my_server = socketserver.ThreadingTCPServer(("", PORT), handler)
my_server.serve_forever()
