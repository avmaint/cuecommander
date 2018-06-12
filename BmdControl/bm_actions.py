from Config import config
from osc4py3.as_eventloop import *
from osc4py3 import oscbuildparse

# todo as coded, this is silly, but we need to see if it works before elegance.
atem_cmds = {
    'aux_source_pp': "/atem/aux/1",
    'aux_source_vmac': "/atem/aux/1",
    'aux_source_ms': "/atem/aux/1",
    'aux_source_prog': "/atem/aux/1",  # todo  verify correct number for the Program.
    'macro': "/atem/macro/"  # todo verify macro syntax.
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


def macro01(action, value):
    """ """
    return (action_util(action, atem_cmds['macro'], 1))


def macro02(action, value):
    """ """
    return (action_util(action, atem_cmds['macro'], 2))


def macro03(action, value):
    """ """
    return (action_util(action, atem_cmds['macro'], 3))


def macro04(action, value):
    """ """
    return (action_util(action, atem_cmds['macro'], 4))


def macro05(action, value):
    """ """
    return (action_util(action, atem_cmds['macro'], 5))


def macro06(action, value):
    """ """
    return (action_util(action, atem_cmds['macro'], 6))


def macro07(action, value):
    """ """
    return (action_util(action, atem_cmds['macro'], 7))


def macro08(action, value):
    """ """
    return (action_util(action, atem_cmds['macro'], 8))


def macro09(action, value):
    """ """
    return (action_util(action, atem_cmds['macro'], 9))


def macro10(action, value):
    """ """
    return (action_util(action, atem_cmds['macro'], 10))
