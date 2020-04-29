#!/usr/bin/env python3

# (C) 2020 Harrell Corp
# This server both spawns a new thread to host HTTP(S) connections to both display the sensor reading as well as provide the human operator
# a button to click to send a "whack" message to the whactuator via the message router

import time
import yaml
import json
import threading
import http.server
import socketserver
import uihandler
import ssl

CONF_FILE = "UIConf.yaml"

with open(CONF_FILE) as yf:
    conf_data = yaml.load(yf)

req_handler = uihandler.UIRequestHandler 

# Start a HTTP server on a configuration-defined port
httpd = socketserver.TCPServer((conf_data['host'], conf_data['listen_port']), req_handler)
if (conf_data['ssl']):
    print("Starting UI server located at: https://", conf_data['host'], ":", conf_data['listen_port'], sep = '')
    httpd.socket = ssl.wrap_socket(httpd.socket, certfile = conf_data['cert'], server_side=True)
else:
    print("Starting UI server located at: http://", conf_data['host'], ":", conf_data['listen_port'], sep = '')
uithread = threading.Thread(target=httpd.serve_forever)
uithread.start()

time.sleep(10)
uihandler.sensor_reading = "MOLE!"
time.sleep(10)
httpd.shutdown()
