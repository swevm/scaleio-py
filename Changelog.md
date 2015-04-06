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
* Statistics gathering (maybe in 0.3+)
* Add a changelog
* IM integration to install new cluster
* Add examples

## v0.3+
* Unit Testing
* Add SDS
* Remove SDS
* IM integration to automate upgrade of cluster software
* IM integration to allow expansion of cluster with new nodes (SDS, SDCs
* Register/Unregister SDC in cluster
* Statistics gathering
* Move classes (at least the bigger ones) into own files

