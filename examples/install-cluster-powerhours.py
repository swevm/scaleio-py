from scaleio-py import im
from scaleio-py import scaleioobject as sioobj
#from scaleio import installerfsm as instfsm
import time
import json
from pprint import pprint

###########################
# Create a ScaleIO System #
###########################
# Flow:
# Create Nodes
# Create basic info. mdmPass, liaPass and some others
# Construct MDM and TB and basic info
# Create list of SDS
# Create list of SDC


###################
# Construct nodes #
###################
nodeUsername = 'root'
nodePassword = 'password'
node1 = sioobj.ScaleIO_Node_Object(None, None, ['192.168.100.61'], None, 'linux', nodePassword, nodeUsername)
node2 = sioobj.ScaleIO_Node_Object(None, None, ['192.168.100.62'], None, 'linux', nodePassword, nodeUsername)
node3 = sioobj.ScaleIO_Node_Object(None, None, ['192.168.100.63'], None, 'linux', nodePassword, nodeUsername)
#print "Node Object:"
#pprint (node1.to_JSON())
#pprint (node2.to_JSON())
#pprint (node2.to_JSON())
#print ""
    
##########################################
# Construct basic info for System_Object #
##########################################
mdmIPs = ['192.168.100.61','192.168.100.62']
sdcList = []
sdsList = []
mdmPassword = 'Scaleio123!!'
liaPassword = 'Scaleio123!!'
licenseKey = None
installationId = None

########################################
# Create MDMs and TB for System_Object #
########################################
primaryMdm = sioobj.Mdm_Object(json.loads(node1.to_JSON()), None, None, node1.nodeIPs) # WHY ISNT ManagementIPs pupulated???? Its not in a working config either. mdmIPs need to be populated though
secondaryMdm = sioobj.Mdm_Object(json.loads(node2.to_JSON()), None, None, node2.nodeIPs)
tb = sioobj.Tb_Object(json.loads(node3.to_JSON()), None, node3.nodeIPs)
callHomeConfiguration = None # {'callHomeConfiguration':'None'}
remoteSyslogConfiguration = None # {'remoteSysogConfiguration':'None'}

################################################################
#Create SDS objects - To be added to SDS list in System_Object #
################################################################
sds1 = sioobj.Sds_Object(json.loads(node1.to_JSON()), None, 'SDS_' + str(node1.nodeIPs[0]), 'default', None, node1.nodeIPs, None, None, None, False, '7072')
sds1.addDevice("/dev/sdb", None, None)
sds2 = sioobj.Sds_Object(json.loads(node2.to_JSON()), None, 'SDS_' + str(node2.nodeIPs[0]), 'default', None, node2.nodeIPs, None, None, None, False, '7072')
sds2.addDevice("/dev/sdb", None, None)
sds3 = sioobj.Sds_Object(json.loads(node3.to_JSON()), None, 'SDS_' + str(node3.nodeIPs[0]), 'default', None, node3.nodeIPs, None, None, None, False, '7072')
sds3.addDevice("/dev/sdb", None, None)
sdsList.append(json.loads(sds1.to_JSON()))
sdsList.append(json.loads(sds2.to_JSON()))
sdsList.append(json.loads(sds3.to_JSON()))
print "sdsList:"
pprint (sdsList)

#############################################################
# Create SDC objects - To be added as list to System_Object #
#############################################################
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
#pprint (sioobj.to_JSON())



#######################
# LOGIN TO SCALEIO IM #
#######################
imconn = im.Im("https://192.168.100.242","admin","Scaleio123!!",verify_ssl=False) # "Password1!") # HTTPS must be used as there seem to be an issue with 302 responses in Requests when using POST
imconn._login()

### UPLOAD RPM PACKAGES TO BE DEPLOYED BY IM ###
imconn.uploadPackages('/Users/swevm/Downloads/RHEL6_1277/') # WORKS!

####################
# INSTALLER STAGES #
####################

# Initialize Installer
im_installer = im.InstallerFSM(imconn, True)

time.sleep(10) # Wait a few seconds before continuing - Not necessary

print "Create minimal cluster as Python objects"
#imconn.create_minimal_scaleio_cluster("Scaleio123!!", "Scaleio123!!")  # Create a 3 node (minimal) ScaleIO cluster and push its definition to IM
imconn.push_cluster_configuration(sioobj.to_JSON())

print "Start Install process!!!"
im_installer.Execute() # Start install process
