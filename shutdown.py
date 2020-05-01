#!/usr/bin/env python3

from wammessage import MessageClient, WAMMessage

# Defaults to no integrity checks
m = WAMMessage()
m.construct_message('SHELL', 'ROUTER', 'SHUTDOWN')

# TODO: Pull from RouterConf
mc = MessageClient('127.0.0.1', 8081)
mc.send(m)
