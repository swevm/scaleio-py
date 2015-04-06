import json
import requests
import time
from requests.auth import HTTPBasicAuth
from requests_toolbelt import SSLAdapter
from requests_toolbelt import MultipartEncoder
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
import ssl
import logging
import time
from os import listdir
from os.path import isfile, join
import logging
from scaleioobject import *
from installerfsm import *


from pprint import pprint

class TLS1Adapter(HTTPAdapter):
    """
    A custom HTTP adapter we mount to the session to force the use of TLSv1, which is the only thing supported by
    the gateway.  Python 2.x tries to establish SSLv2/3 first which failed.
    """
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)

class Im_Generic_Object1(object):
    @classmethod
    def get_class_name(cls):
        """
        A helper method that returns the name of the class.  Used by __str__ below
        """
        return cls.__name__

    def __str__(self):
        """
        A convinience method to pretty print the contents of the class instance
        """
        # to show include all variables in sorted order
        return "<{}> @ {}:\n".format(self.get_class_name(), id(self)) + "\n".join(
            ["  %s: %s" % (key.rjust(22), self.__dict__[key]) for key in sorted(set(self.__dict__))])

    def __repr__(self):
        return self.__str__()

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def to_DICT(self):
        return self.__dict__
    
 

class Im(Im_Generic_Object):
    """
    The IM class provides a pythonic way to interact with and manage a ScaleIO cluster using Installation Manager 'private' API/
    """
    def __init__(self, api_url, username, password, verify_ssl=False, LiaPassword=None):
        """
        Initializes the class

        :param api_url: Base URL for the API.  Often the MDM host.
        :type api_url: str
        :param username: Username to login with
        :type username: str
        :param password: Password
        :type password: str
        :return: A ScaleIO object
        :rtype: ScaleIO
        """

        self._username = username
        self._password = password
        self._im_api_url = api_url
        self._im_session = requests.Session()
        #self._im_session.headers.update({'Accept': 'application/json', 'Version': '1.0'}) # Accept only json
        self._im_session.mount('https://', TLS1Adapter())
        self._im_verify_ssl = verify_ssl
        self._im_logged_in = False
        requests.packages.urllib3.disable_warnings() # Disable unverified connection warning.
        self._cluster_config_cached = None
        self._cache_contains_uncommitted = None
        
        self.SIO_Configuration_Object = None # Holds a DICT representation of the ScaleIO System Configuration

    def _get_cached_config_json(self):
        return self._cluster_config_cached
    
    def _login(self):
        """
        LOGIN CAN ONLY BE DONE BY POSTING TO A HTTP FORM.
        A COOKIE IS THEN USED FOR INTERACTING WITH THE API
        """

        self._im_session.headers.update({'Content-Type':'application/x-www-form-urlencoded', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36'})
        #self._im_session.mount('https://', TLS1Adapter())
        #self._im_verify_ssl = False
        self.j_username = self._username
        self.j_password = self._password
        requests.packages.urllib3.disable_warnings() # Disable unverified connection warning.
        payload = {'j_username': self.j_username, 'j_password': self.j_password, 'submit':'Login'}
        
        # login to ScaleIO IM
        r = self._im_session.post(
            "{}/{}".format(self._im_api_url,"j_spring_security_check"),
            verify=self._im_verify_ssl,
            #headers = {'Content-Type':'application/x-www-form-urlencoded', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36'},
            data=payload)
        print "Login method()"
        #print r.text
        self._im_logged_in = True
        logging.basicConfig(level=logging.INFO)
        
        """
        ADD CODE:
        Check if this is IM have existing configuration. If so populate ScaleIO_configurtion_object
        """
        
    def _check_login(self):
        if not self._im_logged_in:
            self._im_login()
        else:
            pass
        return None
    
    # FIX _do_get method, easier to have one place to do error handling than in all other methods that call _do_get()
    def _do_get(self, uri, **kwargs):
        """
        Convinient method for GET requests
        Returns http request status value from a POST request
        """
        #TODO:
        # Add error handling. Check for HTTP status here would be much more conveinent than in each calling method
        scaleioapi_get_headers = {'Content-type':'application/json','Version':'1.0'}
        
        if kwargs:
            for key, value in kwargs.iteritems():
                if key == 'headers':
                    scaleio_get_headersvalue = value

        try:
            #response = self._im_session.get("{}/{}".format(self._api_url, uri), headers = scaleioapi_get_headers, payload = scaleio_payload).json()
            response = self._im_session.get("{}/{}".format(self._api_url, uri), **kwargs).json()
            #response = self._session.get(url, headers=scaleioapi_post_headers, **kwargs)
            if response.status_code == requests.codes.ok:
                return response
            else:
                raise RuntimeError("_do_get() - HTTP response error" + response.status_code)
        except:
            raise RuntimeError("_do_get() - Communication error with ScaleIO gateway")
        return response

    def _do_put(self, uri, **kwargs):
        """
        Convinient method for POST requests
        Returns http request status value from a POST request
        """
        #TODO:
        # Add error handling. Check for HTTP status here would be much more conveinent than in each calling method
        scaleioapi_put_headers = {'content-type':'application/json'}
        print "_do_put()"
        if kwargs:
            for key, value in kwargs.iteritems():
                #if key == 'headers':
                #    scaleio_post_headers = value
                #    print "Adding custom PUT headers"
                if key == 'json':
                    payload = value
        try:
            #self._session.headers.update({'Content-Type':'application/json'})
            response = self._session.put(url, headers=scaleioapi_put_headers, verify_ssl=self._im_verify_ssl, data=json.dumps(payload))
            print "PUT call:"
            print response.text
            if response.status_code == requests.codes.ok:
                return response
            else:
                raise RuntimeError("_do_put() - HTTP response error" + response.status_code)
        except:
            print "PUT call response:"
            print response.text
            raise RuntimeError("_do_put() - Communication error with ScaleIO gateway")
        return response
    
    def _do_post(self, url, **kwargs):
        """
        Convinient method for POST requests
        Returns http request status value from a POST request
        """
        #TODO:
        # Add error handling. Check for HTTP status here would be much more conveinent than in each calling method
        scaleioapi_post_headers = {'Content-type':'application/json','Version':'1.0'}
        print "_dopost()"
        if kwargs:
            for key, value in kwargs.iteritems():
                if key == 'headers':
                    scaleio_post_headers = value
                    print "Adding custom POST headers"
                if key == 'files':
                    upl_files = value
                    print "Adding files to upload"
        try:
            response = self._session.post(url, headers=scaleioapi_post_headers, verify_ssl=self._im_verify_ssl, files=upl_files)
            print "POST call:"
            print response.text
            if response.status_code == requests.codes.ok:
                return response
            else:
                raise RuntimeError("_do_post() - HTTP response error" + response.status_code)
        except:
            print "POST call response:"
            print response.text
            raise RuntimeError("_do_post() - Communication error with ScaleIO gateway")
        return response
 
    def get_installation_instances(self):
        print "/types/Installation/instances/"
        resp = self._im_session.get("{}/{}".format(self._im_api_url, 'types/Installation/instances'))
        print resp.text

    def get_state(self, count=None):
        #print "/types/State/instances/"
        payload = {'_':'1425822717883'}
        referer = 'https://192.168.100.12/install.jsp'
        #resp = self._im_session.get("{}/{}".format(self._im_api_url, 'types/State/instances/'), params = payload)
        resp = self._im_session.get("{}/{}".format(self._im_api_url, 'types/State/instances/'))
        #print "URL: " + resp.url
        #print resp.text
        return resp.text
    
    def set_state(self, state):
        # state can be: query, upload, install, configure
        if state == 'query':
            resp = self._im_session.put("{}/{}".format(self._im_api_url,"types/State/instances/"),data =json.dumps({"state":"query"}), headers={'Content-Type':'application/json'})
            print "PUT Request URL: " + resp.url
            print "QUERY Response:"
            print resp.text
            return True
        if state == 'upload':
            resp = self._im_session.put("{}/{}".format(self._im_api_url,"types/State/instances/"),data =json.dumps({"state":"upload"}), headers={'Content-Type':'application/json'})
            print "PUT Request URL: " + resp.url
            print "UPLOAD Response:"
            print resp.text
            return True
        if state == 'install':
            resp = self._im_session.put("{}/{}".format(self._im_api_url,"types/State/instances/"),data =json.dumps({"state":"install"}), headers={'Content-Type':'application/json'})
            return True
            print "PUT Request URL: " + resp.url
            print "INSTALL Response:"
            print resp.text
        if state == 'configure':
            resp = self._im_session.put("{}/{}".format(self._im_api_url,"types/State/instances/"),data =json.dumps({"state":"configure"}), headers={'Content-Type':'application/json'})
            return True
            print "PUT Request URL: " + resp.url
            print "CONFIGURE Response:"
            print resp.text
        return False
    
    def set_abort_pending(self, newstate):
        """
        Method to set Abort state if something goes wrong during provisioning
        Method also used to finish provisioning process when all is completed
        Method: POST
        """
        # NOT TO BE USED
        #default_minimal_cluster_config = '{"installationId":null,"mdmIPs":["192.168.102.12","192.168.102.13"],"mdmPassword":"Scaleio123","liaPassword":"Scaleio123","licenseKey":null,"primaryMdm":{"node":{"ostype":"linux","nodeName":null,"nodeIPs":["192.168.102.12"],"domain":null,"userName":"root","password":"vagrant","liaPassword":null},"nodeInfo":null,"managementIPs":null,"mdmIPs":["192.168.102.12"]},"secondaryMdm":{"node":{"ostype":"linux","nodeName":null,"nodeIPs":["192.168.102.13"],"domain":null,"userName":"root","password":"vagrant","liaPassword":null},"nodeInfo":null,"managementIPs":null,"mdmIPs":["192.168.102.13"]},"tb":{"node":{"ostype":"linux","nodeName":null,"nodeIPs":["192.168.102.11"],"domain":null,"userName":"root","password":"vagrant","liaPassword":null},"nodeInfo":null,"tbIPs":["192.168.102.11"]},"sdsList":[{"node":{"ostype":"linux","nodeName":null,"nodeIPs":["192.168.102.11"],"domain":null,"userName":"root","password":"vagrant","liaPassword":null},"nodeInfo":null,"sdsName":"SDS_[192.168.102.11]","protectionDomain":"default","faultSet":null,"allIPs":["192.168.102.11"],"sdsOnlyIPs":null,"sdcOnlyIPs":null,"devices":[{"devicePath":"/home/vagrant/scaleio1","storagePool":null,"deviceName":null}],"optimized":false,"port":7072},{"node":{"ostype":"linux","nodeName":null,"nodeIPs":["192.168.102.12"],"domain":null,"userName":"root","password":"vagrant","liaPassword":null},"nodeInfo":null,"sdsName":"SDS_[192.168.102.12]","protectionDomain":"default","faultSet":null,"allIPs":["192.168.102.12"],"sdsOnlyIPs":null,"sdcOnlyIPs":null,"devices":[{"devicePath":"/home/vagrant/scaleio1","storagePool":null,"deviceName":null}],"optimized":false,"port":7072},{"node":{"ostype":"linux","nodeName":null,"nodeIPs":["192.168.102.13"],"domain":null,"userName":"root","password":"vagrant","liaPassword":null},"nodeInfo":null,"sdsName":"SDS_[192.168.102.13]","protectionDomain":"default","faultSet":null,"allIPs":["192.168.102.13"],"sdsOnlyIPs":null,"sdcOnlyIPs":null,"devices":[{"devicePath":"/home/vagrant/scaleio1","storagePool":null,"deviceName":null}],"optimized":false,"port":7072}],"sdcList":[{"node":{"ostype":"linux","nodeName":null,"nodeIPs":["192.168.102.11"],"domain":null,"userName":"root","password":"vagrant","liaPassword":null},"nodeInfo":null,"splitterRpaIp":null},{"node":{"ostype":"linux","nodeName":null,"nodeIPs":["192.168.102.12"],"domain":null,"userName":"root","password":"vagrant","liaPassword":null},"nodeInfo":null,"splitterRpaIp":null},{"node":{"ostype":"linux","nodeName":null,"nodeIPs":["192.168.102.13"],"domain":null,"userName":"root","password":"vagrant","liaPassword":null},"nodeInfo":null,"splitterRpaIp":null}],"callHomeConfiguration":null,"remoteSyslogConfiguration":null}'
        r1 = self._im_session.post(
            "{}/{}".format(self._im_api_url,"types/Command/instances/actions/abortPending"),
            headers={'Content-type':'application/json','Version':'1.0'}, 
            verify=self._im_verify_ssl,
            data = newstate,
            stream=True
        )
        if not r1.ok:
            # Something went wrong
            print "Error set_abort_pending()"
        
        print "Response after set_abort_pending()"
        # RESPONSE NEED TO BE WRAPPED IN try/catch. Cannot assume JSON is returned.
        print r1.text
        #pprint (json.loads(r1.text))
        return r1.text

    def set_archive_all(self):
        """
        Last method to be called when provisioning is complete
        Method: POST
        """
        r1 = self._im_session.post(
            "{}/{}".format(self._im_api_url,"types/Command/instances/actions/archiveAll"),
            headers={'Content-type':'application/json','Version':'1.0'}, 
            verify=self._im_verify_ssl,
            data = '',
            stream=True
        )
        if not r1.ok:
            # Something went wrong
            print "Error set_archive_all()"
        
        print "Response after set_archive_all()"
        # RESPONSE NEED TO BE WRAPPED IN tey/catch. Can?t assume JSON is returned.
        print r1.text
        #pprint (json.loads(r1.text))
        return r1.text

    def get_version(self):
        print "/version/"
        payload = {'_':'1425822717883'} # Investigate what this number mean when some IM API calls are done. Its used by IM Webui. Seem to be Unixtime format.
        referer = 'https://192.168.100.12/status.jsp'
        resp = self._im_session.get("{}/{}".format(self._im_api_url, 'version/'), params = payload)
        print "URL: " + resp.url
        print resp.text    
        
    def get_installation_packages_latest(self):
        """
        In 1.31-256 getting latest or all packages seem not to work. Always same result not matter what value 'onlLatest' have. Same situation in IM WEBUI too.
        """
        parameter = {'onlyLatest':'False'}
        resp = self._im_session.get("{}/{}".format(self._im_api_url, 'types/InstallationPackageWithLatest/instances'), params=parameter)
        #resp = self._im_session.get('https://192.168.100.52/types/InstallationPackageWithLatest/instances', params=parameter)
        jresp = json.loads(resp.text)

        pprint(jresp)

    def get_installation_packages(self):
        """
        In 1.31-256 getting latest or all packages seem not to work. Always same result not matter what value 'onlLatest' have. Same situation in IM WEBUI too.
        """
        parameter = {'onlyLatest':'False'}
        resp = self._im_session.get("{}/{}".format(self._im_api_url, 'types/InstallationPackageWithLatest/instances'), params=parameter)
        #resp = self._im_session.get('https://192.168.100.52/types/InstallationPackageWithLatest/instances', params=parameter)
        jresp = json.loads(resp.text)
        pprint(jresp.text)

    def get_command_state(self, count=None):
        #print "/types/Command/instances"
        #payload = {'_':'1425822717883'} # What do this mean?
        #resp = self._im_session.get("{}/{}".format(self._im_api_url, 'types/Command/instances/'), params = payload)
        resp = self._im_session.get("{}/{}".format(self._im_api_url, 'types/Command/instances'))
        #resp = self._im_session.get('https://192.168.100.42/types/Command/instances').json()
        #print "URL: " + resp.url
        #pprint (resp.text)
        return resp.text
        
    def get_nodeinfo_instances(self):
        print "/types/NodeInfo/instances/actions/downloadGetInfo"
        resp = self._im_session.get("{}/{}".format(self._im_api_url, 'types/NodeInfo/instances/actions/downloadGetInfo'))
        #resp = self._im_session.get('https://192.168.100.42/types/NodeInfo/instances/actions/downloadGetInfo')
        pprint (resp.text)

    def get_configuration_instances(self, count=None):
        print "/types/Configuration/instances"
        payload = {'_':''}
        resp = self._im_session.get("{}/{}".format(self._im_api_url, 'types/Configuration/instances/'))
        #resp = self._im_session.get('https://192.168.100.42/types/Configuration/instances')
        pprint (resp.text)

    def get_cluster_topology(self, mdmIP, mdmPassword, liaPassword=None):
        # Topology is returned as a file. Save it into a string. Parse as JSON.
        # When adding nodes to existing ScaleIO cluster using IM all node change are driven by changing topology CSV file.
        
        
        #print "Get Topology - Import into ScaleIO_Configuration_Object"
        
        #print "IM SESSION OBJECT:"
        #pprint (self._im_session)
        
        pay1 = {'mdmIps':[mdmIP],'mdmPassword':mdmPassword} #,'liaPassword':liaPassword}
        #pay1 = {'mdmIp':'192.168.100.42','mdmPassword':'Password1!','liaPassword':'Password1!'}
        r1 = self._im_session.post(
            "{}/{}".format(self._im_api_url,"types/Configuration/instances/actions/refreshAndGet"),
            headers={'Content-type':'application/json','Version':'1.0'},
            verify=self._im_verify_ssl,
            json=pay1,
            stream=True
        )
        if not r1.ok:
            # Something went wrong
            print "Error retrieving get_cluster_topology()"
        
        print "*** get_cluster_topology() ***"
        pprint (json.loads(r1.text))
        return r1.text
    
    def retrieve_scaleio_cluster_configuration(self, mdmIP, mdmPassword, liaPassword=None):
        sysconf_json = self.get_cluster_topology(mdmIP, mdmPassword, liaPassword)
        confObj = ScaleIO_System_Object.from_dict(json.loads(sysconf_json))
        confObj.setMdmPassword(mdmPassword)
        confObj.setLiaPassword(liaPassword)
        self._cluster_config_cached = confObj
        self._cache_contains_uncommitted = False

    def populate_scaleio_cluster_configuration_cache(self, mdmIP, mdmPassword, liaPassword=None):
        sysconf_json = self.get_cluster_topology(mdmIP, mdmPassword, liaPassword)
        confObj = ScaleIO_System_Object.from_dict(json.loads(sysconf_json))
        confObj.setMdmPassword(mdmPassword)
        confObj.setLiaPassword(liaPassword)
        self._cluster_config_cached = confObj
        self._cache_contains_uncommitted = False

    def write_cluster_config_to_disk(self):
        with open("cache.json", "w") as file:
            file.write(self._cluster_config_cached.to_JSON())
            file.close()
    
    def read_cluster_config_from_disk(self, filename = None):
        
        if filename:
            with open(filename, "r") as file:
                #result = file.read()
                confObj = ScaleIO_System_Object.from_dict(json.loads(file.read()))
                file.close()
        else:
            with open("cache.json", "r") as file:
                #result = file.read()
                confObj = ScaleIO_System_Object.from_dict(json.loads(file.read()))
                file.close()
        self._cluster_config_cached = confObj # Read file contents into in-memory cluster configuration cache
        self._cache_contains_uncommitted = False

    def push_cached_cluster_configuration(self, mdmPassword, liaPassword, noUpload = False, noInstall= False, noConfigure = False):
        """
        Method push cached ScaleIO cluster configuration to IM (reconfigurations that have been made to cached configuration are committed using IM)
        Method: POST
        Attach JSON cluster configuration as request payload (data). Add MDM and LIA passwords)
        """
        config_params = {'noUpload': noUpload, 'noInstall': noInstall, 'noConfigure':noConfigure}
        print "Push cached ScaleIO cluster configuration to IM"
        self._cluster_config_cached.setMdmPassword(mdmPassword)
        self._cluster_config_cached.setLiaPassword(liaPassword)
        pprint (self._cluster_config_cached.to_JSON())


        ####### FINISH METOD - CAN ONLY PUSH - USE CACHE
        # SDS configured to use /home/scaleio1
        #default_minimal_cluster_config = '{"installationId":null,"mdmIPs":["192.168.102.12","192.168.102.13"],"mdmPassword":"Scaleio123","liaPassword":"Scaleio123","licenseKey":null,"primaryMdm":{"node":{"ostype":"linux","nodeName":null,"nodeIPs":["192.168.102.12"],"domain":null,"userName":"root","password":"vagrant","liaPassword":null},"nodeInfo":null,"managementIPs":null,"mdmIPs":["192.168.102.12"]},"secondaryMdm":{"node":{"ostype":"linux","nodeName":null,"nodeIPs":["192.168.102.13"],"domain":null,"userName":"root","password":"vagrant","liaPassword":null},"nodeInfo":null,"managementIPs":null,"mdmIPs":["192.168.102.13"]},"tb":{"node":{"ostype":"linux","nodeName":null,"nodeIPs":["192.168.102.11"],"domain":null,"userName":"root","password":"vagrant","liaPassword":null},"nodeInfo":null,"tbIPs":["192.168.102.11"]},"sdsList":[{"node":{"ostype":"linux","nodeName":null,"nodeIPs":["192.168.102.11"],"domain":null,"userName":"root","password":"vagrant","liaPassword":null},"nodeInfo":null,"sdsName":"SDS_[192.168.102.11]","protectionDomain":"default","faultSet":null,"allIPs":["192.168.102.11"],"sdsOnlyIPs":null,"sdcOnlyIPs":null,"devices":[{"devicePath":"/home/vagrant/scaleio1","storagePool":null,"deviceName":null}],"optimized":false,"port":7072},{"node":{"ostype":"linux","nodeName":null,"nodeIPs":["192.168.102.12"],"domain":null,"userName":"root","password":"vagrant","liaPassword":null},"nodeInfo":null,"sdsName":"SDS_[192.168.102.12]","protectionDomain":"default","faultSet":null,"allIPs":["192.168.102.12"],"sdsOnlyIPs":null,"sdcOnlyIPs":null,"devices":[{"devicePath":"/home/vagrant/scaleio1","storagePool":null,"deviceName":null}],"optimized":false,"port":7072},{"node":{"ostype":"linux","nodeName":null,"nodeIPs":["192.168.102.13"],"domain":null,"userName":"root","password":"vagrant","liaPassword":null},"nodeInfo":null,"sdsName":"SDS_[192.168.102.13]","protectionDomain":"default","faultSet":null,"allIPs":["192.168.102.13"],"sdsOnlyIPs":null,"sdcOnlyIPs":null,"devices":[{"devicePath":"/home/vagrant/scaleio1","storagePool":null,"deviceName":null}],"optimized":false,"port":7072}],"sdcList":[{"node":{"ostype":"linux","nodeName":null,"nodeIPs":["192.168.102.11"],"domain":null,"userName":"root","password":"vagrant","liaPassword":null},"nodeInfo":null,"splitterRpaIp":null},{"node":{"ostype":"linux","nodeName":null,"nodeIPs":["192.168.102.12"],"domain":null,"userName":"root","password":"vagrant","liaPassword":null},"nodeInfo":null,"splitterRpaIp":null},{"node":{"ostype":"linux","nodeName":null,"nodeIPs":["192.168.102.13"],"domain":null,"userName":"root","password":"vagrant","liaPassword":null},"nodeInfo":null,"splitterRpaIp":null}],"callHomeConfiguration":null,"remoteSyslogConfiguration":null}'
        
        # Generated with scelio_object.py - Progammatically generated JSON using a set of classes that represent different ScaleIO components
        default_minimal_cluster_config = '{"licenseKey": null, "mdmPassword": "Scaleio123", "mdmIPs": ["192.168.102.12", "192.168.102.13"], "sdsList": [{"node": {"userName": "root", "domain": null, "nodeName": null, "nodeIPs": ["192.168.102.11"], "liaPassword": null, "ostype": "linux", "password": "vagrant"}, "protectionDomain": "default", "nodeInfo": null, "sdsName": "SDS_192.168.102.11", "sdcOnlyIPs": [], "optimized": false, "devices": [{"devicePath": "/home/vagrant/scaleio1", "storagePool": null, "deviceName": null}], "faultSet": null, "port": "7072", "sdsOnlyIPs": [], "allIPs": ["192.168.102.11"]}, {"node": {"userName": "root", "domain": null, "nodeName": null, "nodeIPs": ["192.168.102.12"], "liaPassword": null, "ostype": "linux", "password": "vagrant"}, "protectionDomain": "default", "nodeInfo": null, "sdsName": "SDS_192.168.102.12", "sdcOnlyIPs": [], "optimized": false, "devices": [{"devicePath": "/home/vagrant/scaleio1", "storagePool": null, "deviceName": null}], "faultSet": null, "port": "7072", "sdsOnlyIPs": [], "allIPs": ["192.168.102.12"]}, {"node": {"userName": "root", "domain": null, "nodeName": null, "nodeIPs": ["192.168.102.13"], "liaPassword": null, "ostype": "linux", "password": "vagrant"}, "protectionDomain": "default", "nodeInfo": null, "sdsName": "SDS_192.168.102.13", "sdcOnlyIPs": [], "optimized": false, "devices": [{"devicePath": "/home/vagrant/scaleio1", "storagePool": null, "deviceName": null}], "faultSet": null, "port": "7072", "sdsOnlyIPs": [], "allIPs": ["192.168.102.13"]}], "liaPassword": "Scaleio123", "primaryMdm": {"node": {"userName": "root", "domain": null, "nodeName": null, "nodeIPs": ["192.168.102.12"], "liaPassword": null, "ostype": "linux", "password": "vagrant"}, "nodeInfo": null, "managementIPs": [], "mdmIPs": ["192.168.102.12"]}, "callHomeConfiguration": null, "installationId": null, "secondaryMdm": {"node": {"userName": "root", "domain": null, "nodeName": null, "nodeIPs": ["192.168.102.13"], "liaPassword": null, "ostype": "linux", "password": "vagrant"}, "nodeInfo": null, "managementIPs": [], "mdmIPs": ["192.168.102.13"]}, "sdcList": [{"node": {"userName": "root", "domain": null, "nodeName": null, "nodeIPs": ["192.168.102.11"], "liaPassword": null, "ostype": "linux", "password": "vagrant"}, "nodeInfo": null, "splitterRpaIp": null}, {"node": {"userName": "root", "domain": null, "nodeName": null, "nodeIPs": ["192.168.102.12"], "liaPassword": null, "ostype": "linux", "password": "vagrant"}, "nodeInfo": null, "splitterRpaIp": null}, {"node": {"userName": "root", "domain": null, "nodeName": null, "nodeIPs": ["192.168.102.13"], "liaPassword": null, "ostype": "linux", "password": "vagrant"}, "nodeInfo": null, "splitterRpaIp": null}], "tb": {"node": {"userName": "root", "domain": null, "nodeName": null, "nodeIPs": ["192.168.102.11"], "liaPassword": null, "ostype": "linux", "password": "vagrant"}, "nodeInfo": null, "tbIPs": ["192.168.102.11"]}, "remoteSyslogConfiguration": null}'        
        #
        #default_minimal_cluster_config = '{"installationId":null,"mdmIPs":["192.168.100.51","192.168.100.52"],"mdmPassword":"Password1!","liaPassword":"Password1!","licenseKey":null,"primaryMdm":{"node":{"ostype":"linux","nodeName":null,"nodeIPs":["192.168.100.51"],"domain":null,"userName":"root","password":"password","liaPassword":null},"nodeInfo":null,"managementIPs":null,"mdmIPs":["192.168.100.51"]},"secondaryMdm":{"node":{"ostype":"linux","nodeName":null,"nodeIPs":["192.168.100.52"],"domain":null,"userName":"root","password":"password","liaPassword":null},"nodeInfo":null,"managementIPs":null,"mdmIPs":["192.168.100.52"]},"tb":{"node":{"ostype":"linux","nodeName":null,"nodeIPs":["192.168.100.53"],"domain":null,"userName":"root","password":"password","liaPassword":null},"nodeInfo":null,"tbIPs":["192.168.100.53"]},"sdsList":[{"node":{"ostype":"linux","nodeName":null,"nodeIPs":["192.168.100.51"],"domain":null,"userName":"root","password":"password","liaPassword":null},"nodeInfo":null,"sdsName":"SDS_[192.168.100.51]","protectionDomain":"default","faultSet":null,"allIPs":["192.168.100.51"],"sdsOnlyIPs":null,"sdcOnlyIPs":null,"devices":[{"devicePath":"/dev/sdb","storagePool":null,"deviceName":null}],"optimized":false,"port":7072},{"node":{"ostype":"linux","nodeName":null,"nodeIPs":["192.168.100.52"],"domain":null,"userName":"root","password":"password","liaPassword":null},"nodeInfo":null,"sdsName":"SDS_[192.168.100.52]","protectionDomain":"default","faultSet":null,"allIPs":["192.168.100.52"],"sdsOnlyIPs":null,"sdcOnlyIPs":null,"devices":[{"devicePath":"/dev/sdb","storagePool":null,"deviceName":null}],"optimized":false,"port":7072},{"node":{"ostype":"linux","nodeName":null,"nodeIPs":["192.168.100.53"],"domain":null,"userName":"root","password":"password","liaPassword":null},"nodeInfo":null,"sdsName":"SDS_[192.168.100.53]","protectionDomain":"default","faultSet":null,"allIPs":["192.168.100.53"],"sdsOnlyIPs":null,"sdcOnlyIPs":null,"devices":[{"devicePath":"/dev/sdb","storagePool":null,"deviceName":null}],"optimized":false,"port":7072}],"sdcList":[{"node":{"ostype":"linux","nodeName":null,"nodeIPs":["192.168.100.51"],"domain":null,"userName":"root","password":"password","liaPassword":null},"nodeInfo":null,"splitterRpaIp":null},{"node":{"ostype":"linux","nodeName":null,"nodeIPs":["192.168.100.52"],"domain":null,"userName":"root","password":"password","liaPassword":null},"nodeInfo":null,"splitterRpaIp":null},{"node":{"ostype":"linux","nodeName":null,"nodeIPs":["192.168.100.53"],"domain":null,"userName":"root","password":"password","liaPassword":null},"nodeInfo":null,"splitterRpaIp":null}],"callHomeConfiguration":null,"remoteSyslogConfiguration":null}'
        
        print "JSON DUMP OF INSTALL CONFIG:"
        pprint (json.loads(default_minimal_cluster_config))
        
        r1 = self._im_session.post(
            "{}/{}".format(self._im_api_url,"types/Installation/instances/"),
            headers={'Content-type':'application/json','Version':'1.0'},
            params = config_params, 
            verify=self._im_verify_ssl,
            #json=json.loads(self._cluster_config_cached.to_JSON()),
            json = json.loads(default_minimal_cluster_config),
            stream=True
        )
        if not r1.ok:
            # Something went wrong
            print "Error push_cached_cluster_configuration()"
        
        print "Response after push_cached_cluster_configuration()"
        
        # RESPONSE NEED TO BE WRAPPED IN tey/catch. Can?t assume JSON is returned.
        print r1.text
        #pprint (json.loads(r1.text))
        return r1.text
    
    def add_sds_to_cluster(self, sdsobject):
        self._cluster_config_cached.sdsList.append(sdsobject)
        self._cache_contains_uncommitted = True
                
    def create_minimal_scaleio_cluster(self, mdmPassword, liaPassword):
        """
        Using IM this method create a 3-node ScaleIO cluster with 2xMDM, 1xTB, 3x SDS (using /dev/sdb), 3x SDC
        """
        """
        self.read_cluster_config_from_disk("minimal-cluster.json")
        #self._cluster_config_cached.setMdmPassword(setMdmPassword)
        #self._cluster_config_cached.setLiaPassword(setLiaPassword)
        self.push_cached_cluster_configuration(setMdmPassword, setLiaPassword)
        """
        
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
        #node1 = ScaleIO_Node_Object(None, None, ['192.168.102.11'], None, 'linux', nodePassword, nodeUsername)
        #node2 = ScaleIO_Node_Object(None, None, ['192.168.102.12'], None, 'linux', nodePassword, nodeUsername)
        #node3 = ScaleIO_Node_Object(None, None, ['192.168.102.13'], None, 'linux', nodePassword, nodeUsername)
        node1 = ScaleIO_Node_Object(None, None, ['192.168.100.101'], None, 'linux', nodePassword, nodeUsername)
        node2 = ScaleIO_Node_Object(None, None, ['192.168.100.102'], None, 'linux', nodePassword, nodeUsername)
        node3 = ScaleIO_Node_Object(None, None, ['192.168.100.103'], None, 'linux', nodePassword, nodeUsername)
        print "Node Object:"
        pprint (node1.to_JSON())
        pprint (node2.to_JSON())
        pprint (node2.to_JSON())
        print ""
            
        ##########################################
        # Construct basic info for System_Object #
        ##########################################
        mdmIPs = ['192.168.100.101','192.168.100.102']
        sdcList = []
        sdsList = []
        #mdmPassword = 'Scaleio123'
        #liaPassword = 'Scaleio123'
        licenseKey = None
        installationId = None
     
        ########################################
        # Create MDMs and TB for System_Object #
        ########################################
        primaryMdm = Mdm_Object(json.loads(node2.to_JSON()), None, None, node2.nodeIPs) # WHY ISNT ManagementIPs pupulated???? Its not in a working config either. mdmIPs need to be populated though
        secondaryMdm = Mdm_Object(json.loads(node3.to_JSON()), None, None, node3.nodeIPs)
        tb = Tb_Object(json.loads(node1.to_JSON()), None, node1.nodeIPs)
        callHomeConfiguration = None # {'callHomeConfiguration':'None'}
        remoteSyslogConfiguration = None # {'remoteSysogConfiguration':'None'}
        
        ################################################################
        #Create SDS objects - To be added to SDS list in System_Object #
        ################################################################
        sds1 = Sds_Object(json.loads(node1.to_JSON()), None, 'SDS_' + str(node1.nodeIPs[0]), 'default', None, node1.nodeIPs, None, None, None, False, '7072')
        sds1.addDevice("/dev/sdb", None, None)
        sds2 = Sds_Object(json.loads(node2.to_JSON()), None, 'SDS_' + str(node2.nodeIPs[0]), 'default', None, node2.nodeIPs, None, None, None, False, '7072')
        sds2.addDevice("/dev/sdb", None, None)
        sds3 = Sds_Object(json.loads(node3.to_JSON()), None, 'SDS_' + str(node3.nodeIPs[0]), 'default', None, node3.nodeIPs, None, None, None, False, '7072')
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
        sdc1 = Sdc_Object(json.loads(node1.to_JSON()), None, None)
        sdc2 = Sdc_Object(json.loads(node2.to_JSON()), None, None)
        sdc3 = Sdc_Object(json.loads(node3.to_JSON()), None, None)
        
        sdcList.append(json.loads(sdc1.to_JSON()))
        sdcList.append(json.loads(sdc2.to_JSON()))
        sdcList.append(json.loads(sdc3.to_JSON()))
        
        ######################################################
        # Construct a complete ScaleIO cluster configuration #
        ######################################################
        sioobj = ScaleIO_System_Object(installationId,
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
        self._cluster_config_cached = sioobj.to_JSON() # PUSH CONFIGURATION INTO CONFIGURATION CACHE
        self._cache_contains_uncommitted= False # New config pushed into cache - Nothing oncommitted
        self.push_cluster_configuration(self._cluster_config_cached) # sioobj.to_JSON())
        
    def push_cluster_configuration(self, scaleioobj, noUpload = False, noInstall= False, noConfigure = False):
        """
        Method push cached ScaleIO cluster configuration to IM (reconfigurations that have been made to cached configuration are committed using IM)
        Method: POST
        Attach JSON cluster configuration as request payload (data). Add MDM and LIA passwords)
        """

        #print "JSON DUMP OF CLUSTER CONFIG:"
        #pprint (json.loads(scaleioobj))
        config_params = {'noUpload': noUpload, 'noInstall': noInstall, 'noConfigure':noConfigure}

        r1 = self._im_session.post(
            "{}/{}".format(self._im_api_url,"types/Installation/instances/"),
            headers={'Content-type':'application/json','Version':'1.0'},
            params = config_params, 
            verify=self._im_verify_ssl,
            #json=json.loads(self._cluster_config_cached.to_JSON()),
            json = json.loads(scaleioobj),
            stream=True
        )
        if not r1.ok:
            # Something went wrong
            print "Error push_cluster_configuration()"
        
        #print "Response after push_cluster_configuration()"
        
        # RESPONSE NEED TO BE WRAPPED IN tey/catch. Cannot assume JSON is returned.
        #print r1.text
        #pprint (json.loads(r1.text))
        return r1.text
   
    # Add API client methods here that interact with IM API
    @property
    def system(self): # Change to something that is usable. A Class for Generate CSV for example.
        pass
    
    def uploadPackages(self, directory):        
        """
        Not working. Am not able ot figure out how to upload. IT return status 200OK with this code but do not store the files.
        In tomcat.log (IM) there?s a complaint about character encoding whn uploading file. Not sure how to rectiy it in requests post call though
        """
        files_to_upload_dict = {}
        files_to_upload_list = [ f for f in listdir(directory) if isfile(join(directory,f)) ]

        print "Files to upload:"
        for index in range(len(files_to_upload_list)):
            print "  " + files_to_upload_list[index]
            self.uploadFileToIM (directory, files_to_upload_list[index], files_to_upload_list[index])
            #file_tuple = {'files':{str(files_to_upload_list[index]), open(directory + files_to_upload_list[index], 'rb'), 'application/x-rpm'}}      
            #file_tuple = {str(files_to_upload_list[index]), {open(directory + files_to_upload_list[index], 'rb'), 'application/x-rpm'}}
            #file_tuple = {'files': (str(files_to_upload_list[index]), open(directory + files_to_upload_list[index], 'rb'), 'application/x-rpm')}
            #file_tuple = (str(files_to_upload_list[index]), open(directory + files_to_upload_list[index], 'rb'))
            #file_tuple = {str(files_to_upload_list[index]), open(directory + files_to_upload_list[index], 'rb'), 'application/x-rpm'}
            #files_data_to_upload_list.append(file_tuple)
        print "No more files"
        #print "Files to upload Dictionary:"

        
    def uploadFileToIM (self, directory, filename, title):
        """
        Parameters as they look in the form for uploading packages to IM
        """
        parameters = {'data-filename-placement':'inside',
                      'title':str(filename),
                      'filename':str(filename),
                      'type':'file',
                      'name':'files',
                      'id':'fileToUpload',
                      'multiple':''
                      }
        file_dict = {'files':(str(filename), open(directory + filename, 'rb'), 'application/x-rpm')}
        m = MultipartEncoder(fields=file_dict)
        
        temp_username = self._username
        temp_password = self._password
        temp_im_api_url = self._im_api_url
        temp_im_session = requests.Session()
        temp_im_session.mount('https://', TLS1Adapter())
        temp_im_verify_ssl = self._im_verify_ssl

        resp = temp_im_session.post(
            "{}/{}".format(temp_im_api_url,"types/InstallationPackage/instances/uploadPackage"),
            auth=HTTPBasicAuth(temp_username, temp_password),
            #headers = m.content_type,
            files = file_dict,
            verify = False,
            data = parameters
            )
        #print "resp.text = " + resp.text
                
    def deleteFileFromIM(self, filename):
        pass
        """
        Request URL:https://192.168.100.42/instances/InstallationPackage::EMC-ScaleIO-tb-1.31-260.3.el6.x86_64.rpm/
        Request Method:DELETE
        """
        
        ##### NEED TO BE IMPLEMENTED
        # Get list of installed files.
        # Reverse engineer how the process works using the IM Webui
    
    def uploadCsvConfiguration(self, conf_filename):
        """
        NOT NEEDED. JSON can be POSTed to IM instead of sending a CSV that is locally parsed and converted to JSON.
        
        Remote Address:192.168.100.51:443
        Request URL:https://192.168.100.51/types/Configuration/instances/actions/parseFromCSV
        Request Method:POST
        Status Code:200 OK
        Request Headersview source
        Accept:*/*
        Accept-Encoding:gzip, deflate
        Accept-Language:en-US,en;q=0.8,sv;q=0.6
        Connection:keep-alive
        Content-Length:433
        Content-Type:multipart/form-data; boundary=----WebKitFormBoundaryY1f2eTo1mOvh744k
        Cookie:JSESSIONID=A0823886072B2CEBA327A9185AC2BFE0
        Host:192.168.100.51
        Origin:https://192.168.100.51
        Referer:https://192.168.100.51/install.jsp
        User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36
        X-Requested-With:XMLHttpRequest
        Request Payload
        ------WebKitFormBoundaryY1f2eTo1mOvh744k
        Content-Disposition: form-data; name="file"; filename="ScaleIO_Minimal_Config_51.csv"
        Content-Type: text/csv

        """
        parameters = {'selectInstallOrExtend':'install', #'install' or 'extend'
                      'name':'file',
                      'id':'fileToUpload',
                      'filename':'config.csv'
                      }
        file_dict = {'file':('config.csv', open(conf_filename, 'rb'), 'text/csv')}
        """
        files = {'file': ('report.csv', 'some,data,to,send\nanother,row,to,send\n')}
        """
        
        temp_username = self._username
        temp_password = self._password
        temp_im_api_url = self._im_api_url
        temp_im_session = requests.Session()
        #self._im_session.headers.update({'Accept': 'application/json', 'Version': '1.0'}) # Accept only json
        temp_im_session.mount('https://', TLS1Adapter())
        temp_im_verify_ssl = self._im_verify_ssl


        resp = temp_im_session.post(
        #resp = self._do_post(
            "{}/{}".format(temp_im_api_url,"types/Configuration/instances/actions/parseFromCSV"),
            auth=HTTPBasicAuth('admin', 'Password1!'),
            #headers = m.content_type,
            files = file_dict,
            verify = False,
            data = parameters
            )
        pprint (resp)
     
    def getInstallerUrl(self):
        pass


##===============================================
## IM Integration Implmentation  

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s: %(levelname)s %(module)s:%(funcName)s | %(message)s', level=logging.WARNING)

