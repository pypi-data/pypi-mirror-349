from typing import Any, Callable, Dict, Optional, Union
from wsgiref.validate import validator

import requests

from airflow.exceptions import AirflowException
from airflow.providers.qlik_sense.hooks.qlik_sense_hook import QlikSenseHook

from requests_ntlm2 import HttpNtlmAuth

class QlikSenseHookNTLM(QlikSenseHook):
    """
    Qlik Sense Hook to interract with a On-Promise Site Qlik Sense Server
    
    """

    conn_name_attr = 'qlik_sense_conn_id'
    default_conn_name = 'qlik_sense_default'
    conn_type = 'qlik_sense_client_managed_ntlm'
    hook_name = '[NTLM] Qlik Sense Client Managed'
    auth_type = 'NTLM'
    __cookie_session =None

    def __init__(self,conn_id: str = default_conn_name) -> None:
        super().__init__()
        self.conn_id = conn_id
        self.base_url: str = ""
    
    def __get_cookies_session(self):
        """
        
        In NTLM Authentification for Qlik, you have to use a GET request to obain cookies session. When you've got cookies session, you can use it to use POST, PUT, DELETE endpoint in QRS API. 
        This function is calling qrs/about in method GET to obtain the cookies session.    
    
        """
        
        if self.__cookie_session is None:

            session = self.get_conn_init()
            endpoint = 'qrs/about'
            
            if self.base_url and not self.base_url.endswith('/') and endpoint and not endpoint.startswith('/'):
                url = self.base_url + '/' + endpoint
            else:
                url = (self.base_url or '') + (endpoint or '')

            req = requests.Request('GET', url)

            self.log.info("Sending GET about to url: %s to retrieve Qlik Session Cookie", url)

            prepped = session.prepare_request(req)
            try:
                response = session.send(prepped, verify=False, allow_redirects=True)
                if response.status_code  == 200:
                    self.__cookie_session = session.cookies.get_dict()['X-Qlik-Session']
                else:
                    raise ValueError('Error when trying to get qlik session cookies.')

            except requests.exceptions.ConnectionError as ex:
                self.log.warning(
                    '%s Tenacity will retry to execute the operation', ex)
                raise ex
            except:
                raise ValueError('Error when trying to get qlik session cookies.')


    def get_conn_init(self) -> requests.Session:
            """
            Returns http session to use with requests. Initialize a session without cookies X-Qlik-Session

            :param headers: additional headers to be passed through as a dictionary
            :type headers: dict
    
            """
            session = requests.Session()

            if self.conn_id:
                conn = self.get_connection(self.conn_id)

                host = conn.host if conn.host else ""
                
                if not host.startswith('https://'):
                    host = 'https://'+host

                self.base_url = host
                
                #Ajout de la clé XRF
                xrfKey = self._generateXRFKey()
                session.headers.update({'X-Qlik-Xrfkey': xrfKey}) # Ajout de la clé XRF dans les headers de la requête HTTP
                session.params.update({'xrfkey':xrfKey}) # Ajout de la clé XRF dans les paramètres de la requête HTTP

                #Ajout de l'authentification via NTLM    
                session.auth = HttpNtlmAuth(conn.login, conn.password)
                #AJout du user-agent
                session.headers.update({"User-Agent":"Windows"})

            return session
    
    def get_conn(self) -> requests.Session:
            """
            Returns http session to use with requests.

            :param headers: additional headers to be passed through as a dictionary
            :type headers: dict
    
            """
            session = self.get_conn_init()
            self.__get_cookies_session()
            session.cookies.set('X-Qlik-Session', self.__cookie_session, domain=self.base_url.strip('https://').strip('http://'))
            return session

    @staticmethod
    def get_ui_field_behaviour() -> Dict:
        """Returns NTLM Windows Connection Behaviour field"""
        
        return {
            "hidden_fields": ['port'],  
            "relabeling": {
                'login':'Windows Account',
                'host':'Qlik Sense URL',
                'schema':'Session Cookie Header Name'

            },
            "placeholders": {
                'host': 'URL of Qlik Sense Server to NTLM Virtual Proxy',
                'login': "USERNAME",
                'schema':'X-Qlik-Session',
            },
        }

