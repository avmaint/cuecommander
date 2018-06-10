from Config                 import config
from osc4py3.as_eventloop import *

osc_udp_client(config.parms["atemOsc_ip"], config.parms["atemOsc_port"], config.parms["atemOsc_cn"])

print("BmdControl init run")