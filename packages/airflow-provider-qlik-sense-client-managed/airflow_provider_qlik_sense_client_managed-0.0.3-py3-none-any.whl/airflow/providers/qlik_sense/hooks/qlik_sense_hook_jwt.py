from typing import Any, Callable, Dict, Optional, Union
from wsgiref.validate import validator

import requests
from requests.auth import HTTPBasicAuth

from airflow.exceptions import AirflowException
from airflow.providers.qlik_sense.hooks.qlik_sense_hook import QlikSenseHook
from airflow.hooks.base import BaseHook

class QlikSenseHookJWT(QlikSenseHook):
    """
    Qlik Sense Hook to interract with a On-Promise Site Qlik Sense Server
    :param method: the API method to be called

    """

    conn_name_attr = 'qlik_sense_conn_id'
    default_conn_name = 'qlik_sense_default'
    conn_type = 'qlik_sense_client_managed_jwt'
    hook_name = '[JWT] Qlik Sense Client Managed'
    auth_type = 'JWT'
    
    def __init__(self,conn_id: str = default_conn_name) -> None:
        super().__init__()
        self.conn_id = conn_id
           
    
    def get_conn(self) -> requests.Session:
            """
            Returns http session to use with requests.

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

                #Ajout de l'authentification via JWT    
                headers = {'Authorization': 'Bearer ' + conn.password ,'Content-Type': 'application/json', "User-Agent":"Windows"}
                session.headers.update(headers)

                #Ajout de la clé XRF key
                xrfKey = self._generateXRFKey()
                session.headers.update({'X-Qlik-Xrfkey': xrfKey}) # Ajout de la clé XRF dans les headers de la requête HTTP
                session.params.update({'xrfkey':xrfKey}) # Ajout de la clé XRF dans les paramètres de la requête HTTP
                
                #Ajout du user-agent
                session.headers.update({"User-Agent":"Windows"})

            return session
    
    @staticmethod
    def get_ui_field_behaviour() -> Dict:
        """Returns custom field behaviour"""
        import json

        return {
            "hidden_fields": ['port','login', 'schema'],
             "relabeling": {
                'password':'JWT Token',
                'host':'Qlik Sense URL',
            },
            "placeholders": {
                'host': 'URL of Qlik Sense Server to JWT Virtual Proxy',
                'password': 'JWT Token',
            },
        }

