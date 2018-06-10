
import asyncio

import time
#from threading \
import threading


class myThread ( threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
   def run(self):
      print ("Starting " + self.name)
      test1(.5)
      print ("Exiting " + self.name)

def test1(t):
    for i in range(1,10):
        print(i)
        time.sleep(t)

thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 2)

# Start new Threads
thread1.start()
thread2.start()

thread1.join()
thread2.join()

print ("Exiting Main Thread")

