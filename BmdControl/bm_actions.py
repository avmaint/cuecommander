from Config import config
from osc4py3.as_eventloop import *
from osc4py3 import oscbuildparse

# todo as coded, this is silly, but we need to see if it works before elegance.
atem_cmds = {
    'aux_source_pp': "/atem/aux/1",
    'aux_source_vmac': "/atem/aux/1",
    'aux_source_ms': "/atem/aux/1",
    'aux_source_prog': "/atem/aux/1",  # todo  verify correct number for the Program.
    'macro': lambda x: "atem/macros/" + str(x) + "/run"   # macro syntax /atem/macros/$i/run.
}

ip = config.parms["atemOsc_ip"]
port = config.parms["atemOsc_port"]
cn = config.parms["atemOsc_cn"]


# x = osc_startup()

# = osc_udp_client(ip, port, cn)

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


def aux_source_pp(action, value):
    """ """
    return (action_util(action, atem_cmds['aux_source_pp'], 1))


def aux_source_vmac(action, value):
    """ """
    return (action_util(action, atem_cmds['aux_source_vmac'], 2))


def aux_source_ms(action, value):
    """ """
    return (action_util(action, atem_cmds['aux_source_ms'], 3))


def aux_source_prog(action, value):
    """ """
    return (action_util(action, atem_cmds['aux_source_prog'], 9))


def macro(num, action, value):
    """ """

    print("%-16s %-20s       %-10s    func: %-30s  macro: %d" %
          ("",   "", "", "macro", num )
          )

    return (action_util(action, atem_cmds['macro'](num), 1))