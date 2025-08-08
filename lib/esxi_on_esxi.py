# Description: Installs and Configures a Nested ESXi from ISO
# Author: Brendan O'Connor
# Date: August 2025
# Version: 1.0

# Base imports
import os
import stat 
import shutil
import urllib
import requests
import docker 
import subprocess
import crypt
import getpass

'''
Workflow:
    1. Create ISO
        1.1. KS.CFG needs to be created
        1.2. Specs for KS.CFG should come from json file vm.json
        1.3. Pause: prompt to continue when ESXi ISO has been mounted to vm
        1.4. Create custom ISO
            1.4.1. Extract ISO to temp dir
            1.4.2. Chmod 755 to the temp dir
            1.4.3. Edit BOOT.CFG and insert kickstart
    2. Upload ISO
        2.1. Prompt user: create new ISO?
        2.2. If Yes: upload custom ISO to datastore1
    3. Build N shell vms with the approprate sizing specs
        1.1. VM specs should come from a json file vm.json
        1.2. CD/DVD Drive: mount custom ISO
        1.3. Boot
    4. Run VCF Prep Script against N vms

'''

def delete_script_file(script_file_name):
    if os.path.exists(script_file_name):
        os.remove(script_file_name)

def hello_world():
    print("Works.")

def pcli_create_vm_from_iso():
    script_file_name = "pcli_create_vm_from_iso.ps1"
    script_raw = populate_var_from_file("lib/scripts/pcli_create_vm_from_iso.script")
    script = script_raw.splitlines()
    #Continue here... need to edit the parameters of script from vm.json
    write_script_to_script_file(script, script_file_name)
    pcli_execute(script_file_name)

def pcli_execute(script_file_name):
    cmd = []
    cmd = ["pwsh", script_file_name]
    err = subprocess.run(cmd, capture_output=True)
    return err


def populate_var_from_file(file_name):
    with open(file_name) as file:
        file_txt = file.read()
        return file_txt

def write_script_to_script_file(script, script_file_name):
    delete_script_file(script_file_name)
    script_file_name = open(script_file_name, "a")
    for line in script:
        script_file_name.writelines(line+'\n')
    script_file_name.close()