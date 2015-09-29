# ScaleIO SDK Changelog

Authors: Magnus Nilsson & Matt Cowger

## v0.0.1
Initial code to test integration against ScaleIO API

## v0.1 (only in Master branch)
* Rewrote module significantly to use classes for nearly all objects
* Rewrote GET methods to be pore pythonic
* Added support for lookups of objects by name or ID
* Added requirements.txt
* Added setup.py
* Added README with examples
* Added .gitignore
* Changed structure of package to follow community guidelines
* Removed old examples because of rewrite of module and some of them not working (like create volumes)

## v0.2 (only in master branch, never tagged as branch)
* Create volume
* Delete Volume
* Map Volume to SDC
* Unmap volume from SDC
* Additions to Volume and SDC Class

## v0.3 (will get its own branch)
* Map to SDC(s) at the same time of creating a volume
* Auto unmap of SDC when deleting volume that have existing mappings
* Error checking (basics) - Might be pushed to v0.3+
* Make naming of methods and attributes consistent (match to ScaleIO API documentation) - Might be pushed to v0.3+
* Statistics gathering (maybe in 0.3+ likely 0.4)
* Add a changelog
* IM integration to install new cluster
* Add examples

## v0.31 (beta1)
* Create Snapshot by Volume Name
* Create Snapshot by Volume Id
* Delete Snapshot
* Expand Volume
* Clean up API call methods. Now GET and POST calls happen in own methods and all other dependencies in the module uses same methods
* Logging capabilities
* Update examples to use new logging facility
* Create ProtectionDomain (WIP)
* Delete ProtectionDomain (WIP)
* Create FaultSet (WIP)
* Delete FaultSet (WIP)
* set name functionality for FS, PD, SDC and SDS 

## v0.32 (beta2)
* Faultset folded into IM integration as it depend on removing SDS to change - Create Faultset can be done at install time
* Protection Domain Mgmt removed - Pushed to v0.4
* Remove and Manage Faultsets removed - Pushed to v0.4
* Better logging - Configurable at __init__

## v0.33 (beta3)
* Support for 1.32 - Create Volume
* PIP package - Install with: pip install ScaleIO-py
* Store API version to optimize code path for different versions - Not needed to be compatible with basic Mgmt for both 1.31 and 1.32 (need to be used for Metric collection)
* delete_volume() - Obey kwargs 'autoUnmap'
* map_volume_to_sdc() and unmap_volume_from_sdc() - Changed kwargs to 'enableMapAllSdcs'

## v0.34 (beta4) WIP
* Make logging consisent
* Error handling - Find a consistent way to return errors to caller (caller have to use try/catch???)
* Never released

## v0.4
* Restructure of code - will be backwards compatible with v0.3beta3

## v0.4+
* Unit Testing
* Add SDS
* Remove SDS
* IM integration to automate upgrade of cluster software
* IM integration to allow expansion of cluster with new nodes (SDS, SDCs
* Register/Unregister SDC in cluster
* Statistics gathering
* Move classes (at least the bigger ones) into own files