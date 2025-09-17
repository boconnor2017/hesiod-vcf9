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
    0. Specs (JSON)
        MGT[]
            hostname
            ip address
            24 CPU
                Expose Hardware Assisted Virtualization to the Guest
            384 GB Memory
            1080 GB Storage
                HD1: 16GB
                HD2: 40GB
                HD3: 1024GB
            CD attach to ISO
        VI[]
            hostname
            ip address
            20 CPU
                Expose Hardware Assisted Virtualization to the Guest
            384 GB Memory
            306 GB Storage
                HD1: 16GB
                HD2: 40GB
                HD3: 250GB
            CD attach to ISO

    1. pcli_create_vms_from_iso(spec)
        1.1 Connect to ESXi Host
        1.2 Build vms from spec
            1.2.1 Enable CPU passthrough
            1.2.2 Establish Boot Options
            1.2.3 Establish Flags
            1.2.4 Create CD Drive and attach ESXi ISO
            1.2.5 Add Disks
        1.3 Start VMs

    2. pcli_prep_hosts_for_vcf(hosts)
        2.1 For each host, configure for VCF

'''

def delete_script_file(script_file_name):
    if os.path.exists(script_file_name):
        os.remove(script_file_name)

def hello_world():
    print("Works.")

def pcli_create_vms_from_iso(host_specs):
    i=0
    while i < len(host_specs):
        print("Test"+ str(i)+": "+host_specs[i]["name_of_vm"])
        i=i+1
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