#!/usr/bin/env python3

import threading
import json
import zlib

def crc32_if(string):
    '''Function to compute a string integrity check on a passed string'''
    return str(zlib.crc32(string.encode('utf-8')))

class WAMMessage:
    '''Class to represent a message to be sent or received in the WAM system'''

    def __init__(self, integrity = False, integrityfunc = None):
        '''Creates a message with optional integrity checks'''
        self.to = ''
        self.fro = ''
        self.message = ''
        self.integrity = integrity
        self.integrityfunc = integrityfunc

    def construct_message(self, fro, to, msg):
        '''Populates a message with sender, recipient, and message'''
        self.to = to
        self.fro = fro
        self.message = msg

    def deserialize(self, jsonmsg):
        '''Populates a message by deserializing a JSON input'''
        msg = json.loads(jsonmsg)
        if (self.integrity):
            if (self.integrityfunc(msg['from'] + msg['to'] + msg['message']) != msg['integrity']):
                return
        self.fro = msg['from']
        self.to = msg['to']
        self.message = msg['message']

    def serialize(self):
        '''Serializes a message into a JSON string'''
        msg = {}
        msg['from'] = self.fro
        msg['to'] = self.to
        msg['message'] = self.message
        msg['integrity'] = ''
        if (self.integrity):
            msg['integrity'] = self.integrityfunc(self.fro + self.to + self.message)
        return json.dumps(msg)
