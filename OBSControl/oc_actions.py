"""
Executes actions intended for OBS.
The Scenes in the scenes dictionary must exists in the active scene collection in the instance of obs.
OBS must have the web socket plugin installed.
"""

from Config import config
import asyncio
from obswsrc import OBSWS
from obswsrc.requests import ResponseStatus
from obswsrc.requests import SetCurrentSceneRequest

scenes = {
    "00": "00 black",
    "01": "01 Announcement NoClock",
    "02": "02 Announcement Clock",
    "03": "03 ProP SD Lyrics",
    "04": "04 SeriesGraphic",
    #"98": "99 BMD intense",
    #"99": "99 Web Presenter"
}

obs_ip      = config.parms[ "obs_ip" ]    #"127.0.0.1"
obs_port    = config.parms[ "obs_port" ]    #4444

async def setscene(scene):

    async with OBSWS(obs_ip, obs_port, "") as obsws:

        response = await obsws.require(SetCurrentSceneRequest(scene_name=scene))

        # Check if everything is OK
        if response.status == ResponseStatus.OK:
            result = "Scene set: " + scene
            status = "ok"
        else:
            result = "Scene " + scene + " not set. Reason:" + response.error
            status = "error"

        res = {"status": status, "result": result}

        return(res)


def action_util(action, scene):
    """Executes template code for action execution. """

    #print("action_util", scene)
    if action:
        try:

            loop = asyncio.get_event_loop()
            res = loop.run_until_complete(setscene(scene))
            #print("loop result", res)
            # don't close the loop as the second scene change will break

            result = res["result"]
            status = res["status"]

        except Exception as e:
            result = ["Failed:" + e.strerror]
            status = "exception"
    else:
        status = "ok"
        result = ["No Action"]

    res = {"status": status, "result": result}
    #print("action util return", res)
    return(res)


def obs_black(action, value):
    """query video matrix switch status"""
    return (action_util(action, scenes["00"]  ))

def obs_announce_noclock(action, value):
    """query video matrix switch status"""
    return (action_util(action, scenes["01"]  ))

def obs_announce_clock(action, value):
    """query video matrix switch status"""
    return (action_util(action, scenes["02"]  ))

def obs_prop_lyrics(action, value):
    """query video matrix switch status"""
    return (action_util(action, scenes["03"]  ))

def obs_series_graphic(action, value):
    """query video matrix switch status"""
    return (action_util(action, scenes["04"]  ))