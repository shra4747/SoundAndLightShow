# Import the OpenDMX or uDMX controller from PyDMXControl,
#  this will be how the data is outputted.
from PyDMXControl.controllers import OpenDMXController

# Import the fixture profile we will use,
from PyDMXControl.profiles.Generic import Dimmer
import time
import random
import threading


def thread_task(light, threadName):
    while True:
        light.dim(random.randrange(1, 7)*35)
        time.sleep(1)


dmx = OpenDMXController()

fixture1 = dmx.add_fixture(Dimmer, name="Light1")
fixture2 = dmx.add_fixture(Dimmer, name="Light2")
fixture3 = dmx.add_fixture(Dimmer, name="Light3")
fixture4 = dmx.add_fixture(Dimmer, name="Light4")
fixture5 = dmx.add_fixture(Dimmer, name="Light5")
fixture6 = dmx.add_fixture(Dimmer, name="Light6")

if __name__ == "__main__":
    # creating thread
    t1 = threading.Thread(target=thread_task, args=(fixture1, "1"))
    t2 = threading.Thread(target=thread_task, args=(fixture2, "2"))
    t3 = threading.Thread(target=thread_task, args=(fixture3, "3"))
    t4 = threading.Thread(target=thread_task, args=(fixture4, "4"))
    t5 = threading.Thread(target=thread_task, args=(fixture5, "5"))
    t6 = threading.Thread(target=thread_task, args=(fixture6, "6"))

    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()

    # starting thread 2
    # t2.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    t6.join()

    dmx.close()
    print("Done!")
