"""Example to transition to a scene."""

import asyncio
from obswsrc import OBSWS
from obswsrc.requests import ResponseStatus
from obswsrc.requests import SetCurrentSceneRequest
import time
from threading import Thread


scenes = [
    "00 black",
    "01 Announcement No Clock",
    "02 Announcement Clock",
    "03 ProP SD Lyrics",
    "04 SeriesGraphic",
    "99 BMD intense",
    "99 Web Presenter"
]

async def amain():

    async with OBSWS('localhost', 4444, "") as obsws:

        for s in scenes:
            response = await obsws.require(SetCurrentSceneRequest(scene_name=s))

            # Check if everything is OK
            if response.status == ResponseStatus.OK:
                print("Scene set: ",s)
            else:
                print("Scene not set. Reason:", response.error)
            await asyncio.sleep(5)

def smain():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(amain())
    loop.close()

thread = Thread(target=smain)
thread.start()
thread.join()
print('Finished')