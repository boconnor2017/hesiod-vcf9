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

# Custom Functions

def get_depot_settings(vcf_installer_fqdn):
    response = requests.get(vcf_installer_fqdn)
    print(response.json())