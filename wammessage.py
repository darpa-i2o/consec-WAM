#!/usr/bin/env python3

import threading
import json
import zlib
import socket
import queue
import hashlib

def md5_if(string):
    '''Function to compute a MD5 integrity check on a passed string'''
    return hashlib.md5(string.encode('utf-8')).hexdigest()

def sha1_if(string):
    '''Function to compute a SHA1 integrity check on a passed string'''
    return hashlib.sha1(string.encode('utf-8')).hexdigest()

def sha2_if(string):
    '''Function to compute a SHA2 integrity check on a passed string'''
    return hashlib.sha256(string.encode('utf-8')).hexdigest()

def crc32_if(string):
    '''Function to compute a CRC32 integrity check on a passed string'''
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

class MessageClient:
    '''Class to send messages to a specified destination'''

    def __init__(self, host = '127.0.0.1', port = 8090):
        '''Constructs a client to send messages'''
        self.host = host
        self.port = port

    def send(self, msg):
        '''Sends a message'''
        mb = msg.serialize().encode('utf-8')
        s = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)
        s.sendto(mb, (self.host, self.port))

class MessageServer(threading.Thread):
    '''Class to receive messages in a new thread and add them to a specified queue'''
    
    def __init__(self, queue, integrity = False, integrityfunc = None, host = '127.0.0.1', port = 8090):
        '''Initializes a server with hostname and port to listen on'''
        self.host = host
        self.port = port
        self.queue = queue
        self.integrity = integrity
        self.integrityfunc = integrityfunc
        self.buffersz = 1024
        threading.Thread.__init__(self)

    def run(self):
        '''Starts the server in a new thread'''
        s = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)
        s.bind((self.host, self.port))
        while(True):
            mb = s.recvfrom(self.buffersz)
            m = WAMMessage(integrity = self.integrity, integrityfunc = self.integrityfunc)
            m.deserialize(mb[0].decode('utf-8'))
            self.queue.put(m)
            #print("Got message from: " + m.fro)
            if (m.message == "SHUTDOWN"):
                break
        s.close()
