from typing import Any, Callable, Dict, Optional, Union
from wsgiref.validate import validator

import random
import string

import requests


from airflow.exceptions import AirflowException
from airflow.hooks.base import BaseHook


class QlikSenseHook(BaseHook):
    """
    Qlik Sense Hook to interract with a On-Promise Site Qlik Sense Server
    
    """

    conn_name_attr = 'qlik_sense_conn_id'
    default_conn_name = 'qlik_sense_default'
    conn_type = 'qlik_sense_client_managed'
    hook_name = 'Qlik Sense Client Managed'
    auth_type = None
    base_url = None

    def __init__(self,conn_id: str = default_conn_name,auth_type: str = "ntlm") -> None:
        super().__init__()
        self.conn_id = conn_id
        

    def reload_task(self, taskId: str= ""):
        """
        
        Method used to reload task
        
        """

        URI = '/qrs/task/{id}/start/synchronous'.format(id=taskId)
        method = 'POST'
        ans = self.run(method, endpoint=URI)

        return ans

    def reload_app(self, appId: str= ""):
        """
        
        Method used to reload app
        
        """

        URI = '/qrs/app/{id}/reload'.format(id=appId)
        method = 'POST'
        ans = self.run(method, URI)
        return ans

    
    def check_status_reload(self, appId: str= "", taskId: str= ""):
        """
        
        Method used to check status of a task
        
        """
        
        if appId != "":
            URI = '/qrs/reloadtask?filter=app.id eq {id}'.format(id=appId)
        else:
            URI = '/qrs/reloadtask/{id}'.format(id=taskId)
        
        method = 'GET'
        ans = self.run(method, URI)

        return ans
    
    def check_status_external_task_reload(self, taskId: str= ""):
        """
        
        Method used to check status of an external task
        
        """
        
        URI = '/qrs/externalprogramtask/{id}'.format(id=taskId)
        
        method = 'GET'
        ans = self.run(method, URI)

        return ans


    def download_app(self, appId: str= "", skipData: bool=False):
        """
        
        Method used to download app
        
        """
        
        URI = '/qrs/app/{id}/export/{token}?skipData={skipData}'.format(id=appId, skipData=True)
        method = 'POST'
        ans = self.run(method, URI)

        return ans

    def upload_app(self, appId: str= ""):
        """
        
        Method used to download app
        
        """
        
        URI = '/qrs/app/import?name={name}&keepdata={keepdata}&excludeConnections={excludeConnections}'.format(id=appId, skipData=True)
        method = 'POST'
        ans = self.run(method, URI)

        return ans

    def _generateXRFKey(self):
        return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=16))

    def get_conn(self) -> requests.Session:
        """
        Returns http session to use with requests.

        :param headers: additional headers to be passed through as a dictionary
        :type headers: dict
        """
        
        raise RuntimeError('You cannot used parent class to initialize a Qlik Sense Hook. Please use QlikSenseHookJWT or QlikSenseHookNTLM or QlikSenseHookCert hooks.')

    def run(
        self,
        method: str='GET',
        endpoint: Optional[str] = None,
        data: Optional[Union[Dict[str, Any], str]] = None,
        headers: Optional[Dict[str, Any]] = None,
        **request_kwargs: Any,
    ) -> Any:
        r"""
        Performs the request

        :param endpoint: the endpoint to be called i.e. resource/v1/query?
        :type endpoint: str
        :param data: payload to be uploaded or request parameters
        :type data: dict
        :param headers: additional headers to be passed through as a dictionary
        :type headers: dict
        """

        self.session = self.get_conn()

        if self.base_url and not self.base_url.endswith('/') and endpoint and not endpoint.startswith('/'):
            url = self.base_url + '/' + endpoint
        else:
            url = (self.base_url or '') + (endpoint or '')

        if method == 'GET':
            # GET uses params
            req = requests.Request(
                method, url, headers=headers)
        elif method=='POST':
            # Others use data
            import json
            req = requests.Request(
                method, url, data=json.dumps(data), headers=headers)
        else:
            raise RuntimeError('Method not handle by Qlik Sense Client Managed Provider')

        self.log.info("Sending '%s' to url: %s", method, url)

        prepped = self.session.prepare_request(req)
        try:
            response = self.session.send(prepped, verify=False, allow_redirects=True)
            return response

        except requests.exceptions.ConnectionError as ex:
            self.log.warning(
                '%s Tenacity will retry to execute the operation', ex)
            raise ex


