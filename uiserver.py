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

msg_integrity = False
msg_integrityfunc = None
mc = wammessage.MessageClient(host = conf_data['router_host'], port = conf_data['router_port'])
ms = wammessage.MessageServer(recv_queue, host = conf_data['host'], port = conf_data['message_listen_port'])

if (conf_data['integrity'] == 'crc32'):
    ms.integrity = True
    ms.integrityfunc = wammessage.crc32_if
    msg_integrity = True
    msg_integrityfunc = wammessage.crc32_if

if (conf_data['integrity'] == 'md5'):
    ms.integrity = True
    ms.integrityfunc = wammessage.md5_if
    msg_integrity = True
    msg_integrityfunc = wammessage.md5_if

if (conf_data['integrity'] == 'sha1'):
    ms.integrity = True
    ms.integrityfunc = wammessage.sha1_if
    msg_integrity = True
    msg_integrityfunc = wammessage.sha1_if

# Start a HTTP server on a configuration-defined port
httpd = socketserver.TCPServer((conf_data['host'], conf_data['http_listen_port']), req_handler)
if (conf_data['ssl']):
    print("Starting UI server located at: https://", conf_data['host'], ":", conf_data['http_listen_port'], sep = '')
    httpd.socket = ssl.wrap_socket(httpd.socket, certfile = conf_data['cert'], server_side=True)
else:
    print("Starting UI server located at: http://", conf_data['host'], ":", conf_data['http_listen_port'], sep = '')
uithread = threading.Thread(target=httpd.serve_forever)

# Start the HTTP server, and the message server
uithread.start()
ms.start()

# Loop to check queues and process
while True:
    if not recv_queue.empty():
        m = recv_queue.get()
        print("Incoming message!")
        uihandler.sensor_reading = m.message 
        if m.message == 'SHUTDOWN':
            print("Received shutdown message from router")
            break
    if not uihandler.click_queue.empty():
        c = uihandler.click_queue.get()
        m = wammessage.WAMMessage(integrity = msg_integrity, integrityfunc = msg_integrityfunc)
        m.construct_message(fro, 'WHACTUATOR', 'WHACK!')
        mc.send(m)

httpd.shutdown()
