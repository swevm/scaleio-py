from scaleiopy import scaleio
from pprint import pprint
import sys

# How to run:
# python create_map-volume.py ip-to-mdm user pass volume_name size_mb protection_domain_name storage_pool_name

# Whats this code doing:
# Create a volume of x MB [min 8192MB] inside specified protectiondomain and storagepool, then map it to all registered SDCs

sio = scaleio.ScaleIO("https://" + sys.argv[1] + "/api",sys.argv[2],sys.argv[3],False,"ERROR") # HTTPS must be used as there seem to be an issue with 302 responses in Requests when using POST
    
sio.create_volume(sys.argv[4], sys.argv[5], sio.get_pd_by_name(sys.argv[6]), sio.get_storage_pool_by_name(sys.argv[7]), mapAll=True)

pprint(sio.volumes)
