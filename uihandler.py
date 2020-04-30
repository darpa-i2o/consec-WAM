#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler
import queue

sensor_reading = "NO MOLE"
click_queue = queue.Queue()

class UIRequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Refresh', '5')
        self.end_headers()

    def _wam_respond(self):
        content = '<html><head><title>WAM</title></head><body><h1>{}</h1><form action="/" method="post"><input type="submit" value="Whack mole!"/></form></body></html>'
        return content.format(sensor_reading).encode('utf-8')

    def do_GET(self):
        self._set_headers()
        self.wfile.write(self._wam_respond())

    def do_POST(self):
        click_queue.put('CLICK')
        self.send_response(303)
        self.send_header('Location', '/')
        self.end_headers()
