from scaleiopy import scaleio
import logging
from pprint import pprint
import sys


logging.basicConfig(format='%(asctime)s: %(levelname)s %(module)s:%(funcName)s | %(message)s', level=logging.DEBUG)
sio = scaleio.ScaleIO("https://" + sys.argv[1] + "/api",sys.argv[2], sys.argv[3] ,verify_ssl=False) # HTTPS must be used as there seem to be an issue with 302 responses in Requests when using POST
pprint(sio.system)
pprint(sio.sdc)
pprint(sio.sds)
pprint(sio.volumes)
pprint(sio.protection_domains)
