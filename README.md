# ScaleIO-py

#### A module for interacting with the EMC ScaleIO 1.3+ REST API.

Authors: Magnus Nilsson & Matt Cowger

Requirements:

* Python 2.7+
* [Requests](http://docs.python-requests.org/en/latest/)
* [Requests-Toolbelt](https://github.com/sigmavirus24/requests-toolbelt)
* ScaleIO 1.3 or 1.31 installation with REST API Gateway configured (note, the [Vagrantfile](https://github.com/virtualswede/vagrant-scaleio) from @virtualswede works fine to deploy ScaleIO with for development and testing)


## Code examples

### Connect to ScaleIO API
```
from scaleio-py import scaleio
sio = scaleio.ScaleIO("https://192.168.50.12/api","admin","Scaleio123",verify_ssl=False)
```

#### Get a list of all attributes related to each SDC known by your ScaleIO cluster
```
#print all the known SDCs:
pprint(sio.sdc)
```

#### Get list of attributes related to all SDS
```
#print all the known SDSs:
pprint(sio.sds)
```

#### Get list of attributes related to all known Volumes
```
#print all the known Volumes:
pprint(sio.volumes)
```

#### Get list of attributes related to each protection domain
```
#print all the known Protection Domains:
pprint(sio.protection_domains)
```

#### Create a new Volume in Proctection Domain
```
#Create a new Volume
sio.create_volume_by_pd_name('testvol001', 8192, sio.get_pd_by_name('default'))

#Create Volume and Map to single SDC in one operation
sio.create_volume_by_pd_name('testvol001', 8192, sio.get_pd_by_name('default'), mapToSdc=sio.get_sdc_by_id('ce4d7e2a00000001'))

#Create Volume and Map to all SDC in one operation
sio.create_volume_by_pd_name('testvol001', 8192, sio.get_pd_by_name('default'), mapAll=True)

```

#### Map existing Volume to a SDC by its ID
```
# method get_sdc_by_ip('ipaddr') if you want to map an Vol to SDC using its IP address
sio.map_volume_to_sdc(sio.get_volume_by_name('testvol'), sio.get_sdc_by_id('ce4d7e2a00000001'), False)

# Map Volume to all SDCs
sio.map_volume_to_sdc(sio.get_volume_by_name('testvol'), mapAll=True)
```

#### Unmap volume from SDC
```
#Unmap Volume from SDC
sio.unmap_volume_from_sdc(sio.get_volume_by_name('testvol'), sio.get_sdc_by_id('ce4d7e2a00000001'))
```

#### Delete a Volume from ScaleIO cluster
```
#Delete Volume
sio.delete_volume(sio.get_volume_by_name('testvol'), 'ONLY_ME')
```

### Install ScaleIO using IM API
```
#Install cluster using 'private' IM API
#Look in examples/install-cluster-mac.py for a complete example
```