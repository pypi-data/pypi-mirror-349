from typing import Any, Callable, Dict, Optional

from airflow.models import BaseOperator
from airflow.hooks.base import BaseHook
from airflow.providers.qlik_sense.hooks.qlik_sense_hook_ntlm import QlikSenseHookNTLM
from airflow.providers.qlik_sense.hooks.qlik_sense_hook_jwt import QlikSenseHookJWT
from airflow.providers.qlik_sense.hooks.qlik_sense_hook_cert import QlikSenseHookCert

class QlikSenseReloadTaskOperator(BaseOperator):
    """
    Trigger a reload task of the app id passed in params.

    :conn_id: connection to run the operator with it
    :appId: str
    
    """

    # Specify the arguments that are allowed to parse with jinja templating
    template_fields = ['taskId']

    #template_fields_renderers = {'headers': 'json', 'data': 'py'}
    template_ext = ()
    ui_color = '#00873d'

    def __init__(self, *, taskId: str = None, conn_id: str = 'qlik_conn_sample', waitUntilFinished: bool = True, **kwargs: Any,) -> None:
        super().__init__(**kwargs)
        self.conn_id = conn_id
        self.conn_type = BaseHook.get_connection(self.conn_id).conn_type
        self.taskId = taskId
        self.waitUntilFinished = waitUntilFinished
        
    def execute(self, context: Dict[str, Any]) -> Any:

        self.log.info("Initiate Hook")
        if self.conn_type == 'qlik_sense_client_managed_ntlm':
            self.log.info("Initiating NTLM Hook")
            hook = QlikSenseHookNTLM(conn_id=self.conn_id)
        elif self.conn_type == 'qlik_sense_client_managed_cert':
            self.log.info("Initiating Certificate Hook")
            hook = QlikSenseHookCert(conn_id=self.conn_id)
        elif self.conn_type == 'qlik_sense_client_managed_jwt':
            self.log.info("Initiating Bearer Hook")
            hook = QlikSenseHookJWT(conn_id=self.conn_id)

        self.log.info("Call HTTP method to reload task {}".format(self.taskId))

        response = hook.reload_task(self.taskId)

        if self.waitUntilFinished:
            flag=True
            while flag:
                ans = hook.check_status_reload(taskId=self.taskId)
                self.log.info('Statut de la tâche: {}'.format(ans.text))
                if ans.status_code == 200:
                    body = ans.json()
                    reloadStatus = body['operational']['lastExecutionResult']['status']
                    if reloadStatus in [7]:
                        flag=False 
                    if reloadStatus in [5,6,4,8,11]:
                        flag=False 
                else:
                    raise ValueError("API Error return")

        self.log.info('Status Code Return {}'.format(response.status_code))
        self.log.info('Answer Return {}'.format(response.text))
        return response.text
