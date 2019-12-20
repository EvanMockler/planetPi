#!/usr/bin/env python
# This python script will be used to find my mobile phone location via the Blynk GPS streaming widget
from sense_hat import SenseHat

import os
import BlynkLib

sense = SenseHat()

auth = "GDE87IKFSXy1FG41kjtp1i7v4NoJsw9Y"
blynk=BlynkLib.Blynk(auth)


# Writing the GPS coordinates from my phone to the virtual pin within the Blynk app
@blynk.VIRTUAL_WRITE(4)
def show_location(param):
 #format the parameters received from the virtual pin and place into an environmental variable that can be accessed outside the show location function
  os.environ['latitude'] = "{} N".format(param[0])
  os.environ['longitude'] = "{} E".format(param[1])

# Creating a loop that will run until the Blynk data is written to the PIN
while True:
    blynk.run()
    # The user of the Pi will have to stand-by while the data is being transmitted
    sense.show_message("Please wait")
    if os.getenv("latitude") is not None and os.getenv("longitude") is not None:
       break

#Print the current latitude and longitude.
print(os.environ['latitude'])
print(os.environ['longitude'])




