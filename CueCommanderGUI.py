"""CueCommanderGUI App - Implements event automation for production events.
Originally built for HoW, specifically Unionville Alliance Church.

This version uses tkinter  as the UI
"""

__author__ = "Terry Doner"
__copyright__ = "Copyright 2018, Terry Doner"
__credits__ = ["Terry Doner"]
__license__ = "GPL 3"
__version__ = "0.1"

import sys
import time
from osc4py3.as_eventloop   import *
from osc4py3                import oscmethod as osm
from pathlib                import Path

from Config                 import config

from AudioRecording         import ar_actions
from ProjectorControl       import pc_actions
from MatrixControl          import mc_actions
from BmdControl             import bm_actions # BlackMagic ATEM Controls
#from OBSControl             import oc_actions # Open Broadcast Softwarefrom OBSControl             import oc_actions # Open Broadcast Software
from CSAVControl            import csav_actions

from tkinter import *
from tkinter import ttk

#from functools import partial


# Functions
currentFuncName = lambda n=0: sys._getframe(n + 1).f_code.co_name

def ts():
    "Utility function to generate a timestamp"
    t = time.localtime(time.time())
    yyyy = str(t.tm_year)
    mm = str(t.tm_mon).zfill(2)
    dd = str(t.tm_mday).zfill(2)
    hh = str(t.tm_hour).zfill(2)
    mi = str(t.tm_min).zfill(2)
    se = str(t.tm_sec).zfill(2)
    stamp = yyyy + mm + dd + "_" + hh + mi + se
    return(stamp)

def printf(format, *values):
    print(format % values)

# Globals
finished = False



def end_program(action, value):
    global finished

    if action:
        finished = True
        result = "will terminate"
    else :
        result="Ignored"

    return(result)


def osc_event_handler(address, typetags, arguments):

    found = False
    func = ""

    for k in osc_map.keys():
        addr = "/" + str(config.parms["qlc_universe"]) + "/dmx/" + str(k)
        if addr == address:
            found = True
            func = osc_map[k]

    if found:
        val = arguments[0]

        if val > 0.99:
            action = True
        elif val < 0.99:
            action = False
        else:
            print("Unexpected type:", type(val))
            action = False
            val = -1

        print("%-16s %-20s addr: %-10s    func: %-30s  action: %-5s  value: %f" %
              (ts(), currentFuncName(), address, func.__name__, action, val)
              )

        #dispatch to specific action handler
        res = func(action, val )

        print("%-16s %-20s addr: %-10s    result:%-10s" %
              (ts(), currentFuncName(), address, res)
              )
    else:
        action = False
        val = -2
        print("%-16s %-20s addr: %-10s    >>> Not Recognized <<<" %
              (ts(), currentFuncName(), address)
              )
        print(arguments)

    print("----")

#TODO - apply DRY (don't repeat yourself...) Need to refactor this code
# right now we have osc number mapped to function,
# function name embdeds a name of the command
# then we look up that name to get the command string.
#
# instead config structure should be a 4 value result:
# - OSC # (key)
# - function to invoke
# - parameter to pass
# - Description of what it does.
# doing this would make the code more compact and easier to configure to different installations
# Example:
# 91 : kramer_generic_command, "#VID in>out||VID 4>4\r\n", "Normal - PP stage display to rear display"

# this structure would be used to build the osc map.
# need to think more about how to apply function templates


osc_map = {
     0:  end_program,

    40:  ar_actions.start_recording,
    41:  ar_actions.stop_recording,
    42:  ar_actions.osc_process_files,

    20:  mc_actions.kramer_centreAux,
    21:  mc_actions.kramer_centrePrg,
    22:  mc_actions.kramer_centreNorm,
    23:  mc_actions.kramer_LNvmAux,    # Lobby and Nursery from ATEM Aux
    24:  mc_actions.kramer_LNvmPgm,    # Lobby and Nursery from ATEM Pgm
    29:  mc_actions.kramer_status,
    25:  mc_actions.kramer_centrems,
    26:  mc_actions.kramer_LNms,
    27:  mc_actions.kramer_AC_CDWU0009,
    28:  mc_actions.kramer_AC_CDMUA001,
    90:  mc_actions.kramer_rear_CDWU0009,
    91:  mc_actions.kramer_rear_CDMUA001,

    10: pc_actions.projector_status,
    11: pc_actions.projector_on,
    12: pc_actions.projector_off,

    30: bm_actions.aux_source_pp,
    31: bm_actions.aux_source_vmac,
    32: bm_actions.aux_source_ms,
    33: bm_actions.aux_source_prog,
    #
    # 50: oc_actions.obs_black,
    # 51: oc_actions.obs_announce_noclock,
    # 52: oc_actions.obs_announce_clock,
    # 53: oc_actions.obs_prop_lyrics,
    # 54: oc_actions.obs_series_graphic,

    #61: bm_actions.macro01,
    61: lambda  x, y : bm_actions.macro(1, x, y),
    #61: partial(  bm_actions.macro, num=1 ),

    62: lambda  x, y : bm_actions.macro(2, x, y),
    63: lambda  x, y : bm_actions.macro(3, x, y),
    64: lambda  x, y : bm_actions.macro(4, x, y),
    65: lambda  x, y : bm_actions.macro(5, x, y),
    66: lambda  x, y : bm_actions.macro(6, x, y),
    67: lambda  x, y : bm_actions.macro(7, x, y),
    68: lambda  x, y : bm_actions.macro(8, x, y),
    69: lambda  x, y : bm_actions.macro(9, x, y),
    70: lambda  x, y : bm_actions.macro(10, x, y),

    80: lambda x,y   : csav_actions.playback(21,x,y)

}

def mainOSC():
    """Starts the main processing engine."""
    global finished
    print(ts(), "CueCommander Execution begins\n")

    print(ts(), "parms=", config.parms)

    # validate we have needed configuration values

    # Make server channels to receive packets.

    osc_startup()
    osc_udp_server(config.parms["osc_ip"], config.parms["osc_port"], config.parms["osc_sname"])

    print("%-12s %-20s" % (  "OSC Addr", "Action" ) )

    for k in osc_map.keys():
        addr = "/" + str(config.parms["qlc_universe"]) + "/dmx/" + str(k)
        func = osc_map[ k ]
        print("%-12s %-20s" % (addr, func.__name__ ))

    osc_method("/2/dmx/*",  osc_event_handler, argscheme=osm.OSCARG_MESSAGEUNPACK)

    #this method for /atem is for local unit testing
    #/atem messages are supposed to be received by atemOSC
    #todo - write a stub for atemOSC for unit testing. and remove this line. And simplify Config.
    osc_method("/atem/*",  osc_event_handler , argscheme=osm.OSCARG_MESSAGEUNPACK)

    # Periodically call osc4py3 processing method in your event loop.
    finished = False
    while not finished:
        osc_process()
        time.sleep(.1)
        # a good spot to put in a pause - (1/10th of a second) trade off between repsonse time and cpu burn.

    # Properly close the osc system.

    print(ts(), "CueCommander Execution normal termination.\n")

from UI import build_ui


def mainGUI():

    print(ts(), "I", "CueCommander Main Execution begins\n")

    build_ui.logmsg("I", "CueCommander GUI Initialized.")

    build_ui.root.mainloop()

    print(ts(), "I",  "CueCommander Execution normal termination.\n")


mainGUI()