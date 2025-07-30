from typing import Any, Callable, Dict, Optional
import time

from airflow.exceptions import AirflowException
from airflow.models import BaseOperator
from airflow.hooks.base import BaseHook
from airflow.providers.qlik_sense.hooks.qlik_sense_hook_ntlm import QlikSenseHookNTLM
from airflow.providers.qlik_sense.hooks.qlik_sense_hook_jwt import QlikSenseHookJWT
from airflow.providers.qlik_sense.hooks.qlik_sense_hook_cert import QlikSenseHookCert

class QlikSenseReloadAppOperator(BaseOperator):
    """
    Trigger a reload of the app id passed in params.

    :conn_id: connection to run the operator with it
    :appId: str
    
    """

    # Specify the arguments that are allowed to parse with jinja templating
    template_fields = ['app_id']

    #template_fields_renderers = {'headers': 'json', 'data': 'py'}
    template_ext = ()
    ui_color = '#00873d'

    def __init__(self, *, app_id: str = None, conn_id: str = 'qlik_conn_sample', waitUntilFinished: bool = True, **kwargs: Any,) -> None:
        super().__init__(**kwargs)
        self.conn_id = conn_id
        self.log.info(BaseHook.get_connection(self.conn_id))
        self.conn_type = BaseHook.get_connection(self.conn_id).conn_type
        self.waitUntilFinished = waitUntilFinished
        self.app_id = app_id
        
    def execute(self, context: Dict[str, Any]) -> Any:

        self.log.info("Initiate Hook")
        self.log.info('Connection Type Request {}'.format(self.conn_type))
        if self.conn_type == 'qlik_sense_client_managed_ntlm':
            self.log.info("Initiating NTLM Hook")
            hook = QlikSenseHookNTLM(conn_id=self.conn_id)
        elif self.conn_type == 'qlik_sense_client_managed_cert':
            self.log.info("Initiating Certificate Hook")
            hook = QlikSenseHookCert(conn_id=self.conn_id)
        elif self.conn_type == 'qlik_sense_client_managed_jwt':
            self.log.info("Initiating Bearer Hook")
            hook = QlikSenseHookJWT(conn_id=self.conn_id)

        self.log.info("Call HTTP method to reload app {}".format(self.app_id))

        response = hook.reload_app(self.app_id)
        
        if response.status_code not in range(200,300):
            raise ValueError('Erreur lors du lancement du rechargement de l application: {error}'.format(error=response.text))
        else:
            self.log.info(response.text)

        if self.waitUntilFinished:
            time.sleep(10)
            flag=True
            while flag:
                ans = hook.check_status_reload(appId=self.app_id)
                self.log.info('Code Statut de la tâche: {}'.format(ans.status_code))
                self.log.info('Statut de la tâche: {}'.format(ans.text))
                if ans.status_code == 200:
                    body = ans.json()
                    reloadStatus = body[0]['operational']['lastExecutionResult']['status']
                    if reloadStatus in [7]:
                        flag=False 
                    if reloadStatus in [5,6,4,8,11]:
                        flag=False 
                else:
                    raise ValueError("API Error return")

        self.log.info('Status Code Return {}'.format(response.status_code))
        self.log.info('Answer Return {}'.format(response.text))

        return response.text
