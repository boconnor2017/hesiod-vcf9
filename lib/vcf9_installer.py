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
import sys
import ssl
import socket
import hashlib

# Custom Functions

def api_get(url, headers):
    requests.packages.urllib3.disable_warnings()
    response = requests.get(url, headers=headers, verify=False)
    return response

def api_post(url, headers, payload):
    requests.packages.urllib3.disable_warnings()
    response = requests.post(url, headers=headers, json=payload, verify=False)
    return response

def get_thumbprint(host, port):
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    with socket.create_connection((host, port)) as sock:
        with context.wrap_socket(sock, server_hostname=host) as ssock:
            cert_der = ssock.getpeercert(binary_form=True)
    fingerprint = hashlib.sha256(cert_der).hexdigest().upper()
    sha256_fingerprint = ":".join(fingerprint[i:i+2] for i in range(0, len(fingerprint), 2))
    return sha256_fingerprint

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

def vcf_validate_depot_connection_status(depot_settings_json_py):
    if depot_settings_json_py["vmwareAccount"]["status"] != "DEPOT_CONNECTION_SUCCESSFUL":
        continue_prompt = input("Depot is not connected. Retry? [Y/N]")
        if continue_prompt == "Y":
            vcf_validate_depot_connection_status
        else:
            sys.exit()
    else:
        return True

