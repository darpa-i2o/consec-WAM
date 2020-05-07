#!/usr/bin/env python3

import os
import sys
import socketserver
import socket
import threading
import shutdown
import time

mcount = 0
stime = time.time()

class DebugServer(socketserver.BaseRequestHandler):
    
    rcsz = 1024
    menu = "WAM debugging menu:\r\np [IP]: pings an IP from the router to verify connection\r\nq: terminates debugging session\r\nr: prints router stats\r\ns: shutdown WAM\r\n"

    def handle(self):
        '''Handles a single session of debugging'''
        self.request.sendall(self.menu.encode('utf-8'))
        while True:
            inc = self.request.recv(self.rcsz).strip().decode('utf-8')
            if len(inc) == 0:
                self.request.sendall("Please type a command\r\n".encode('utf-8'))
            elif inc[0] == 'q':
                #print('Quitting')
                break
            elif inc[0] == 'r':
                self.request.sendall("WAM router has been running {} seconds, handling {} messages\r\n".format(int(time.time() - stime), mcount).encode('utf-8'))
            elif inc[0] == 'p':
                # NOTICE THERE IS A COMMAND INJECTION VULN HERE!
                s = os.popen('ping -c 1 {}'.format(inc[2:]))
                self.request.sendall("Ping results:\r\n{}".format(s.read()).encode('utf-8'))
            elif inc[0] == 's':
                shutdown.do_shutdown()
                break
            else:
                self.request.sendall("Invalid command\r\n".encode('utf-8'))


# if __name__ == '__main__':
#     dbgd = socketserver.TCPServer(('127.0.0.1', 9999), DebugServer)
#     dbgd.serve_forever()
