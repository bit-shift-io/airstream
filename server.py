from http.server import BaseHTTPRequestHandler
from temp import *
from mako.template import Template
from pathlib import Path

routes = {
  "/" : {
    "template" : "index.html"
  }
}

class Server(BaseHTTPRequestHandler):

  def init(self):
    print("INIT CALLED")
    self.filetypes = {
      ".js": {
        "contentType": "text/javascript",
        "fn": self.handle_text
      },
      ".css": {
        "contentType": "text/css",
        "fn": self.handle_text
      },
      ".jpg": {
        "contentType": "image/jpeg",
        "fn": self.handle_binary
      },
      ".html": {
        "contentType": "text/html",
        "fn": self.handle_html
      }
    }
    print(self.filetypes)

  def find_filetype(self, file_path):
    split_path = os.path.splitext(file_path)
    extension = split_path[1]
    return self.filetypes[extension]

  def handle_text(self, file_path):
    print("handle_text:" + "{}".format(file_path))
    return bytes(open("{}".format(file_path), 'r').read(), "UTF-8")

  def handle_binary(self, file_path):
    print("handle_binary:" + "{}".format(file_path))
    return open("{}".format(file_path), 'rb')

  def handle_html(self, file_path):
    print("handle_html:" + "{}".format(file_path))
    t = Template(filename="{}".format(file_path))
    return bytes(t.render(history=history), "UTF-8")

  def do_HEAD(self):
    return
    
  def do_GET(self):
    self.init()
    status = 200
    content_type = "text/plain"
    response_content = ""

    path = self.path

    print("GET with path: " + self.path)

    if self.path in routes:
        print(routes[self.path])
        path = routes[self.path]['template']

    filepath = Path("Templates/{}".format(path))
    if filepath.is_file():
      filetype = self.find_filetype(filepath)
      if (filetype):
        content_type = filetype["contentType"]
        response_content = filetype["fn"](filepath)
      else:
        content_type = "text/plain"
        response_content = bytes("404 Not Found", "UTF-8")
    else:
        content_type = "text/plain"
        response_content = bytes("404 Not Found", "UTF-8")

    self.send_response(status)
    self.send_header('Content-type', content_type)
    self.end_headers()
    #content = bytes(response_content, "UTF-8")
    self.wfile.write(response_content)
    return
    
  def do_POST(self):
    return
    
