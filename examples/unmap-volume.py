from scaleiopy.scaleio import ScaleIO
from pprint import pprint
import sys

# How to run:
# python unmap-volume.py ip-to-mdm user pass volume_name sdc_ip

# Whats this code doing:
# Unmaps specified volume from specified SDC IP

sio = ScaleIO("https://" + sys.argv[1] + "/api",sys.argv[2],sys.argv[3],False, "ERROR") # HTTPS must be used as there seem to be an issue with 302 responses in Requests when using POST
  
sio.unmap_volume_from_sdc(sio.get_volume_by_name(sys.argv[4]), sio.get_sdc_by_ip(sys.argv[5]))