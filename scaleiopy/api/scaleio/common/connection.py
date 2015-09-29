# Standard lib imports
#import logging
from requests.auth import HTTPBasicAuth
from requests_toolbelt import SSLAdapter
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
import requests
import ssl
import logging

# Third party imports
# None

# Project level imports
# None

#log = logging.getLogger(__name__)

# How to remove this one. Let Requests inherit from this class???
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
                                       

class Connection(object):

    def __init__(self, connection, api_url, username, password, verify_ssl=False, debugLevel=None):
        """
        Initialize a new instance
        """
        self.conn = connection        

        self._username = username
        self._password = password
        self._api_url = api_url
        self._session = requests.Session()
        self._session.headers.update({'Accept': 'application/json', 'Version': '1.0'}) # Accept only json
        self._session.mount('https://', TLS1Adapter())
        self._verify_ssl = verify_ssl
        self._logged_in = False
        self._api_version = None
        requests.packages.urllib3.disable_warnings() # Disable unverified connection warning.
#        logging.basicConfig(format='%(asctime)s: %(levelname)s %(module)s:%(funcName)s | %(message)s',level=self._get_log_level(debugLevel))
#        self.logger = logging.getLogger(__name__)
#        self.logger.debug("Logger initialized!")
        self._check_login() # Login. Otherwise login is called upon first API operation

    
    def logout(self):
        pass
    
    def login(self):
        self.conn.logger.debug("Logging into " + "{}/{}".format(self._api_url, "login"))
        self.conn.logger.debug("With credentials " + "{}/{}".format(self._username, self._password))
        login_response = self._session.get(
            "{}/{}".format(self._api_url,"login"),
            verify=self._verify_ssl,
            auth=HTTPBasicAuth(self._username, self._password)
        ).json()
        if type(login_response) is dict:
            # If we got here, something went wrong during login
            for key, value in login_response.iteritems():
                if key == 'errorCode':
                    self.conn.logger.error('Login error code: %s', login_response['message'])
                    raise RuntimeError(login_response['message'])
        else:
            self._auth_token = login_response
            self.conn.logger.debug('Authentication token recieved: %s', self._auth_token)
            self._session.auth = HTTPBasicAuth('',self._auth_token)
            self._logged_in = True
            # Set _api_version_ to current version of connected API
            self._api_version = login_response = self._session.get(
                "{}/{}".format(self._api_url,"version"),
                verify=self._verify_ssl,
                auth=HTTPBasicAuth(self._username, self._password)
                ).json() # Do ScaleIO API really obey versioning????

    def _check_login(self):
        if not self._logged_in:
            self.login()
        else:
            pass
        return None

    def get_api_version(self):
        self._check_login()
        # API version scheme:
        # 1.0 = < v1.32
        # 1.1 =   v1.32
        # x.x =   v2.0
        return self._api_version


    # Basic data handling transfer methods
    
    # FIX _do_get method, easier to have one place to do error handling than in all other methods that call _do_get()
    def _do_get(self, url, **kwargs):
        """
        Convenient method for GET requests
        Returns http request status value from a POST request
        """
        #TODO:
        # Add error handling. Check for HTTP status here would be much more conveinent than in each calling method
        scaleioapi_post_headers = {'Content-type':'application/json','Version':'1.0'}
        try:
            #response = self._session.get("{}/{}".format(self._api_url, uri)).json()
            response = self._session.get(url)
            if response.status_code == requests.codes.ok:
                self.conn.logger.debug('_do_get() - HTTP response OK, data: %s', response.text)                
                return response
            else:
                self.conn.logger.error('_do_get() - HTTP response error: %s', response.status_code)
                self.conn.logger.error('_do_get() - HTTP response error, data: %s', response.text)                
                raise RuntimeError("_do_get() - HTTP response error" + response.status_code)
        except Exception as e:
            self.conn.logger.error("_do_get() - Unhandled Error Occurred: %s" % str(e)) 
            raise RuntimeError("_do_get() - Communication error with ScaleIO gateway")
        return response

    def _do_post(self, url, **kwargs):
        """
        Convenient method for POST requests
        Returns http request status value from a POST request
        """
        #TODO:
        # Add error handling. Check for HTTP status here would be much more conveinent than in each calling method
        scaleioapi_post_headers = {'Content-type':'application/json','Version':'1.0'}
        try:
            response = self._session.post(url, headers=scaleioapi_post_headers, **kwargs)
            self.conn.logger.debug('_do_post() - HTTP response: %s', response.text)
            if response.status_code == requests.codes.ok:
                self.conn.logger.debug('_do_post() - HTTP response OK, data: %s', response.text)                
                return response
            else:
                self.conn.logger.error('_do_post() - HTTP response error: %s', response.status_code)
                self.conn.logger.error('_do_post() - HTTP response error, data: %s', response.text)                
                raise RuntimeError("_do_post() - HTTP response error" + response.status_code)
        except Exception as e:
            self.conn.logger.error("_do_post() - Unhandled Error Occurred: %s" % str(e)) 
            raise RuntimeError("_do_post() - Communication error with ScaleIO gateway")
        return response


    def _do_put(self):
        pass
    
    def _do_delete(self):
        pass
    
