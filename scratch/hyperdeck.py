#script to control kramer vs-88dt

import socket
from inspect import currentframe, getframeinfo
import sys



parms = {
    "ip"    : ["127.0.0.1", "127.0.0.1"],
    "port"  : 9993,
}

cmds = {
    'startrecord'   : "record\r\n",
    'stop'          : "stop\r\n",
    'quit'          : "quit\r\n",
    'deviceinfo'    : "device info\r\n",
    'configuration' : "configuration\r\n",
    'watchdog'      : "watchdog: period: 0\r\n",
}

def hd_send_command(deck, cmd_list):
    BUFFER_SIZE = 1024

    print ('Sending commands %s' %cmd_list)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.connect((parms['ip'][deck], parms['port']))

    data = sock.recv(BUFFER_SIZE).decode()
    print ('Welcome %s' %repr(data))
    
    for cmd_name in cmd_list:
        msg = cmds[cmd_name]

        b = bytes(msg, 'utf-8')
        sock.send(b)

        data = sock.recv(BUFFER_SIZE).decode()
        print ('Sent: %s, Received %s' %(msg, repr(data)))

    sock.close()

def main():

    cl = [cmds['deviceinfo'], cmds['startrecord'] ]

    try:
        hd_send_command(0, cl)

    except Exception as e:
        print( format(e))
        print ('Exception ' )

main()