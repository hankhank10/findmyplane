import requests
import time
import random  #only need this for testing
from SimConnect import *

def request_new_plane_instance ():
    print ("Attempting to connecting to server to request new plane instance...")

    try:
        new_plane_request = requests.get(website_address + "/api/create_new_plane")
    except requests.exceptions.RequestException as e:
        print ("... connection failed")
        return "error"

    if new_plane_request.status_code == 200:
        print("Connected to server")
    else:
        print ("... error code received from server")
        return "error"

    received_data = (new_plane_request.json())

    print ("Public key: ", received_data['ident_public_key'])
    if verbose: print ("Received private key", received_data['ident_private_key'])
    print ()

    return received_data


def update_location():

    # Get data from sim
    current_latitude = aq.get("PLANE_LATITUDE")
    current_longitude = aq.get("PLANE_LONGITUDE")
    current_altitude = aq.get("ALTITUDE")
    current_compass = round(aq.get("MAGNETIC_COMPASS"))

    data_to_send = {
        'ident_public_key': ident_public_key,
        'ident_private_key': ident_private_key,
        'current_latitude': current_latitude,
        'current_longitude': current_longitude,
        'current_compass': current_compass,
        'current_altitude': current_altitude
    }

    global datapoints_sent
    global errors_received

    if verbose: print ("Sending ", data_to_send)
    
    try:
        r = requests.post(website_address+"/api/update_plane_location", json=data_to_send)
    except:
        if verbose: print ("Error sending data")
        errors_received = errors_received + 1

    datapoints_sent = datapoints_sent + 1

    if not verbose: print (str(datapoints_sent) + " datapoints sent with " + str(errors_received) + "errors received", end='\r')

    return "ok"


def print_settings():
    print ()
    print ("# SETTINGS:")
    print ("Server address is", website_address)
    print ("Delay after failed new plane request =", str(delay_after_failed_new_plane_request))
    print ("Delay between updates =", str(delay_between_updates))
    print ()

# Settings
website_address = "http://51.195.171.71:8765"
delay_after_failed_new_plane_request = 3
delay_between_updates = 2
test_mode = True  #testing only
verbose = True

datapoints_sent = 0
errors_received = 0

print ("")
print ("")
print ("Find My Plane client starting")
print ()
print_settings()

# Connect to sim here
print ("Attempting to connect to MSFS 2020...")
try:
    sm = SimConnect()
    aq = AircraftRequests(sm, _time=10)
except:
    print ("... no sim found")
    exit()

print ("... connected to MSFS 2020")
print ()

# Request new plane instance from the server
if test_mode:
    print("# LAUNCHING IN TEST MODE")
    ident_public_key = "QDSDX"
    ident_private_key = "LfN_uXQMtJCAThKY5ZkfJn_V8Dw"
else:
    print("# CONNECT TO SERVER")
    received_plane_details = "error"
    while received_plane_details == "error":
        received_plane_details = request_new_plane_instance()
        if received_plane_details == "error": time.sleep(delay_after_failed_new_plane_request)

    ident_public_key = received_plane_details['ident_public_key']
    ident_private_key = received_plane_details['ident_private_key']

print ("")
print ("Find your plane at: ", website_address + "/view/" + ident_public_key)
print ("")

# Report the info to the server
run_forever = True
while run_forever:
    update_location()
    time.sleep(delay_between_updates)
