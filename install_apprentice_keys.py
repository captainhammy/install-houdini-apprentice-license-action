"""This script is used to get and install non-commercial Houdini licenses."""

# Standard Library
import socket
import subprocess
import sys

# SideFX
import sidefx

# Parse the args from the action execution.
client_id = sys.argv[1]
client_secret_key = sys.argv[2]
houdini_version = sys.argv[3]

result = subprocess.check_output(["sesictrl", "print-server"])
server_code = result.decode().split("\n")[1].split()[2]

server_name = socket.getfqdn()

service = sidefx.service(
    access_token_url="https://www.sidefx.com/oauth2/application_token",
    client_id=client_id,
    client_secret_key=client_secret_key,
    endpoint_url="https://www.sidefx.com/api/",
)

license_strings = service.license.get_non_commercial_license(
    server_name=server_name, server_code=server_code, version=houdini_version, products='HOUDINI-NC'
)

for key in license_strings["license_keys"]:
    print("Installing", key)
    subprocess.call(["sesictrl", "install", key])

