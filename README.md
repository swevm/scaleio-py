# ScaleIO-py

#### A Python module for interacting with the EMC ScaleIO 1.3+ REST API.

Authors: Magnus Nilsson & Matt Cowger

Requirements:

* Python 2.7+
* [Requests](http://docs.python-requests.org/en/latest/)
* [Requests-Toolbelt](https://github.com/sigmavirus24/requests-toolbelt)
* ScaleIO 1.3 or 1.31 installation with REST API Gateway configured (note, the [Vagrantfile](https://github.com/virtualswede/vagrant-scaleio) from @virtualswede works fine to deploy ScaleIO with for development and testing)

## Module status
Goal is to resemble the ScaleIO API (not in detail) in a Pythonic way. Atm ScaleIO-py is in early beta stage and focus will be on getting basic features become stable (especially the to/from object mapping) before adding fancy functionality. 

### UPDATE 2015-06-06: Provisioning of ScaleIO cluster using IM works but there are issues with ScaleIO cluster mgmt once installed. Am workin on adopting code so it work correctly in 1.32 as well. for example create a new volume and map to host do not work. Many other may work bu I have´t tested yet.


## Installation
* git clone https://github.com/swevm/scaleio-py.git
* cd scaleio-py
* python setup.py install


## Supported CRUD functionality
### Retrieve methods
* Get list of SDS objects
* Get list of SDC objects
* Get list of Protection Domain objects
* Get list of Volume objects
* Get lsit of Fault Set objects
* Get list of Storage Pool objects
* Get list of System objects
* Get volume by id or name
* Get SDC by id, name or ip
* Get SDS by id, name or ip
* Get Storage Pool by id or name
* Get Protection Domain by id or name
* Get Volume by id or name
* Get list of SDC(s) mapped to Volume by volumeObject

### Create
* Create Volume by Protection Domain name [rename??] (Take PD object not PD name as argument)
* Map Volume to SDC
* Map Volume to all SDCs
* Unmap Volume from SDC
* Install new ScaleIO cluster (binaries and basic configuration using IM API)
* Create Faultset
* Create Volume snapshot

### Delete
* Delete Volume
* Delete Volume snapshot (by Volume Object) [Need testing]
* Delete SDC from cluster (same as unregister SDC from cluster) [remove one of them]
* Create Volume snapshot byt System id [Need testing]

### Update
* Set SDC name
* Upload binaries to be installed by IM


## Code examples
Have a look in examples directory for complete code examples.

### Connect to ScaleIO API
```
from scaleiopy import scaleio
# Logging level can be change by adjusting last parameter [DEBUG, FATAL, ERROR, CRITICAL, WARNING, INFO]. If left out of class init DEBUG is assumed
sio = scaleio.ScaleIO("https://192.168.50.12/api","admin","Scaleio123",False, "ERROR)
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

#### Create a new Volume in Protection Domain
```
#Create a new Volume (of 8192Mb, smallest possible)
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

#### Create Snapshot of Volume
```
snapSpec = scaleio.SnapshotSpecification()
snapSpec.addVolume(sio.get_volume_by_name('volume_name'))
sio.create_snapshot(sio.get_system_id(), snapSpec)
```

#### Delete Snapshot
```
# Consistency group Id can be found by parsing result from get_volume_by_name().
sio.delete_snapshot(sio.get_system_id(), 'consistency_group_id')
```

### Install ScaleIO using IM API
```
#Install cluster using 'private' IM API
#Look in examples/install-cluster-mac.py for a complete example
```
