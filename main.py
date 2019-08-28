#!/usr/bin/env python3
import time
from http.server import HTTPServer
from server import Server
from temp import *
import _thread

HOST_NAME = '0.0.0.0'
PORT_NUMBER = 8000

if __name__ == '__main__':
    httpd = HTTPServer((HOST_NAME, PORT_NUMBER), Server)
    print(time.asctime(), 'Server UP - %s:%s' % (HOST_NAME, PORT_NUMBER))
    try:
        _thread.start_new_thread(poll_temps_foreever, ())

        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), 'Server DOWN - %s:%s' % (HOST_NAME, PORT_NUMBER)) 
