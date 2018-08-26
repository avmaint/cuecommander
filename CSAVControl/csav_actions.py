"""This package is responsible for the communications with the lighting system.
The current implementation works with our ETC CS AV Console.
"""

from Config import config
from osc4py3.as_eventloop import *
from osc4py3 import oscbuildparse

# todo as coded, this is silly, but we need to see if it works before elegance.
atem_cmds = {
    'csav_playback_21': "/cs/playback/21/level/1.0",

    'playback': lambda x: "cs/playback/" + str(x) + "/level/1.0"    
}

ip = config.parms["csav_ip"]
port = config.parms["csav_port"]
cn = config.parms["csav_cn"]

def action_util(action: bool, cmd, val):
    if action:
        try:
            # osc_startup()
            # osc_udp_client(config.parms[ "atemOsc_ip" ], config.parms[ "atemOsc_port" ], config.parms[ "atemOsc_cn" ])
            addr = cmd
            args = [val]
            msg = oscbuildparse.OSCMessage(addr, ",i", args)
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

    res = {"status": status, "result": result}

    return (res)


def tmp_source_pp(action, value):
    """ """
    return (action_util(action, atem_cmds['aux_source_pp'], 1))

def playback(num, action, value):
    """ """

    print("%-16s %-20s       %-10s    func: %-30s  playback: %d" %
          ("",   "", "", "playback", num )
          )

    return (action_util(action, atem_cmds['playback'](num), 1))