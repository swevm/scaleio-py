from scaleiopy import *
import logging
from pprint import pprint
import sys

# How to run:
# python create-snapshot-of-volume.py ip-to-gw user pass volume_name

logging.basicConfig(format='%(asctime)s: %(levelname)s %(module)s:%(funcName)s | %(message)s', level=logging.DEBUG)
sio = scaleio.ScaleIO("https://" + sys.argv[1] + "/api",sys.argv[2],sys.argv[3],verify_ssl=False) # HTTPS must be used as there seem to be an issue with 302 responses in Requests when using POST
    
#sio.create_volume_by_pd_name(sys.argv[4], 8192, sio.get_pd_by_name(sys.argv[5]), mapAll=True)
#pprint(sio.volumes)

snapSpec = scaleio.SnapshotSpecification()
snapSpec.addVolume(sio.get_volume_by_name(sys.argv[4]))
print "**********"
print "* Volume *"
print "**********"
pprint (sio.get_volume_by_name(sys.argv[4]))

print "**********************"
print "Snapshot specification"
print "**********************"
pprint (snapSpec)

print "* Creating Snapshot"
#print "systemId = " + str(sio.get_system_id())
#pprint (sio.get_system_id())
result = sio.create_snapshot(sio.get_system_id(), snapSpec)
pprint (result)
