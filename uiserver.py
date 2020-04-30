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
import queue
import wammessage
import ssl
import sys

CONF_FILE = "UIConf.yaml"

with open(CONF_FILE) as yf:
    conf_data = yaml.load(yf)

req_handler = uihandler.UIRequestHandler
recv_queue = queue.Queue()

fro = 'UI'

if (conf_data['integrity'] == 'off' or not conf_data['integrity']):
    mc = wammessage.MessageClient(host = conf_data['router_host'], port = conf_data['router_port'])
    ms = wammessage.MessageServer(recv_queue, host = conf_data['host'], port = conf_data['message_listen_port'])
#elif (conf_data['integrity'] == 'crc32'):
#    
#elif (conf_data['integrity'] == 'md5'):
#
#elif (conf_data['integrity'] == 'sha1'):
#
else:
    #print(conf_data['integrity'])
    sys.exit(-1)

# Start a HTTP server on a configuration-defined port
httpd = socketserver.TCPServer((conf_data['host'], conf_data['http_listen_port']), req_handler)
if (conf_data['ssl']):
    print("Starting UI server located at: https://", conf_data['host'], ":", conf_data['http_listen_port'], sep = '')
    httpd.socket = ssl.wrap_socket(httpd.socket, certfile = conf_data['cert'], server_side=True)
else:
    print("Starting UI server located at: http://", conf_data['host'], ":", conf_data['http_listen_port'], sep = '')
uithread = threading.Thread(target=httpd.serve_forever)
uithread.start()

ms.start()

time.sleep(10)
if not recv_queue.empty():
    print("Incoming sensor message!")
    uihandler.sensor_reading = "MOLE!"
time.sleep(10)
httpd.shutdown()
print("Got" + str(uihandler.click_queue.qsize()) + "clicks!")
