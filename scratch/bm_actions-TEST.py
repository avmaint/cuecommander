from Config import config
from osc4py3.as_eventloop import *
from osc4py3 import oscbuildparse

atem_cmds = {
    'aux_source_pp'     : "/atem/aux/1 1",
    'aux_source_vmac'   : "/atem/aux/1 2",
    'aux_source_ms'     : "/atem/aux/1 3",
    'aux_source_prog'   : "/atem/aux/1 9",
    'macro01'           : "/2/dmx/61"
}

ip =    config.parms["atemOsc_ip"]
port =  config.parms["atemOsc_port"]
cn  =   config.parms["atemOsc_cn"]

x = osc_startup()

x = osc_udp_client(ip, port, cn)

def action_util(action:bool, cmd):

    if action:
        try:
            #osc_startup()
            #osc_udp_client(config.parms[ "atemOsc_ip" ], config.parms[ "atemOsc_port" ], config.parms[ "atemOsc_cn" ])
            addr = cmd
            args = [1.0]
            msg = oscbuildparse.OSCMessage(addr, ",f", args)
            x = osc_send(msg, cn)

            x = osc_process()

            status = "ok"
            result = "cmd=" + cmd
        except Exception as e:
            result = ["Failed:" + e.strerror]
            status = "exception"
    else:
        result = ["No action"]
        status = "ok"

    res = { "status" : status, "result": result }

    return(res)


def aux_source_pp(action, value):
    """ """
    return (action_util(action, atem_cmds['aux_source_pp']  ))


def aux_source_vmac(action, value):
    """ """
    return (action_util(action, atem_cmds['aux_source_vmac']))


def aux_source_ms(action, value):
    """ """
    return (action_util(action, atem_cmds['aux_source_ms']))

def aux_source_prog(action, value):
    """ """
    return (action_util(action, atem_cmds['aux_source_prog']))

def macro01(action, value):
    """ """
    return (action_util(action, atem_cmds['macro01']))

macro01(True, [1.0])
