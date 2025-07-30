"""Setup.py for the Qlik Sense Airflow provider package. Built from datadog provider package for now."""

from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

"""Perform the package airflow-provider-qlik-sense setup."""
setup(
    name='airflow-provider-qlik-sense-client-managed',
    version="0.0.3",
    description='Airflow package provider to perform action into Qlik Sense On-Promise (reload apps, tasks ...).',
    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points={
        "apache_airflow_provider": [
            "provider_info=airflow.providers.qlik_sense.__init__:get_provider_info"
        ]
    },
    license='Apache License 2.0',
    packages=['airflow.providers.qlik_sense', 'airflow.providers.qlik_sense.hooks', 
    'airflow.providers.qlik_sense.operators',],
    install_requires=['apache-airflow>=2.10', 'requests-ntlm2>=6.5.3'],
    setup_requires=['setuptools', 'wheel'],
    author='Clement Parsy',
    author_email='cparsy@decideom.fr',
    url='',
    classifiers=[
        "Framework :: Apache Airflow",
        "Framework :: Apache Airflow :: Provider",
    ],
    python_requires='~=3.9',
)
