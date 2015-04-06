from scaleio-py import scaleio
import logging
from pprint import pprint
import sys

# How to run:
# python create_mapall-volume.py ip-to-mdm user pass volume_name protection_domain_name

# Whats this code doing:
# Create a volume of 8GB inside specified protectiondomain and map it to all registered SDCs

logging.basicConfig(format='%(asctime)s: %(levelname)s %(module)s:%(funcName)s | %(message)s', level=logging.WARNING)
sio = scaleio.ScaleIO("https://" + sys.argv[1] + "/api",sys.argv[2],sys.argv[3],verify_ssl=False) # HTTPS must be used as there seem to be an issue with 302 responses in Requests when using POST
    
sio.create_volume_by_pd_name(sys.argv[4], 8192, sio.get_pd_by_name(sys.argv[5]), mapAll=True)

pprint(sio.volumes)
