from SimConnect import *
import time

print ("Attempting to connect to MSFS 2020...")
sm = SimConnect()
aq = AircraftRequests(sm, _time=10)
print ("... connected to MSFS 2020")

run_forever = True

while run_forever:

    current_latitude = aq.get("PLANE_LATITUDE")
    current_longitude = aq.get("PLANE_LONGITUDE")
    current_altitude = aq.get("ALTITUDE")
    current_compass = round(aq.get("MAGNETIC_COMPASS"))

    print (str(current_latitude) + ", " + str(current_longitude))
    time.sleep(1)