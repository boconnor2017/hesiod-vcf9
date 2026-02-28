# Description: Installs and Configures VCF 9
# Author: Brendan O'Connor
# Date: September 2025
# Version: 1.0

# Base imports
import os
import stat 
import shutil
import urllib
import requests
import docker 
import subprocess
import base64
from requests.auth import HTTPBasicAuth
import json

# Custom Functions

def api_get(url, headers):
    requests.packages.urllib3.disable_warnings()
    response = requests.get(url, headers=headers, verify=False)
    return response

def api_post(url, headers, payload):
    requests.packages.urllib3.disable_warnings()
    response = requests.post(url, headers=headers, json=payload, verify=False)
    return response

def vcf_create_token(url, username, password):
    headers = {"Content-Type" : "application/json"}
    payload = {"username": username, "password": password}
    response = api_post(url, headers, payload)
    response.raise_for_status()
    response_json = response.json()
    token = response_json["accessToken"]
    return token

def vcf_deploy_sddc(url, token, vcf_json_py):
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    response = api_post(url, headers, vcf_json_py)
    response.raise_for_status()
    response_json = response.json()
    return response_json

def vcf_get_depot_settings(url, token):
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    response = api_get(url, headers)
    response_json = response.json()
    return response_json

def vcf_get_sddc_tasks(url, token):
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    response = api_get(url, headers)
    response_json = response.json()
    return response_json

