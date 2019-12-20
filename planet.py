#!/usr/bin/env python
# This python script will use the Skyfield library to calculate viewing angles($
# Any planet viewed will be automatically tweeted via a Twitter API.

from sense_hat import SenseHat
from twython import Twython
from time import sleep
import os
from skyfield.api import Topos, load

sense = SenseHat()

# The below external script will hold keys required to write to the Twitter API
execfile("/home/pi/planetfind/keys.py")
myTweet = Twython(C_key,C_secret,A_token,A_secret)

#timescale is object used to hold the position or positions of the planets
ts = load.timescale()
t = ts.now()
#creating variable to access environmetal variables from parent bash script
latitude = os.environ.get('latitude')
longitude = os.environ.get('longitude')

#initilising the package for the planets
planets = load('de421.bsp')
earth = planets['earth']
mars = planets['mars']
venus = planets['venus']
mercury = planets['mercury']
jupiter = planets['jupiter barycenter']
neptune = planets['neptune barycenter']
uranus = planets['uranus barycenter']
saturn = planets['saturn barycenter']
pluto = planets['pluto barycenter']

# Creating a string array that will be called for the LED menu on the Pi. 
solarSystem = ["mars","venus","mercury","jupiter","neptune","uranus","saturn","pluto"]
# Creating an object array of the initialized planets from the skyfield package.
system = [mars,venus,mercury,jupiter, neptune, uranus, saturn, pluto]

# Clear the LED display of any former patterns
sense.clear()

# Creating a menu for the user via a while loop.
def menu(sense,solarSystem):
  i=0
  sense.show_message("Choose a planet")
  while True:
    # Show the first planet in the Solar System array
    sense.show_message(solarSystem[i])
    evt = None
    while not evt:
        evt = sense.stick.wait_for_event()
        print evt
        # If statement to determine which key on the sense joystick was pressed
        if evt.action == 'pressed': 
            # If the joytick is toggled left show the respective planet in the array
	    if evt.direction == "left":
               i = (i - 1) % len(solarSystem)
            # # If the joytick is toggled right show the respective planet in the array
            elif evt.direction == "right":
               i = (i + 1) % len(solarSystem)
            # If middle button is pressed the user has selected the planet they wish to receive viewing coordinates for
            elif evt.direction == "middle":
	       return i
	       break	
        else:
          evt = None 



selectedPlanet = None
altitude = None
azimuth = None
while True:
  i = menu(sense,solarSystem)
  # initializing selected planet from object array.
  selectedPlanet = system[i]
  # initializing planet name from string array.
  planetName = solarSystem[i]
  # creating variable that creates the users location on earth. Taking in latitude and longitude data received from Blynk 
  myLocation = earth + Topos("{} N".format(latitude),"{} E".format(longitude))
  # creating the astrometric position that is needed by Skyfield to derive the apparent position
  astro = myLocation.at(t).observe(selectedPlanet)
  # assigning apparent function to variable. This will provide us with the altitude(latitude) and azimuth(longitude) which would be used to calculate the viewing position in the sky.
  app = astro.apparent()
  alt, az, distance = app.altaz()
  altitude = alt.dstr()
  azimuth = az.dstr()
  print(alt.dstr())
  print(az.dstr())
  # Displaying calculations on the LEDs
  if selectedPlanet is not None:
     sense.show_message("You have selected {}".format(planetName), text_colour=[255, 0, 0])
     sense.show_message("altitude is {}".format(altitude), text_colour=[255, 0, 0])
     sense.show_message("azimuth is {}".format(azimuth), text_colour=[255, 0, 0])
     sleep(2)
     # Tywthon is being used to update the status on my spaceviewerPi API automatically. 
     myTweet.update_status(status="I am currently at latitude {} and longitude {}. I am viewing {} at altitude {} and azimuth {}.".format(latitude,longitude,planetName,altitude,azimuth))
     evt = None
     while not evt:
        # Allow the user to run the menu again by pressing up or alternatively shutdown the Pi by holding the joystick down
        sense.show_message("press down to quit")
        evt = sense.stick.wait_for_event(emptybuffer=True)
        if evt.action == 'pressed':
          if evt.direction == "up":
             menu(sense,solarSystem)
        elif evt.action == 'held':
          if evt.direction == "down": 
             os.system("sudo shutdown -h now")
        else: sense.stick.wait_for_event(emptybuffer=True) 

 
