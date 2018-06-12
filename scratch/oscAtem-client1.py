from Config  import config
from osc4py3.as_eventloop import *
from osc4py3 import oscbuildparse

ip  =   config.parms["atemOsc_ip"]
port =  config.parms["atemOsc_port"]
cn  =   config.parms["atemOsc_cn"]

x = osc_startup()

X = osc_udp_client(ip , port, cn)

# Build a simple message and send it.


addr = "/atem/aux/1 2"
args = [0.0]
msg = oscbuildparse.OSCMessage(addr, ",f", args )
x = osc_send(msg, cn)

x = osc_process()

# Properly close the system.
osc_terminate()