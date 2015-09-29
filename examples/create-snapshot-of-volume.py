from scaleiopy.scaleio import ScaleIO
from scaleiopy.api.scaleio.mapping.snapshotspecification import SIO_SnapshotSpecification
from pprint import pprint
import sys

# How to run:
# python create-snapshot-of-volume.py ip-to-gw user pass volume_name

sio = ScaleIO("https://" + sys.argv[1] + "/api",sys.argv[2],sys.argv[3],False,"ERROR") # HTTPS must be used as there seem to be an issue with 302 responses in Requests when using POST
    
#sio.create_volume_by_pd_name(sys.argv[4], 8192, sio.get_pd_by_name(sys.argv[5]), mapAll=True)
#pprint(sio.volumes)


snapSpec = SIO_SnapshotSpecification()
snapSpec.addVolume(sio.provisioning.get_volume_by_name(sys.argv[4]))
print "**********"
print "* Volume *"
print "**********"
pprint (sio.provisioning.get_volume_by_name(sys.argv[4]))

print "**********************"
print "Snapshot specification"
print "**********************"
pprint (snapSpec)

print "* Creating Snapshot"
#print "systemId = " + str(sio.get_system_id())
#pprint (sio.get_system_id())
result = sio.provisioning.create_snapshot(sio.get_system_id(), snapSpec)
pprint (result)
