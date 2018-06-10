"""
Multi-threading version to avoid event loop conflicts between osc and obs
"""

from Config import config
import asyncio
from obswsrc import OBSWS
from obswsrc.requests import ResponseStatus
from obswsrc.requests import SetCurrentSceneRequest
import threading

scenes = {
    "00": "00 black",
    "01": "01 Announcement No Clock",
    "02": "02 Announcement Clock",
    "03": "03 ProP SD Lyrics",
    "04": "04 SeriesGraphic",
    #"98": "99 BMD intense",
    #"99": "99 Web Presenter"
}

obs_ip = "127.0.0.1"
obs_port = 4444
s = scenes["03"]

async def mainx(s):
    #global s

    async with OBSWS(obs_ip, obs_port, "") as obsws:

        response = await obsws.require(SetCurrentSceneRequest(scene_name=s))

        # Check if everything is OK
        if response.status == ResponseStatus.OK:
            res = "Scene set: " + s
            #print("Scene set: ",s)
        else:
            res = "Scene " + s + " not set. Reason:" + response.error
            #print("Scene ", s, " not set. Reason:", response.error)
        print(res)
        return(res)

class myThread ( threading.Thread):
   def __init__(self, threadID, name, counter, scene):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
      self.scene = scene
   def run(self):
      print ("Starting " + self.name)
      #mainx(self.scene)
      loop = asyncio.get_event_loop()
      loop.run_until_complete(mainx(self.scene))
      loop.close()
      print ("Exiting " + self.name)


def action_util(action, cmd):
    """Executes template code for action execution. """
    global s
    print("action_util", cmd)
    if action:
        try:
            #s = cmd
            thread1 = myThread(1, "Thread-1", 1, cmd)
            thread1.start()
            thread1.join()

            #loop = asyncio.get_event_loop()
            #loop.run_until_complete(mainx())
            #loop.close()
            result = cmd
            status = "ok"
        except Exception as e:
            result = ["Failed:" + e.strerror]
            status = "exception"
    else:
        status = "ok"
        result = ["No Action"]

    res = {"status": status, "result": result}


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