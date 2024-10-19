from PyDMXControl.controllers import OpenDMXController
# from PyDMXControl.controllers import uDMXController

# Import the fixture profile we will use,
#  the simple Dimmer in this example.
from PyDMXControl.profiles.Generic import Dimmer
from PyDMXControl.profiles.Generic import RGB_Vdim

# Create an instance of the uDMX controller,
#  this holds all the fixture information and outputs it.
# This will start outputting data immediately.
dmx = OpenDMXController()
# dmx = uDMXController()

# Add a new Dimmer fixture to our controller
#  and save it to a variable so we can access it.
# We give it a name so it's easier to identify in the debug control options.
# Next, dim the intensity of the fixture from it's initial value of zero
fixture = dmx.add_fixture(RGB_Vdim, name="My_First_Dimmer")
#  to full, which is represented as 255 in DMX.
# This is done over 5000 milliseconds, or 5 seconds.
fixture.set_vdim(100)
# We can now start the web control panel built into PyDMXControl.
# This will output the web address in console, but should be http://0.0.0.0:8080
# This runs in the background and so we can continue to do other things still.
dmx.web_control()
dmx.debug_control()

# Once the console debug mode is exited the script will continue, to stop it
#  exiting and stopping DMX output when can use a built-in sleep function.
# This sleep function will wait until enter is pressed in the console before continuing.
dmx.sleep_till_enter()

# With everything done, you can terminate the DMX output and the program by calling
#  the close method of the controller.
# This will cleanly close any threads in use and stop DMX output.
dmx.close()
