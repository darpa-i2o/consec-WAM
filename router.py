#!/usr/bin/env python3

import wammessage
import queue
import yaml

CONF_FILE = "RouterConf.yaml"

with open(CONF_FILE) as yf:
    conf_data = yaml.load(yf)

fro = 'ROUTER'
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

if (conf_data['integrity'] == 'sha2'):
    msg_integrity = True
    msg_integrityfunc = wammessage.sha2_if

ms = wammessage.MessageServer(mq, host = conf_data['host'], port = conf_data['message_listen_port'], integrity = msg_integrity, integrityfunc = msg_integrityfunc)

ms.start()
sinks = {}
sinks['UI'] = wammessage.MessageClient(host = conf_data['ui_host'], port = conf_data['ui_port'])
sinks['WHACTUATOR'] = wammessage.MessageClient(host = conf_data['whac_host'], port = conf_data['whac_port'])

while True:
    m = mq.get()
    print("Got message from: " + m.fro + " to: " + m.to + " msg: " + m.message)
    if m.message == 'SHUTDOWN':
        m.fro = 'ROUTER'
        sinks['UI'].send(m)
        sinks['WHACTUATOR'].send(m)
        break
    if m.to == 'UI' or m.to == 'WHACTUATOR':
        sinks[m.to].send(m)

