#!/usr/bin/env python3

import wammessage
import random
import yaml
import time

class Sensor:
    '''A sensor to detect digital moles'''

    def __init__(self, host, port, integrity = False, integrityfunc = None):
        self.fro = 'SENSOR'
        self.to = 'UI'
        self.pollint = 5
        self.mole = 'NO MOLE!'
        self.host = host
        self.port = port
        self.integrity = integrity
        self.integrityfunc = integrityfunc
        self.msg = wammessage.WAMMessage(integrity = self.integrity, integrityfunc = self.integrityfunc)
        self.mc = wammessage.MessageClient(host = self.host, port = self.port)
        random.seed()

    def start(self):
        while True:
            rv = random.randint(0, 100)
            if rv <= conf_data['mole_chance']:
                self.mole = 'MOLE!'
            else:
                self.mole = 'NO MOLE!'
            self.msg.construct_message(self.fro, self.to, self.mole)
            self.mc.send(self.msg)
            time.sleep(self.pollint)

if __name__ == '__main__':
    CONF_FILE = "SensorConf.yaml"
    
    with open(CONF_FILE) as yf:
        conf_data = yaml.load(yf)
        
    msg_integrity = False
    msg_integrityfunc = None

    if (conf_data['integrity'] == 'crc32'):
        msg_integrity = True
        msg_integrityfunc = wammessage.crc32_if
        
    if (conf_data['integrity'] == 'sha1'):
        msg_integrity = True
        msg_integrityfunc = wammessage.sha1_if

    s = Sensor(conf_data['router_host'], conf_data['router_port'], integrity = msg_integrity, integrityfunc = msg_integrityfunc)
    s.start()
