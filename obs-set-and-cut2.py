"""Example to transition to a scene."""

import asyncio
from obswsrc import OBSWS
from obswsrc.requests import ResponseStatus
from obswsrc.requests import SetCurrentSceneRequest
import time

scenes = [
    "00 black",
    "01 Announcement No Clock",
    "02 Announcement Clock",
    "03 ProP SD Lyrics",
    "04 SeriesGraphic",
    "99 BMD intense",
    "99 Web Presenter"
]

def main():
    obsws = OBSWS('localhost', 4444, "")

    for s in scenes:
        response =   obsws.require(SetCurrentSceneRequest(scene_name=s))

        # Check if everything is OK
        if response.status == ResponseStatus.OK:
            print("Scene set: ",s)
        else:
            print("Scene not set. Reason:", response.error)
            time.sleep(5)

#loop = asyncio.get_event_loop()
main()

