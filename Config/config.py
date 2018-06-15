
from pathlib          import Path
import socket

#todo move parms to external config file. Look at StageDisplay.py in the propresenter code as an example.
# parms_1 = {
#     "ip"    : "127.0.0.1",
#     "port"  : 9002 ,
#     "sname" : "aservername",
#     "cname" : "aclient",
#     "universe" : 2
# }

# parms holds constants that may have different values based on the system it runs on.
parms_all = {

    #Terry's laptop
    "argon-mba.home" : {
        "dir"           : Path("~/Dropbox/UAC_Audio/"),
        "midi_device_name" : "IAC Driver Bus 1",
        "midi_status"   : 144,
        "osc_ip"        : "127.0.0.1",
        "osc_port"      : 9002,
        "osc_sname"     : "cc",
        "qlc_universe"  : 2,
        "atemOsc_ip"    : "127.0.0.1", # loop back to CueCommander for unit test
        "atemOsc_port"  : 9002,
        "atemOsc_cn"    : "atemOSC",
        "obs_ip"        : "127.0.0.1",
        "obs_port"      : 5555
    },

    # windows machine in the balcony
    "CDWU-0009" : {
        "dir"         : Path("~/Dropbox/UAC_Audio/"),
        "device_name" : "loopMIDI Port",
        "midi_status" : 176,
        "osc_ip"      : "127.0.0.1",
        "osc_port"    : 9002,
        "osc_sname"   : "cc",
        "qlc_universe": 2,
        "atemOsc_ip": "192.168.0.164",  # loop back to CueCommander for unit test
        "atemOsc_port": 3333,
        "atemOsc_cn": "atemOSC",
        "obs_ip"        : "192.168.0.164",
        "obs_port"      : 5555

    }
}

vs88dt = { # The kramer matrix switch
    "ip" : "192.168.0.184",
    "port" : 5000
}

prj_ip = {
    "east" : "192.168.0.193",
    "cent" : "192.168.0.194",
    "west" : "192.168.0.195",
    #"rear" : "192.168.0.183" # Hitachi
}
#todo figure out why Hitachi is not responding


this_host = socket.gethostname()

parms = parms_all[this_host]