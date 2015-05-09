from scaleiopy import im
from scaleiopy import scaleioobject as sioobj
#from scaleio import installerfsm as instfsm
import time
import json
from pprint import pprint

###########################
# Create a ScaleIO System #
###########################
#
# Prereq: 3 x CentOS 6.5 or RHEL 6.5
#
# Flow:
# Create Nodes
# Create basic info. mdmPass, liaPass and some others
# Construct MDM and TB and basic info
# Create list of SDS
# Create list of SDC


###################
# Construct nodes #
###################
nodeUsername = 'root' # Username for ScaleIO Node OS (these machines need to be pre installed)
nodePassword = 'vagrant' # Password for ScaleIO Node OS
node1 = sioobj.ScaleIO_Node_Object(None, None, ['192.168.102.11'], None, 'linux', nodePassword, nodeUsername)
node2 = sioobj.ScaleIO_Node_Object(None, None, ['192.168.102.12'], None, 'linux', nodePassword, nodeUsername)
node3 = sioobj.ScaleIO_Node_Object(None, None, ['192.168.102.13'], None, 'linux', nodePassword, nodeUsername)
    
##########################################
# Construct basic info for System_Object #
##########################################
mdmIPs = ['192.168.102.12','192.168.102.13']
sdcList = []
sdsList = []
mdmPassword = 'Scaleio123'
liaPassword = 'Scaleio123'
licenseKey = None
installationId = None

########################################
# Create MDMs and TB for System_Object #
########################################
primaryMdm = sioobj.Mdm_Object(json.loads(node2.to_JSON()), None, None, node2.nodeIPs)
secondaryMdm = sioobj.Mdm_Object(json.loads(node3.to_JSON()), None, None, node3.nodeIPs)
tb = sioobj.Tb_Object(json.loads(node1.to_JSON()), None, node1.nodeIPs)
callHomeConfiguration = None # {'callHomeConfiguration':'None'}
remoteSyslogConfiguration = None # {'remoteSysogConfiguration':'None'}

################################################################
#Create SDS objects - To be added to SDS list in System_Object #
################################################################
# Adjust addDevice() to match local block device you have in your node
# Define SDS that belong to a FaultSet - Not tested!
#sds1 = sioobj.Sds_Object(json.loads(node1.to_JSON()), None, 'SDS_' + str(node1.nodeIPs[0]), 'default', 'faultset1', node1.nodeIPs, None, None, None, False, '7072')

sds1 = sioobj.Sds_Object(json.loads(node1.to_JSON()), None, 'SDS_' + str(node1.nodeIPs[0]), 'default', 'faultset1', node1.nodeIPs, None, None, None, False, '7072')
sds1.addDevice("/home/vagrant/scaleio1", None, None)
sds2 = sioobj.Sds_Object(json.loads(node2.to_JSON()), None, 'SDS_' + str(node2.nodeIPs[0]), 'default', 'faultset2', node2.nodeIPs, None, None, None, False, '7072')
sds2.addDevice("/home/vagrant/scaleio1", None, None)
sds3 = sioobj.Sds_Object(json.loads(node3.to_JSON()), None, 'SDS_' + str(node3.nodeIPs[0]), 'default', 'faultset3', node3.nodeIPs, None, None, None, False, '7072')
sds3.addDevice("/home/vagrant/scaleio1", None, None)
sdsList.append(json.loads(sds1.to_JSON()))
sdsList.append(json.loads(sds2.to_JSON()))
sdsList.append(json.loads(sds3.to_JSON()))

#############################################################
# Create SDC objects - To be added as list to System_Object #
#############################################################
# Decide which nodes in your cluster should become a SDC
"""
node=None,
nodeInfo=None,
splitterRpaIp=None
"""
sdc1 = sioobj.Sdc_Object(json.loads(node1.to_JSON()), None, None)
sdc2 = sioobj.Sdc_Object(json.loads(node2.to_JSON()), None, None)
sdc3 = sioobj.Sdc_Object(json.loads(node3.to_JSON()), None, None)

sdcList.append(json.loads(sdc1.to_JSON()))
sdcList.append(json.loads(sdc2.to_JSON()))
sdcList.append(json.loads(sdc3.to_JSON()))

######################################################
# Construct a complete ScaleIO cluster configuration #
######################################################
sioobj = sioobj.ScaleIO_System_Object(installationId,
                               mdmIPs,
                               mdmPassword,
                               liaPassword,
                               licenseKey,
                               json.loads(primaryMdm.to_JSON()),
                               json.loads(secondaryMdm.to_JSON()),
                               json.loads(tb.to_JSON()),
                               sdsList,
                               sdcList,
                               callHomeConfiguration,
                               remoteSyslogConfiguration
                               )

# Export sioobj to JSON (should upload clean in IM)


###########################################################################
# Push System_Object JSON - To be used by IM to install ScaleIO on nodes #
###########################################################################



#######################
# LOGIN TO SCALEIO IM #
#######################
imconn = im.Im("https://192.168.102.12","admin","Scaleio123",verify_ssl=False) # "Password1!") # HTTPS must be used as there seem to be an issue with 302 responses in Requests when using POST
imconn._login()

### UPLOAD RPM PACKAGES TO BE DEPLOYED BY IM ###
imconn.uploadPackages('/Users/swevm/Downloads/RHEL6_1277/') # Adjust to your needs. All RPMs for RHEL6 should exist in this dir except for GUI and Gateway

####################
# INSTALLER STAGES #
####################

# Initialize Installer
im_installer = im.InstallerFSM(imconn, True)

time.sleep(10) # Wait a few seconds before continuing - Not necessary

print "Create minimal cluster as Python objects"
imconn.push_cluster_configuration(sioobj.to_JSON())

print "Start Install process!!!"
im_installer.Execute() # Start install process
