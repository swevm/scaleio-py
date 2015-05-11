from scaleiopy import scaleio
from pprint import pprint
import sys

# How to run:
# python unmap-volume.py ip-to-mdm user pass volume_name sdc_ip

# Whats this code doing:
# Unmaps specified volume from specified SDC IP

sio = scaleio.ScaleIO("https://" + sys.argv[1] + "/api",sys.argv[2],sys.argv[3],False, "ERROR") # HTTPS must be used as there seem to be an issue with 302 responses in Requests when using POST
  
#sio.unmap_volume_from_sdc(sio.get_volume_by_name('testvol009'), sio.get_sdc_by_id('ce4d7e2a00000001'))
sio.unmap_volume_from_sdc(sio.get_volume_by_name(sys.argv[4]), sio.get_sdc_by_ip(sys.argv[5]))