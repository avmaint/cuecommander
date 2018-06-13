"""CueCommander App - Implements event automation for production events.
Originally built for HoW, specifically Unionville Alliance Church.

This version uses QLC+ as the UI which generates OSC events for action.
"""

__author__ = "Terry Doner"
__copyright__ = "Copyright 2018, Terry Doner"
__credits__ = ["Terry Doner"]
__license__ = "GPL 3"
__version__ = "0.3"

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
from OBSControl             import oc_actions # Open Broadcast Software

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

    10: pc_actions.projector_status,
    11: pc_actions.projector_on,
    12: pc_actions.projector_off,

    30: bm_actions.aux_source_pp,
    31: bm_actions.aux_source_vmac,
    32: bm_actions.aux_source_ms,
    33: bm_actions.aux_source_prog,

    50: oc_actions.obs_black,
    51: oc_actions.obs_announce_noclock,
    52: oc_actions.obs_announce_clock,
    53: oc_actions.obs_prop_lyrics,
    54: oc_actions.obs_series_graphic,

    61: bm_actions.macro01,
    62: bm_actions.macro02,
    63: bm_actions.macro03,
    64: bm_actions.macro04,
    65: bm_actions.macro05,
    66: bm_actions.macro06,
    67: bm_actions.macro07,
    68: bm_actions.macro08,
    69: bm_actions.macro09,
    70: bm_actions.macro10,

}

def main():
    """Starts the main processing engine."""
    global finished
    print(ts(), "CueCommander Execution begins\n")

    #TODO replace embedded parms with external config file. report on the config file used and optionally the contents.
    print(ts(), "parms=", config.parms)

    osc_startup()

    # Make server channels to receive packets.

    osc_udp_server(config.parms["osc_ip"], config.parms["osc_port"], config.parms["osc_sname"])

    print("\tOSC Addr\tAction")

    for k in osc_map.keys():
        addr = "/" + str(config.parms["qlc_universe"]) + "/dmx/" + str(k)
        func = osc_map[ k ]
        print(addr, func.__name__, sep='\t') #TODO remove after core engine is working

    osc_method("/2/dmx/*",  osc_event_handler , argscheme=osm.OSCARG_MESSAGEUNPACK)
    #this method for /atem is for local unit testing
    osc_method("/atem/*",  osc_event_handler , argscheme=osm.OSCARG_MESSAGEUNPACK)

    # Periodically call osc4py3 processing method in your event loop.
    finished = False
    while not finished:
        osc_process()
        time.sleep(.25)
        # a good spot to put in a pause - (1/10th of a second) trade off between repsonse time and cpu burn.

    # Properly close the osc system.
    osc_terminate()

    print(ts(), "CueCommander Execution normal termination.\n")

main()

############################
## Notes
############################

# What I know about midi messages.
#       midi_status:  use p1=144 of my laptop and p1=176 for CDWU-0009
#todo need to figure out where QLC specs 144 or 176
#       we want to use the input "IAC Driver Bus 1"
#       we only handle "note velocity" events
#       midi status identifies between "Note Velocity", "Control Change' and 'Program Change'
#       Note Velocity => 144
#       Control Change => 176
#       Program Change => 192