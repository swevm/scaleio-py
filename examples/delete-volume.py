from scaleio-py import scaleio
import logging
from pprint import pprint
import sys

# How to run:
# python delete-volume.py ip-to-mdm user pass volume_name

# Whats this code doing:
# Unmaps specified volume from any SDCs using it and then delete the volume

logging.basicConfig(format='%(asctime)s: %(levelname)s %(module)s:%(funcName)s | %(message)s', level=logging.WARNING)
sio = scaleio.ScaleIO("https://" + sys.argv[1] + "/api",sys.argv[2],sys.argv[3],verify_ssl=False) # HTTPS must be used as there seem to be an issue with 302 responses in Requests when using POST
    
#sio.delete_volume(sio.get_volume_by_name('testvol009'), 'ONLY_ME') 
sio.delete_volume(sio.get_volume_by_name(sys.argv[4]), 'ONLY_ME', autoUnmap=True)

pprint(sio.volumes)
