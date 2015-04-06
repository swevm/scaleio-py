from scaleio-py import im
import time

#######################
# LOGIN TO SCALEIO IM #
#######################
imconn = im.Im("https://192.168.102.12","admin","Scaleio123",verify_ssl=False) # "Password1!") # HTTPS must be used as there seem to be an issue with 302 responses in Requests when using POST
imconn._login()

### UPLOAD RPM PACKAGES TO BE DEPLOYED BY IM ###
imconn.uploadPackages('/Users/swevm/Downloads/RHEL6_1277/') # WORKS!

####################
# INSTALLER STAGES #
####################

# Initialize Installer
im_installer = im.InstallerFSM(imconn, True)

time.sleep(10) # Wait a few seconds before continuing - Not necessary

### RUN IM INSTALL PROCESS - EXTRACT JSON CONFIG TO FIND OUT WHERE DEVICE(S) TO BE USED BY SDS NODES ARE CONFIGURED TO ALLOW CREATING A BASIC MINIMUM 3 NODE CLUSTER WITH VAGRANT
print "Create minimal cluster as Python objects"
imconn.create_minimal_scaleio_cluster("Scaleio123", "Scaleio123")  # Create a 3 node (minimal) ScaleIO cluster and push its definition to IM
print "Start Install process!!!"
im_installer.Execute() # Start install process
