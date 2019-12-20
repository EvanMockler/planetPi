#!/bin/sh
# This path.sh wrapper script will be used to create environmetal variables that will be passed to the child python scripts. It will be run in crontab on reboot of the pi.
export currentLocation="$(python /home/pi/planetfind/location.py)" 

# Filter the Blynk string output from location.py script into the coordinates required for calculations in planet.py script
export latitude=$(echo $currentLocation | awk '{print $27, $28}')
export longitude=$(echo $currentLocation | awk '{print $29, $30}')

echo $latitude 
echo $longitude

# Run the python script that will make planet calculations using Skyfield & run the LED menu on the sensehat.
python /home/pi/planetfind/planet.py





