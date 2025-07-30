from typing import Any, Callable, Dict, Optional, Union
from wsgiref.validate import validator

import requests
from requests.auth import HTTPBasicAuth

from airflow.exceptions import AirflowException
from airflow.providers.qlik_sense.hooks.qlik_sense_hook import QlikSenseHook
from airflow.hooks.base import BaseHook


class QlikSenseHookCert(QlikSenseHook):
    """
    Qlik Sense Hook to interract with a On-Promise Site Qlik Sense Server
    
    """

    conn_name_attr = 'qlik_sense_conn_id'
    default_conn_name = 'qlik_sense_default'
    conn_type = 'qlik_sense_client_managed_cert'
    hook_name = '[CERT] Qlik Sense Client Managed'
    auth_type = 'CERT'

    def __init__(self,conn_id: str = default_conn_name) -> None:
        super().__init__()
        self.conn_id = conn_id
        self.base_url: str = ""

    
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
                
                #Ajout de la clé XRF
                xrfKey = self._generateXRFKey()
                session.headers.update({'X-Qlik-Xrfkey': xrfKey}) # Ajout de la clé XRF dans les headers de la requête HTTP
                session.params.update({'xrfkey':xrfKey}) # Ajout de la clé XRF dans les paramètres de la requête HTTP
                
                #Ajout de l'authentificaition par certificat
                session.cert = conn.extra__qlik_sense_client_managed__client_pem

                #Ajout de l'identité utilisée par l'authentification par certificat
                headersAuth = {"X-Qlik-User":"UserDirectory={UD}: UserId={UID}".format(UD= conn.extra.extra__qlik_sense_client_managed__qlik_user_directory, 
                                                                                       UID=conn.extra.extra__qlik_sense_client_managed__qlik_account
                                                                                        )}
                session.headers.update(headersAuth)    
                #Ajout du User-Agent
                session.headers.update({"User-Agent":"Windows"})

            return session
    

    @staticmethod
    def get_connection_form_widgets() -> Dict[str, Any]:
        """Returns connection widgets to add to connection form"""
        from flask_appbuilder.fieldwidgets import BS3PasswordFieldWidget, BS3TextFieldWidget
        from flask_babel import lazy_gettext
        from wtforms.fields import PasswordField, StringField, BooleanField
        from wtforms.validators import InputRequired

        return {
            "extra__qlik_sense_client_managed__client_pem": StringField(
                lazy_gettext('Client cert'), widget=BS3TextFieldWidget()
            ),
            "extra__qlik_sense_client_managed__client_key": StringField(
                lazy_gettext('Client key'), widget=BS3TextFieldWidget()
            ),
            "extra__qlik_sense_client_managed__qlik_account": StringField(
                lazy_gettext('Qlik Account'), widget=BS3TextFieldWidget()
            ),
            "extra__qlik_sense_client_managed__qlik_user_directory": StringField(
                lazy_gettext('Qlik User Directory'), widget=BS3TextFieldWidget()
            ),
        }

    @staticmethod
    def get_ui_field_behaviour() -> Dict:
        """Returns custom field behaviour"""
        import json

        return {
            "hidden_fields": ['port', 'schema', 'login', 'password'],
            "relabeling": {},
            "placeholders": {
                'host': 'URL of Qlik Sense Server',
                'extra__qlik_sense_client_managed__client_pem': 'Filepath to client.pem',
                'extra__qlik_sense_client_managed__client_key': 'Filepath to client.key',
                'extra__qlik_sense_client_managed__qlik_account': 'Qlik Sense Account',
                'extra__qlik_sense_client_managed__qlik_user_directory': 'Qlik Sense User Directory',
            },
        }

