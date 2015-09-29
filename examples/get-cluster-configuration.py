from scaleiopy import im
from scaleiopy import scaleioobject as sioobj
#from scaleio import installerfsm as instfsm
import time
import json
from pprint import pprint

imconn = im.Im("https://192.168.102.12","admin","Scaleio123",verify_ssl=False) # "Password1!") # HTTPS must be used as there seem to be an issue with 302 responses in Requests when using POST
imconn._login()
imconn.retrieve_scaleio_cluster_configuration("192.168.102.12", "Scaleio123", "Scaleio123")