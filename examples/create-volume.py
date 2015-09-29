from scaleiopy.scaleio import ScaleIO
from pprint import pprint
import sys

# How to run:
# python create-volume.py ip-to-mdm user pass volume_name size_mb protection_domain_name storage_pool_name
# Minimal volume size is 8192MB, 8GB and then increments of 8GB
# Whats this code doing:
# Create a volume of x MB inside specified protectiondomain and storagepool
sio = ScaleIO("https://" + sys.argv[1] + "/api",sys.argv[2],sys.argv[3],False,"ERROR") # HTTPS must be used as there seem to be an issue with 302 responses in Requests when using POST
sio.provisioning.create_volume(sys.argv[4], sys.argv[5], sio.cluster_pd.get_pd_by_name(sys.argv[6]), sio.cluster_sp.get_storage_pool_by_name(sys.argv[7]))
pprint (sio.cluster_pd.get_pd_by_name(sys.argv[6]))
pprint (sio.cluster_sp.get_storage_pool_by_name(sys.argv[7]))
pprint(sio.volumes)
