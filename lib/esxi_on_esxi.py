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

def pcli_create_vms_from_iso(env_json_py, mgt, vi):
    # Import Keystrokes powershell script
    set_vm_keystrokes_script_name = "Set-VMKeystrokes.ps1"
    set_vm_keystrokes_script_raw = populate_var_from_file("lib/scripts/pcli_set_vm_keystrokes.script")
    set_vm_keystrokes_script = set_vm_keystrokes_script_raw.splitlines()
    write_script_to_script_file(set_vm_keystrokes_script, set_vm_keystrokes_script_name)
    # Import create vm from ISO script
    create_vm_from_iso_script_name = "pcli_create_vm_from_iso.ps1"
    create_vm_from_iso_script_raw = populate_var_from_file("lib/scripts/pcli_create_vm_from_iso.script")
    create_vm_from_iso_script = create_vm_from_iso_script_raw.splitlines()
    write_script_to_script_file(create_vm_from_iso_script, create_vm_from_iso_script_name)
    # Customize the script for Management
    if mgt:
        print("Building nested management cluster:")
        i=0
        while i < len(env_json_py["nested_esxi_servers"]["management_host_specs"]):
            print("    Creating ESXi Host"+ str(i)+": "+env_json_py["nested_esxi_servers"]["management_host_specs"][i]["name_of_vm"])
            # Create temp PowerCLI script for populated input variables
            shutil.copy(create_vm_from_iso_script_name, str(i)+"_"+create_vm_from_iso_script_name)
            new_create_vm_from_iso_script_name = str(i)+"_"+create_vm_from_iso_script_name
            # Find and Replace Server Input Variables from Script
            search_and_replace_in_file("ID:SIV-001", env_json_py["physical_server"][env_json_py["nested_esxi_servers"]["management_host_specs"][i]["deploy_to_physical_host"]]["ip_address"], new_create_vm_from_iso_script_name)
            search_and_replace_in_file("ID:SIV-002", env_json_py["physical_server"][env_json_py["nested_esxi_servers"]["management_host_specs"][i]["deploy_to_physical_host"]]["username"], new_create_vm_from_iso_script_name)
            search_and_replace_in_file("ID:SIV-003", env_json_py["physical_server"][env_json_py["nested_esxi_servers"]["management_host_specs"][i]["deploy_to_physical_host"]]["password"], new_create_vm_from_iso_script_name)
            search_and_replace_in_file("ID:SIV-004", env_json_py["physical_server"][env_json_py["nested_esxi_servers"]["management_host_specs"][i]["deploy_to_physical_host"]]["deploy_vms_to_this_datastore"][env_json_py["nested_esxi_servers"]["management_host_specs"][i]["deploy_to_datastore"]], new_create_vm_from_iso_script_name)
            search_and_replace_in_file("ID:SIV-005", env_json_py["nested_esxi_servers"]["management_host_specs"][i]["CD_path"], new_create_vm_from_iso_script_name)
            # Find and Replace VM Input Variables from Script
            search_and_replace_in_file("ID:VIV-001", env_json_py["nested_esxi_servers"]["management_host_specs"][i]["name_of_vm"], new_create_vm_from_iso_script_name)
            search_and_replace_in_file("ID:VIV-002", env_json_py["nested_esxi_servers"]["management_host_specs"][i]["numCPU"], new_create_vm_from_iso_script_name)
            search_and_replace_in_file("ID:VIV-003", env_json_py["nested_esxi_servers"]["management_host_specs"][i]["memoryGB"], new_create_vm_from_iso_script_name)
            search_and_replace_in_file("ID:VIV-004", env_json_py["nested_esxi_servers"]["management_host_specs"][i]["harddisks"][0]["storage_GB"], new_create_vm_from_iso_script_name)
            search_and_replace_in_file("ID:VIV-005", env_json_py["nested_esxi_servers"]["management_host_specs"][i]["harddisks"][1]["storage_GB"], new_create_vm_from_iso_script_name)
            search_and_replace_in_file("ID:VIV-006", env_json_py["nested_esxi_servers"]["management_host_specs"][i]["harddisks"][2]["storage_GB"], new_create_vm_from_iso_script_name)
            search_and_replace_in_file("ID:VIV-007", env_json_py["physical_server"][env_json_py["nested_esxi_servers"]["management_host_specs"][i]["deploy_to_physical_host"]]["deploy_vms_to_this_network"], new_create_vm_from_iso_script_name)
            # Find and Replace Nested ESXi Input Variables from Script
            search_and_replace_in_file("ID:EIV-001", env_json_py["nested_esxi_servers"]["management_host_specs"][i]["nested_esxi_ip_address"], new_create_vm_from_iso_script_name)
            search_and_replace_in_file("ID:EIV-002", env_json_py["physical_network"][1]["subnet_mask"], new_create_vm_from_iso_script_name)
            search_and_replace_in_file("ID:EIV-003", env_json_py["physical_network"][1]["default_gateway"], new_create_vm_from_iso_script_name)
            search_and_replace_in_file("ID:EIV-004", env_json_py["dns"][0], new_create_vm_from_iso_script_name)
            search_and_replace_in_file("ID:EIV-005", env_json_py["dns"][1], new_create_vm_from_iso_script_name)
            search_and_replace_in_file("ID:EIV-006", env_json_py["nested_esxi_servers"]["management_host_specs"][i]["nested_esxi_hostname"], new_create_vm_from_iso_script_name)
            # Build Nested ESXi VM
            pcli_execute(new_create_vm_from_iso_script_name)
            # Cleanup
            delete_script_file(new_create_vm_from_iso_script_name)
            print("    Finished building ESXi Host"+ str(i)+": "+env_json_py["nested_esxi_servers"]["management_host_specs"][i]["name_of_vm"])
            i=i+1
    # Customize the script for VI
    if vi:
        print("Building nested vi cluster:")
        i=0
        while i < len(env_json_py["nested_esxi_servers"]["vi_host_specs"]):
            print("    ESXi Host"+ str(i)+": "+env_json_py["nested_esxi_servers"]["vi_host_specs"][i]["name_of_vm"])
            i=i+1

def pcli_execute(script_file_name):
    cmd = []
    cmd = ["pwsh", script_file_name]
    err = subprocess.run(cmd, capture_output=True)
    return err

def pcli_prep_hosts_for_vcf(env_json_py, mgt, vi): 
    # Import prep esxi hosts for vcf script
    prep_esxi_hosts_for_vcf_script_name = "pcli_prep_esxi_hosts_for_VCF.ps1"
    prep_esxi_hosts_for_vcf_script_raw = populate_var_from_file("lib/scripts/prep_esxi_hosts_for_VCF.script")
    prep_esxi_hosts_for_vcf_script = prep_esxi_hosts_for_vcf_script_raw.splitlines()
    write_script_to_script_file(prep_esxi_hosts_for_vcf_script, prep_esxi_hosts_for_vcf_script_name)
    # Customize the script for Management
    if mgt:
        print("Prepping Hosts for VCF:")
        hostlist = "\""
        i=0
        while i < len(env_json_py["nested_esxi_servers"]["management_host_specs"]):
            print("    Prepping ESXi Host"+ str(i)+": "+env_json_py["nested_esxi_servers"]["management_host_specs"][i]["name_of_vm"])
            # Create list of hosts
            hostlist = hostlist+env_json_py["nested_esxi_servers"]["management_host_specs"][i]["nested_esxi_ip_address"]+"\", "
            # Lookup network
            search_and_replace_in_file("ID:SIV-006", env_json_py["physical_server"][env_json_py["nested_esxi_servers"]["management_host_specs"][i]["deploy_to_physical_host"]]["deploy_vms_to_this_network"], prep_esxi_hosts_for_vcf_script_name)
            i=i+1
        # Remove comma from the last host
        hostlist = hostlist[:-2]
        # Search and Replace Server Input Variables
        search_and_replace_in_file("ID:SIV-001", hostlist, prep_esxi_hosts_for_vcf_script_name)
        search_and_replace_in_file("ID:SIV-002", env_json_py["ntp"]["server"], prep_esxi_hosts_for_vcf_script_name)
        search_and_replace_in_file("ID:SIV-003", "root", prep_esxi_hosts_for_vcf_script_name) #hardcoded
        search_and_replace_in_file("ID:SIV-004", env_json_py["universal_authentication"]["virtual_password"], prep_esxi_hosts_for_vcf_script_name)
        search_and_replace_in_file("ID:SIV-005", "vSwitch0", prep_esxi_hosts_for_vcf_script_name) #hardcoded
        search_and_replace_in_file("ID:SIV-006", "0", prep_esxi_hosts_for_vcf_script_name) #hardcoded
        # Prep the Hosts
        pcli_execute(prep_esxi_hosts_for_vcf_script_name)

def populate_var_from_file(file_name):
    with open(file_name) as file:
        file_txt = file.read()
        return file_txt

def search_and_replace_in_file(searchtext, replacewithtext, filename):
    line = populate_var_from_file(filename)
    newline = line.replace(searchtext, replacewithtext)
    delete_script_file(filename)
    filename = open(filename, "a")
    for line in newline:
        filename.writelines(line)
    filename.close()

def write_script_to_script_file(script, script_file_name):
    delete_script_file(script_file_name)
    script_file_name = open(script_file_name, "a")
    for line in script:
        script_file_name.writelines(line+'\n')
    script_file_name.close()