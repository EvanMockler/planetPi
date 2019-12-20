# planetPi

This project entails the utilization of Blynk IoT and a Raspberry Pi with SenseHat as a tool to calculate the viewing angles
(altitude & azimuth) for a planet based on your mobile device location.

This application works in conjunction with the Blynk app (https://blynk.io/) for mobile devices. The virtual pin selected for 
the GPS stream widget in the app will need to be matched with the code here or customised bespoke. The token received from 
Blynk will also have to be changed.
Similarly the Twython keys in the key.py file will have to be swapped out for the respective keys provided to the user when 
setting up a developer API with Twitter.

As a note files deltat.data, deltat.preds,de421.bsp and Leap_Second.dat are part of the Skyfield API library (found at https://rhodesmill.org/skyfield/). This commit only utilises de421.bsp due to only requiring current coordinates of respective planets.

The core script for running the app is path.sh. This script is a bash script that calls location.py and planet.py. Also 
included is the cron job that is currently running on my pi to start the app on boot.
The keys.py script holds keys that allow the app to write to Twitter.

When running on my pi I have placed the following files in the path /home/pi/planetfind : 
Leap_Second.dat 
de421.bsp
deltat.data 
deltat.preds 
keys.py
location.py
path.sh
planet.py

I mention this as I have some paths in the code would have to be customized to account for this.

Please see DEMO available as https://youtu.be/xvDwJASyOjM
