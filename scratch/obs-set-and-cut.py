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

async def main():

    async with OBSWS('localhost', 4444, "") as obsws:

        for s in scenes:
            response = await obsws.require(SetCurrentSceneRequest(scene_name=s))

            # Check if everything is OK
            if response.status == ResponseStatus.OK:
                print("Scene set: ",s)
            else:
                print("Scene not set. Reason:", response.error)
            await asyncio.sleep(5)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()

