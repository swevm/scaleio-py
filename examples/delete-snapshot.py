from scaleiopy import *
import logging
from pprint import pprint
import sys

# How to run:
# python create-snapshot-of-volume.py ip-to-gw user pass consistency_group_id

logging.basicConfig(format='%(asctime)s: %(levelname)s %(module)s:%(funcName)s | %(message)s', level=logging.DEBUG)
sio = scaleio.ScaleIO("https://" + sys.argv[1] + "/api",sys.argv[2],sys.argv[3],verify_ssl=False)

print "* Delete Snapshot"
result = sio.delete_snapshot(sio.get_system_id(), sys.argv[4])
pprint (result)


