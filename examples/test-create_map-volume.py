from scaleiopy import scaleio
import logging
from pprint import pprint
import sys

# How to run:
# python create_map-volume.py ip-to-mdm user pass volume_name protection_domain_name sizeInMb

# Whats this code doing:
# Create a volume of XYZ Mb (minimum 8192) inside specified protectiondomain and map it to all registered SDCs. Create volume as thin.

logging.basicConfig(format='%(asctime)s: %(levelname)s %(module)s:%(funcName)s | %(message)s', level=logging.WARNING)
sio = scaleio.ScaleIO("https://" + sys.argv[1] + "/api",sys.argv[2],sys.argv[3],verify_ssl=False) # HTTPS must be used as there seem to be an issue with 302 responses in Requests when using POST
    
sio.create_volume_by_pd_name(sys.argv[4], int(sys.argv[6]), sio.get_pd_by_name(sys.argv[5]), True, mapAll=True)
pprint(sio.volumes)
