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
    def __init__(self, api_url, username, password, verify_ssl=False, LiaPassword=None, debugLevel=None):
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
        logging.basicConfig(format='%(asctime)s: %(levelname)s %(module)s:%(funcName)s | %(message)s',
            level=self._get_log_level(debugLevel))
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Logger initialized!")
        self.SIO_Configuration_Object = None # Holds a DICT representation of the ScaleIO System Configuration
        
    @staticmethod
    def _get_log_level(level):
        """
        small static method to get logging level
        :param str level: string of the level e.g. "INFO"
        :returns logging.<LEVEL>: appropriate debug level
        """
        # default to DEBUG
        if level is None or level == "DEBUG":
            return logging.DEBUG

        level = level.upper()
        # Make debugging configurable
        if level == "INFO":
            return logging.INFO
        elif level == "WARNING":
            return logging.WARNING
        elif level == "CRITICAL":
            return logging.CRITICAL
        elif level == "ERROR":
            return logging.ERROR
        elif level == "FATAL":
            return logging.FATAL
        else:
            raise Exception("UnknownLogLevelException: enter a valid log level")

    def _get_cached_config_json(self):
        return self._cluster_config_cached
    
    def _login(self):
        """
        LOGIN CAN ONLY BE DONE BY POSTING TO A HTTP FORM.
        A COOKIE IS THEN USED FOR INTERACTING WITH THE API
        """
        self.logger.debug("Logging into " + "{}/{}".format(self._im_api_url, "j_spring_security_check"))
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
        #self.logger.debug("Login POST response: " + "{}".format(r.text))
        self._im_logged_in = True
        
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
        self.logger.debug("_do_get() " + "{}/{}".format(self._api_url,uri))
        
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
            self.logger.debug("do_put(): " + "{}".format(uri))

            #self._session.headers.update({'Content-Type':'application/json'})
            response = self._session.put(url, headers=scaleioapi_put_headers, verify_ssl=self._im_verify_ssl, data=json.dumps(payload))
            self.logger.debug("_do_put() - Response: " + "{}".format(response.text))
            if response.status_code == requests.codes.ok:
                return response
            else:
                self.logger.error("_do_put() - HTTP response error: " + "{}".format(response.status_code))
                raise RuntimeError("_do_put() - HTTP response error" + response.status_code)
        except:
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
        self.logger.debug("_do_post()")

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
            self.logger.debug("_do_post() - Response: " + "{}".format(response.text))
            if response.status_code == requests.codes.ok:
                return response
            else:
                self.logger.error("_do_post() - Response Code: " + "{}".format(response.status_code))
                raise RuntimeError("_do_post() - HTTP response error" + response.status_code)
        except:
            raise RuntimeError("_do_post() - Communication error with ScaleIO gateway")
        return response
 
    def get_installation_instances(self):
        self.logger.debug("/types/Installation/instances")
        #print "/types/Installation/instances/"
        resp = self._im_session.get("{}/{}".format(self._im_api_url, 'types/Installation/instances'))
        #print resp.text

    def get_state(self, count=None):
        self.logger.debug("/types/State/instances")
        payload = {'_':'1425822717883'}
        referer = 'https://192.168.100.12/install.jsp'
        #resp = self._im_session.get("{}/{}".format(self._im_api_url, 'types/State/instances/'), params = payload)
        resp = self._im_session.get("{}/{}".format(self._im_api_url, 'types/State/instances/'))
        return resp.text
    
    def set_state(self, state):
        # state can be: query, upload, install, configure
        self.logger.debug("set_state(" + "{})".format(state) )
        if state == 'query':
            resp = self._im_session.put("{}/{}".format(self._im_api_url,"types/State/instances/"),data =json.dumps({"state":"query"}), headers={'Content-Type':'application/json'})
            #print "PUT Request URL: " + resp.url
            #print "QUERY Response:"
            #print resp.text
            return True
        if state == 'upload':
            resp = self._im_session.put("{}/{}".format(self._im_api_url,"types/State/instances/"),data =json.dumps({"state":"upload"}), headers={'Content-Type':'application/json'})
            #print "PUT Request URL: " + resp.url
            #print "UPLOAD Response:"
            #print resp.text
            return True
        if state == 'install':
            resp = self._im_session.put("{}/{}".format(self._im_api_url,"types/State/instances/"),data =json.dumps({"state":"install"}), headers={'Content-Type':'application/json'})
            return True
            #print "PUT Request URL: " + resp.url
            #print "INSTALL Response:"
            #print resp.text
        if state == 'configure':
            resp = self._im_session.put("{}/{}".format(self._im_api_url,"types/State/instances/"),data =json.dumps({"state":"configure"}), headers={'Content-Type':'application/json'})
            return True
            #print "PUT Request URL: " + resp.url
            #print "CONFIGURE Response:"
            #print resp.text
        return False
    
    def set_abort_pending(self, newstate):
        """
        Method to set Abort state if something goes wrong during provisioning
        Method also used to finish provisioning process when all is completed
        Method: POST
        """
        self.logger.debug("set_abort_pending(" + "{})".format(newstate))
        r1 = self._im_session.post(
            "{}/{}".format(self._im_api_url,"types/Command/instances/actions/abortPending"),
            headers={'Content-type':'application/json','Version':'1.0'}, 
            verify=self._im_verify_ssl,
            data = newstate,
            stream=True
        )
        if not r1.ok:
            # Something went wrong
            self.logger.error("Error set_abort_pending(" +"{})".format(newstate))

        return r1.text

    def set_archive_all(self):
        """
        Last method to be called when provisioning is complete
        Method: POST
        """
        self.logger.debug("set_archive_all()")

        r1 = self._im_session.post(
            "{}/{}".format(self._im_api_url,"types/Command/instances/actions/archiveAll"),
            headers={'Content-type':'application/json','Version':'1.0'}, 
            verify=self._im_verify_ssl,
            data = '',
            stream=True
        )
        if not r1.ok:
            # Something went wrong
            self.logger.error("Error code: " + "{}".format(r1.status_code))
        return r1.text

    def get_version(self):
        self.logger.debug("get_version()")
        payload = {'_':'1425822717883'} # Investigate what this number mean when some IM API calls are done. Its used by IM Webui. Seem to be Unixtime format.
        referer = 'https://192.168.100.12/status.jsp'
        resp = self._im_session.get("{}/{}".format(self._im_api_url, 'version/'), params = payload)  
        
    def get_installation_packages_latest(self):
        """
        In 1.31-256 getting latest or all packages seem not to work. Always same result not matter what value 'onlLatest' have. Same situation in IM WEBUI too.
        """
        self.logger.debug("get_installation_packages_latest()")
        parameter = {'onlyLatest':'False'}
        resp = self._im_session.get("{}/{}".format(self._im_api_url, 'types/InstallationPackageWithLatest/instances'), params=parameter)
        #resp = self._im_session.get('https://192.168.100.52/types/InstallationPackageWithLatest/instances', params=parameter)
        jresp = json.loads(resp.text)

        #pprint(jresp)

    def get_installation_packages(self):
        """
        In 1.31-256 getting latest or all packages seem not to work. Always same result not matter what value 'onlLatest' have. Same situation in IM WEBUI too.
        """
        self.logger.debug("get_installation_packages()")
        parameter = {'onlyLatest':'False'}
        resp = self._im_session.get("{}/{}".format(self._im_api_url, 'types/InstallationPackageWithLatest/instances'), params=parameter)
        #resp = self._im_session.get('https://192.168.100.52/types/InstallationPackageWithLatest/instances', params=parameter)
        jresp = json.loads(resp.text)
        #pprint(jresp.text)
        return jresp
    
    def get_command_state(self, count=None):
        self.logger.debug("get_command_state(" + "{})".format(count))
        resp = self._im_session.get("{}/{}".format(self._im_api_url, 'types/Command/instances'))
        return resp.text
        
    def get_nodeinfo_instances(self):
        self.logger.debug("/types/NodeInfo/instances/actions/downloadGetInfo")
        resp = self._im_session.get("{}/{}".format(self._im_api_url, 'types/NodeInfo/instances/actions/downloadGetInfo'))

    def get_configuration_instances(self, count=None):
        self.logger.debug("/types/Configuration/instances")
        payload = {'_':''}
        resp = self._im_session.get("{}/{}".format(self._im_api_url, 'types/Configuration/instances/'))

    def get_cluster_topology(self, mdmIP, mdmPassword, liaPassword=None):
        # Topology is returned as a file. Save it into a string. Parse as JSON.
        # When adding nodes to existing ScaleIO cluster using IM all node change are driven by changing topology CSV file.

        self.logger.debug("get_cluster_topology(" + "{},{},{}".format(mdmIP, mdmPassword, liaPassword))

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
            self.logger.error("Could not fetch congiuration from remote IM")
        self.logger.debug("POST response: " + "{}".format(r1.text))
        return r1.text
    
    def retrieve_scaleio_cluster_configuration(self, mdmIP, mdmPassword, liaPassword=None):
        self.logger.debug("retrieve_scaleio_cluster_configuration(" + "{},{},{}".format(mdmIP, mdmPassword, liaPassword))
        sysconf_json = self.get_cluster_topology(mdmIP, mdmPassword, liaPassword)
        confObj = ScaleIO_System_Object.from_dict(json.loads(sysconf_json))
        confObj.setMdmPassword(mdmPassword)
        confObj.setLiaPassword(liaPassword)
        self._cluster_config_cached = confObj
        self._cache_contains_uncommitted = False

    def populate_scaleio_cluster_configuration_cache(self, mdmIP, mdmPassword, liaPassword=None):
        self.logger.debug("populate_scaleio_cluster_configuration_cache(" + "{},{},{}".format(mdmIP, mdmPassword, liaPassword))
        sysconf_json = self.get_cluster_topology(mdmIP, mdmPassword, liaPassword)
        confObj = ScaleIO_System_Object.from_dict(json.loads(sysconf_json))
        confObj.setMdmPassword(mdmPassword)
        confObj.setLiaPassword(liaPassword)
        self._cluster_config_cached = confObj
        self._cache_contains_uncommitted = False

    def write_cluster_config_to_disk(self):
        self.logger.debug("write_cluster_config_to_disk()")
        with open("cache.json", "w") as file:
            file.write(self._cluster_config_cached.to_JSON())
            file.close()
    
    def read_cluster_config_from_disk(self, filename = None):
        self.logger.debug("read_cluster_config_from_disk(" + "{})".format(filename))
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
    
    def add_sds_to_cluster(self, sdsobject):
        self.logger.debug("add_sds_to_cluster(" + "{})".format(sdsobject))
        self._cluster_config_cached.sdsList.append(sdsobject)
        self._cache_contains_uncommitted = True
                
    def push_cluster_configuration(self, scaleioobj, noUpload = False, noInstall= False, noConfigure = False):
        """
        Method push cached ScaleIO cluster configuration to IM (reconfigurations that have been made to cached configuration are committed using IM)
        Method: POST
        Attach JSON cluster configuration as request payload (data). Add MDM and LIA passwords)
        """
        self.logger.debug("push_cluster_configuration(" + "{},{},{},{})".format(scaleioobj, noUpload, noInstall, noConfigure))
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
            self.logger.error("Error push_cluster_configuration() - " + "Errorcode: {}".format(r1.status_code))

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
        self.logger.debug("uploadPackages(" + "{})".format(directory))
        #print "Files to upload:"
        for index in range(len(files_to_upload_list)):
            self.logger.info(files_to_upload_list[index])
            self.uploadFileToIM (directory, files_to_upload_list[index], files_to_upload_list[index])
        
    def uploadFileToIM (self, directory, filename, title):
        """
        Parameters as they look in the form for uploading packages to IM
        """
        self.logger.debug("uploadFileToIM(" + "{},{},{})".format(directory, filename, title))
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
        self.logger.info("Uploaded: " + "{}".format(filename))
        self.logger.debug("HTTP Response: " + "{}".format(resp.status_code))
        #print "resp.text = " + resp.text
                
    def deleteFileFromIM(self, filename):
        pass
        """
        Request URL:https://192.168.100.42/instances/InstallationPackage::EMC-ScaleIO-tb-1.31-260.3.el6.x86_64.rpm/
        Request Method:DELETE
        """
        self.logger.debug("deleteFileFromIM(" + "{}".format(filename))
        ##### NEED TO BE IMPLEMENTED
        # Get list of installed files.
        # Reverse engineer how the process works using the IM Webui
     
    def getInstallerUrl(self):
        pass


##===============================================
## IM Integration Implementation  

if __name__ == "__main__":
    pass
    #logging.basicConfig(format='%(asctime)s: %(levelname)s %(module)s:%(funcName)s | %(message)s', level=logging.WARNING)

