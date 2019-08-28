from http.server import BaseHTTPRequestHandler
from temp import *
from mako.template import Template

class Server(BaseHTTPRequestHandler):
  def do_HEAD(self):
    return
    
  def do_GET(self):
    self.respond()
    
  def do_POST(self):
    return
    
  def handle_http(self, status, content_type):
    self.send_response(status)
    self.send_header('Content-type', content_type)
    self.end_headers()
    t = Template(filename='Templates/index.html')
    return bytes(t.render(history=history), "UTF-8")
    
  def respond(self):
    content = self.handle_http(200, 'text/html')
    self.wfile.write(content)