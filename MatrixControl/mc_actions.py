"""
This package manages commnunication with the Kramer VS88DT video matrix switch.
It implements a set of 'presets' which are combinations of settings commonly used at UAC.

Kramer Inputs
# 1 output #1 from fx4 (which comes from CDMU-A001)
# 2 output #2 from fx4 (which comes from CDMU-A001)
# 3 output #3 from fx4 (which comes from CDMU-A001)
# 4 stage display from CDMU-A001
# 5 Mediashout program output (CDWU-0009)
# 6 ATEM Program
# 7 ATEM Aux
# 8 ?

Kramer Outputs
# 1 projector East
# 2 projector centre
# 3 projector west
# 4 cofidence (rear)
# 5 ?
# 6 ATEM
# 7 Lobby
# 8 Nursery

"""
from Config import config
import socket

kramer_cmds = {
    'bdate'     : "#BUILD-DATE?\r\n",
    'model'     : "#MODEL?\r\n",
    'version'   : "#VERSION?\r\n",
    'protver'   : "#PROT-VER?\r\n",
    'status'     : "#BUILD-DATE?|MODEL?|#VERSION?|#PROT-VER?\r\n",
    'centrePrg' : "#VID in>out|VID 6>2\r\n", # feed centre screen from VM Program
    'centreAux' : "#VID in>out|VID 7>2\r\n", # feed centre screen from VM Aux
    'centreNorm': "#VID in>out|VID 2>2\r\n", # feed centre screen as normal
    'LNvmAux'   : "#VID in>out||VID 7>7|VID 7>8\r\n",
    'LNvmPgm'   : "#VID in>out||VID 6>7|VID 6>8\r\n",
    'LNms'      : "#VID in>out||VID 5>7|VID 5>8\r\n", # nursery and lobby from mediashout
    'centrems'  : "#VID in>out|VID 5>2\r\n",  # feed centre screen as normal
    'AC_CDWU0009'   : "#VID in>out||VID 5>1|VID 5>3\r\n",  # feed AC from Windows
    'AC_CDMUA001'   : "#VID in>out||VID 1>1|VID 3>3\r\n",  # feed AC from ProPresenter,
    'rear_CDWU0009' : "#VID in>out||VID 5>4\r\n", # Windows output to rear
    'rear_CDMUA001' : "#VID in>out||VID 4>4\r\n"   # normal PP stage display to rear
}


def kramer_send_command(cmd ):
    BUFFER_SIZE = 1024
    data=""

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)

        try:
            sock.connect((config.vs88dt["ip"], config.vs88dt["port"]))
        except Exception as e:
            print('Exception on connect:', format(e))

        data = sock.recv(BUFFER_SIZE).decode()
        print('Welcome %s' % repr(data))

        #for cmd_name in cmd_list:
        #msg = cmd

        b = bytes(cmd, 'utf-8')
        sock.send(b)

        # print ('Sent:', cmd )
        data = sock.recv(BUFFER_SIZE).decode()
        print('Sent: %s, Received %s' % (cmd, repr(data)))

    except Exception as e:
        print('Exception:', format(e))

    sock.close()

    return(repr(data))


def action_util(action, cmd):
    """Action execution. """
    if action:
        try:
            result =  kramer_send_command(cmd)
            status = "ok"
        except Exception as e:
            result = ["Failed:" + e.strerror]
            status = "exception"
    else:
        status = "ok"
        result = ["No Action"]

    res = {"status": status, "result": result}

def kramer_LNms(action, value):
    "switches lobby and nursery to mediashout as the source"
    return ( action_util(action, kramer_cmds[ 'LNms' ] ))

def kramer_centrems(action, value):
    "switches centre screen to mediashout"
    return (action_util(action, kramer_cmds[ 'centrems' ] ))

def kramer_LNvmPgm(action, value):
    """Sets lobby and nursery to ATEM program"""
    return (action_util(action, kramer_cmds[ 'LNvmPgm' ] ))

def kramer_LNvmAux(action, value):
    """Sets lobby and nursery to ATEM Auxillary output"""
    return (action_util(action, kramer_cmds[ 'LNvmAux' ] ))

def kramer_centreNorm(action, value):
    """Sets centre screen to normal mapping"""
    return (action_util(action, kramer_cmds[ 'centreNorm' ] ))

def kramer_centrePrg(action, value):
    """Sets cenrtre screen to ATEM program"""
    return (action_util(action, kramer_cmds['centrePrg'] ))

def kramer_centreAux(action, value):
    """Sets centre screen to ATEM Auxillary"""
    return (action_util(action, kramer_cmds[ 'centreAux' ] ))

def kramer_AC_CDWU0009(action, value):
    """Sets AC screen to windows"""
    return (action_util(action, kramer_cmds[ 'AC_CDWU0009' ] ))

def kramer_AC_CDMUA001(action, value):
    """Sets AC screen to Mac - PropPRESENTER"""
    return (action_util(action, kramer_cmds[ 'AC_CDMUA001' ] ))

def kramer_status(action, value):
    """query video matrix switch status"""
    return (action_util(action, kramer_cmds['status']  ))

def kramer_rear_CDWU0009(action, value):
    """Sets rear screen to Windows"""
    return (action_util(action, kramer_cmds[ 'rear_CDWU0009' ] ))

def kramer_rear_CDWU0009(action, value):
    """Sets rear screen to PP Stage Display"""
    return (action_util(action, kramer_cmds[ 'rear_CDMUA001' ] ))

def kramer_generic_command(action, osc, commandstr, description):
    """Invokes an action on the kramer matrix switch"""
    return (action_util(action, commandstr ))
