"""CueCommander App - Implements event automation for production events.
Originally built for HoW, specifically Unionville Alliance Church.

This version uses QLC+ as the UI which generates OSC events for action.
"""

__author__ = "Terry Doner"
__copyright__ = "Copyright 2018, Terry Doner"
__credits__ = ["Terry Doner"]
__license__ = "GPL 2"
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
    else :
        pass


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


osc_map = {
     2: end_program,

     0:  ar_actions.start_recording,
     1:  ar_actions.stop_recording,
     3:  ar_actions.osc_process_files,

     4:  mc_actions.osc_kramer_centreAux,
     5:  mc_actions.osc_kramer_centrePrg,
     6:  mc_actions.osc_kramer_centreNorm,
     7:  mc_actions.osc_kramer_LNvmAux,    # Lobby and Nursery from ATEM Aux
     8:  mc_actions.osc_kramer_LNvmPgm,    # Lobby and Nursery from ATEM Pgm
     9:  mc_actions.osc_kramer_status,
     13: mc_actions.osc_kramer_centrems,
     14: mc_actions.osc_kramer_LNms,

     10: pc_actions.projector_status,
     11: pc_actions.osc_projector_on,
     12: pc_actions.osc_projector_off
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

    # Associate Python functions with message address patterns, using default
    # argument scheme OSCARG_DATAUNPACK.

    print("\tOSC Addr\tAction")

    # TODO rather than an explict OSC subscrioption for every event type ...
    ## extend the not_registered handler so that is dispatches to a standard handler based on config

    for k in osc_map.keys():
        addr = "/" + str(config.parms["qlc_universe"]) + "/dmx/" + str(k)
        func = osc_map[ k ]
        print(addr, func.__name__, sep='\t') #TODO remove after core engine is working

    osc_method("/2/dmx/*",  osc_event_handler , argscheme=osm.OSCARG_MESSAGEUNPACK)

    # Periodically call osc4py3 processing method in your event loop.
    finished = False
    while not finished:
        osc_process()
        time.sleep(.1)
        # a good spot to put in a pause - (1/10th of a second) trade off between repsonse time and cpu burn.

    # Properly close the osc system.
    osc_terminate()

    print(ts(), "CueCommander Execution normal termination.\n")

main()

##
## Notes
##

# What I know about midi messages.
#       midi_status:  use p1=144 of my laptop and p1=176 for CDWU-0009
# todo need to figure out where QLC specs 144 or 176
#       we want to use the input "IAC Driver Bus 1"
#       we only handle "note velocity" events
#       midi status identifies between "Note Velocity", "Control Change' and 'Program Change'
#       Note Velocity => 144
#       Control Change => 176
#       Program Change => 192