from scaleiopy import scaleio
import logging
from pprint import pprint
import sys


logging.basicConfig(format='%(asctime)s: %(levelname)s %(module)s:%(funcName)s | %(message)s', level=logging.WARNING)
sio = scaleio.ScaleIO("https://" + sys.argv[1] + "/api",sys.argv[2], sys.argv[3] ,verify_ssl=False) # HTTPS must be used as there seem to be an issue with 302 responses in Requests when using POST
print "--- ScaleIO System ---"
pprint(sio.system)
print "--- ScaleIO SDC ---"
pprint(sio.sdc)
print "--- ScaleIO SDS ---"
pprint(sio.sds)
print  "--- ScaleiO Volumes ---"
pprint(sio.volumes)
print "--- ScaleIO Protection Domains ---"
pprint(sio.protection_domains)
print "--- ScaleIO Fault Sets ---"
pprint(sio.fault_sets)