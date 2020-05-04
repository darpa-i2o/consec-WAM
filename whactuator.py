#!/usr/bin/env python3

import sensor
import wammessage
import yaml
import threading
import queue

CONF_FILE = "WhactuatorConf.yaml"

with open(CONF_FILE) as yf:
    conf_data = yaml.load(yf)

mq = queue.Queue()
msg_integrity = False
msg_integrityfunc = None

if (conf_data['integrity'] == 'crc32'):
    msg_integrity = True
    msg_integrityfunc = wammessage.crc32_if

if (conf_data['integrity'] == 'md5'):
    msg_integrity = True
    msg_integrityfunc = wammessage.md5_if

if (conf_data['integrity'] == 'sha1'):
    msg_integrity = True
    msg_integrityfunc = wammessage.sha1_if

ms = wammessage.MessageServer(mq, host = conf_data['host'], port = conf_data['port'], integrity = msg_integrity, integrityfunc = msg_integrityfunc)

s = sensor.Sensor(conf_data['router_host'], conf_data['router_port'], integrity = msg_integrity, integrityfunc = msg_integrityfunc)
sthread = threading.Thread(target = s.start)

sthread.start()
ms.start()

while True:
    if not mq.empty():
        m = mq.get()
        if s.mole == 'MOLE!' and m.message == 'WHACK!':
            print('Successfully whacked a mole!')
        if s.mole == 'NO MOLE!' and m.message == 'WHACK!':
            print('Whacked at nothing!')
        if m.message == 'SHUTDOWN':
            print("Received shutdown message from router")
            s.shutdown = True
            break

