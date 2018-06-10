from Config import config
from osc4py3.as_eventloop import *
from osc4py3 import oscbuildparse

ip =    config.parms["atemOsc_ip"]
port =  config.parms["atemOsc_port"]
cn  =   config.parms["atemOsc_cn"]

x = osc_startup()

x = osc_udp_client(ip, port, cn)

try:

    addr = "/atem/aux/1 9"
    args = [1.0]
    msg = oscbuildparse.OSCMessage(addr, ",f", args)

    x = osc_send(msg, cn)
    x = osc_process()

    status = "ok"
    result = "cmd=" + addr
except Exception as e:
    result = ["Failed:" + e.strerror]
    status = "exception"


res = { "status" : status, "result": result }

z = osc_terminate()

print("done")