from scaleiopy.scaleio import ScaleIO
from pprint import pprint
import sys

# How to run:
# python map-volume.py ip-to-mdm user pass volume_name sdc_ip

# Whats this code doing:
# Maps specified volume to ip address of specified SDC

sio = scaleio.ScaleIO("https://" + sys.argv[1] + "/api",sys.argv[2],sys.argv[3],False,"ERROR") # HTTPS must be used as there seem to be an issue with 302 responses in Requests when using POST
      
sio.map_volume_to_sdc(sio.get_volume_by_name(sys.argv[4]), sio.get_sdc_by_ip(sys.argv[5]), True)

