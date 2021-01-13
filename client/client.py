import requests
import time


def request_new_plane_instance (verbose=True):
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
    if verbose:
        print ("Received public key", received_data['ident_public_key'])
        print ("Received private key", received_data['ident_private_key'])
    else:
        print ("Received key pair")
    print ()

    return received_data


def update_location():

    data_to_send = {
        'ident_public_key': ident_public_key,
        'ident_private_key': ident_private_key,
        'current_latitude': 100,
        'current_longitude': 150,
        'current_heading': 10
    }
    print ("Sending", data_to_send)

    r = requests.post(website_address+"/api/update_plane_location", json=data_to_send)

    return "ok"


def print_settings():
    print ()
    print ("# SETTINGS:")
    print ("Server address is", website_address)
    print ("Delay after failed new plane request =", str(delay_after_failed_new_plane_request))
    print ("Delay between updates =", str(delay_between_updates))
    print ()

# Settings


website_address = "http://localhost:5008"
delay_after_failed_new_plane_request = 3
delay_between_updates = 2


# Main loop


print ("")
print ("")
print ("Find My Plane client starting")
print_settings()


# Get plane details from the server

print()
print("# CONNECT TO SERVER")

received_plane_details = "error"
while received_plane_details == "error":
    received_plane_details = request_new_plane_instance()
    if received_plane_details == "error": time.sleep(delay_after_failed_new_plane_request)

ident_public_key = received_plane_details['ident_public_key']
ident_private_key = received_plane_details['ident_private_key']

# Connect to client

run_forever = True

while run_forever:
    update_location()
    time.sleep(delay_between_updates)
