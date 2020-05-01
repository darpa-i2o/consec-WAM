#!/usr/bin/env python3

import wammessage
import random
import yaml
import time

random.seed()
CONF_FILE = "SensorConf.yaml"

with open(CONF_FILE) as yf:
    conf_data = yaml.load(yf)

fro = 'SENSOR'
to = 'UI'
msg_integrity = False
msg_integrityfunc = None

if (conf_data['integrity'] == 'crc32'):
    msg_integrity = True
    msg_integrityfunc = wammessage.crc32_if

if (conf_data['integrity'] == 'sha1'):
    msg_integrity = True
    msg_integrityfunc = wammessage.sha1_if

molem = 'NO MOLE!'
m = wammessage.WAMMessage(integrity = msg_integrity, integrityfunc = msg_integrityfunc)
mc = wammessage.MessageClient(host = conf_data['router_host'], port = conf_data['router_port'])

while True:
    rv = random.randint(0, 100)
    if rv <= conf_data['mole_chance']:
        molem = 'MOLE!'
    else:
        molem = 'NO MOLE!'
    m.construct_message(fro, to, molem)
    mc.send(m)
    time.sleep(5)
