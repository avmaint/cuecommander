"""This package is responsible for the communications with the projection system.
The current implementaton works with our Sony projectors. In the future support for the Hitachi will be added.
"""

from Config import config
import pysdcp #https://github.com/Galala7/pySDCP

def sony_set_power(on_off : bool):
    """Turn the Sony projectors on"""
    res=[]
    for k in config.prj_ip.keys():
        ip = config.prj_ip[k]
        try:
            p = pysdcp.Projector(ip)
            p.set_power(on_off)
            r =  p.get_power()
        except Exception as e:
            result = ["Failed:" + e.strerror]
            status = "exception"
            r = "unknown"

        res = res + [{"ip" : ip , "power" : r} ]

    return(res)

def sony_get_power( ):
    """Query projector power status"""
    res=[]
    for k in config.prj_ip.keys():
        ip = config.prj_ip[k]
        p = pysdcp.Projector(ip)
        res = res + [{"ip" : ip , "power" : p.get_power()} ]
    return(res)


def projector_status(action: bool, value):
    """Enquire on the power status of the projectors."""

    if action:
        try:
            result = sony_get_power()
            status = "ok"
        except Exception as e:
            result = ["Failed:" + e.strerror]
            status = "exception"
    else:
        result = ["No action"]
        status = "ok"

    res = { "status" : status, "result": result }
    return(res)


def projector_on(action: bool, value):
    """Turn on the projectors."""

    if action:
        try:
            result = sony_set_power(True)
            status = "ok"
        except Exception as e:
            result = ["Failed:" + e.strerror]
            status = "exception"
    else:
        status = "ok"
        result = ["No Action"]

    res = { "status" : status, "result": result }
    return(res)


def projector_off(action: bool, value):
    """Turn off the projectors."""

    if action:
        try:
            result = sony_set_power(False)
            status="ok"
        except Exception as e:
            result = ["Failed:" + e.strerror]
            status = "exception"
    else:
        status = "ok"
        result = ["No Action"]

    res = { "status" : status, "result": result }
    return(res)