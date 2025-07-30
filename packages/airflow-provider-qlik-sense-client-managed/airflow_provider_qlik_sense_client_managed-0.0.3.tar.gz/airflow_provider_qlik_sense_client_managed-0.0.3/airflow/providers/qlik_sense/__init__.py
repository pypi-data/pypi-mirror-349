from __future__ import annotations


def get_provider_info():
    return {
        "package-name": "airflow-provider-qlik-sense-client-managed",
        "name": "Qlik Sense Client Managed Airflow Provider",
        "description": 'Airflow package provider to perform actions on Qlik Sense Client Managed Server.', # Required
        "hooks": [
            {
                "integration-name": "Qlik Sense Client Managed",
                "python-modules": ["airflow.providers.qlik_sense.hooks.qlik_sense_hook", 
                "airflow.providers.qlik_sense.hooks.qlik_sense_hook_ntlm",
                "airflow.providers.qlik_sense.hooks.qlik_sense_hook_cert", 
                "airflow.providers.qlik_sense.hooks.qlik_sense_hook_jwt", 
                ]
            }
            ],
        "operators":[
                        {
                            "integration-name": "Qlik Reload App Operator",
                            "python-modules":["airflow.providers.qlik_sense.operators.reload_app_operator"]
                        },
                        {
                            "integration-name": "Qlik Reload Task Operator",
                            "python-modules":["airflow.providers.qlik_sense.operators.reload_task_operator"]
                        }, 

        ],
        'connection-types': [
            {
                'hook-class-name': 'airflow.providers.qlik_sense.hooks.qlik_sense_hook_cert.QlikSenseHookCert',
                'connection-type': 'qlik_sense_client_managed_cert',
            },
            {
                'hook-class-name': 'airflow.providers.qlik_sense.hooks.qlik_sense_hook_jwt.QlikSenseHookJWT',
                'connection-type': 'qlik_sense_client_managed_jwt',
            },
            {
                'hook-class-name': 'airflow.providers.qlik_sense.hooks.qlik_sense_hook_ntlm.QlikSenseHookNTLM',
                'connection-type': 'qlik_sense_client_managed_ntlm',
            },
        ],
        "versions": ["0.0.2"]
    }