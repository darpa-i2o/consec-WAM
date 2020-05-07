#!/usr/bin/env python3

from wammessage import MessageClient, WAMMessage
import wammessage
import yaml

def do_shutdown():
    
    CONF_FILE = "RouterConf.yaml"
    
    with open(CONF_FILE) as yf:
        conf_data = yaml.load(yf)
        
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

    m = WAMMessage(integrity = msg_integrity, integrityfunc = msg_integrityfunc)
    m.construct_message('SHELL', 'ROUTER', 'SHUTDOWN')

    mc = MessageClient(conf_data['host'], conf_data['message_listen_port'])
    mc.send(m)

if __name__ == '__main__':
    do_shutdown()
