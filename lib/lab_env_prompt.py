# Description: Prompts Users to Generate a lab_environment.json variable file
# Author: Brendan O'Connor
# Date: October 2025
# Version: 1.0

# Base imports
import os
import stat 
import shutil
import urllib
import requests
import docker 
import subprocess
import json

# Custom Functions
def delete_script_file(script_file_name):
    if os.path.exists(script_file_name):
        os.remove(script_file_name)

def dump_json_to_file(json_python_obj, json_filename):
    delete_script_file(json_filename)
    json_file = open(json_filename, "w")
    json_dump = json.dump(json_python_obj, json_file, indent = 6)
    return json_dump

def fill_in_the_rest(env_json_py, cd_path, is_management_vlan):
    total_mgt = 4
    total_vi = 4
    mgt_gw = env_json_py["physical_network"][is_management_vlan]["default_gateway"]
    ip_split = mgt_gw.split(".")
    sub = ip_split[0]+"."+ip_split[1]+"."+ip_split[2]+"."
    i=0
    while i < total_mgt:
        env_json_py["nested_esxi_servers"]["management_host_specs"][i]["name_of_vm"] = "hesvcf-esx0"+str(i+1)
        env_json_py["nested_esxi_servers"]["management_host_specs"][i]["nested_esxi_hostname"] = env_json_py["nested_esxi_servers"]["management_host_specs"][i]["name_of_vm"]+env_json_py["domain"]
        env_json_py["nested_esxi_servers"]["management_host_specs"][i]["nested_esxi_ip_address"] = sub+str(i+20)
        env_json_py["nested_esxi_servers"]["management_host_specs"][i]["numCPU"] = "24"
        env_json_py["nested_esxi_servers"]["management_host_specs"][i]["expose_hw_virt_to_guest"] = "yes"
        env_json_py["nested_esxi_servers"]["management_host_specs"][i]["memoryGB"] = "384"
        env_json_py["nested_esxi_servers"]["management_host_specs"][i]["harddisks"][0]["storage_GB"] = "16"
        env_json_py["nested_esxi_servers"]["management_host_specs"][i]["harddisks"][1]["storage_GB"] = "40"
        env_json_py["nested_esxi_servers"]["management_host_specs"][i]["harddisks"][2]["storage_GB"] = "1024"
        env_json_py["nested_esxi_servers"]["management_host_specs"][i]["CD_path"] = cd_path
        env_json_py["nested_esxi_servers"]["management_host_specs"][i]["deploy_to_physical_host"] = 0
        env_json_py["nested_esxi_servers"]["management_host_specs"][i]["deploy_to_datastore"] = 0
        i=i+1
    i=0
    while i < total_vi:
        env_json_py["nested_esxi_servers"]["vi_host_specs"][i]["name_of_vm"] = "hesvcf-esx0"+str(i+1)
        env_json_py["nested_esxi_servers"]["vi_host_specs"][i]["nested_esxi_hostname"] = env_json_py["nested_esxi_servers"]["vi_host_specs"][i]["name_of_vm"]+env_json_py["domain"]
        env_json_py["nested_esxi_servers"]["vi_host_specs"][i]["nested_esxi_ip_address"] = sub+str(i+20)
        env_json_py["nested_esxi_servers"]["vi_host_specs"][i]["numCPU"] = "24"
        env_json_py["nested_esxi_servers"]["vi_host_specs"][i]["expose_hw_virt_to_guest"] = "yes"
        env_json_py["nested_esxi_servers"]["vi_host_specs"][i]["memoryGB"] = "384"
        env_json_py["nested_esxi_servers"]["vi_host_specs"][i]["harddisks"][0]["storage_GB"] = "16"
        env_json_py["nested_esxi_servers"]["vi_host_specs"][i]["harddisks"][1]["storage_GB"] = "40"
        env_json_py["nested_esxi_servers"]["vi_host_specs"][i]["harddisks"][2]["storage_GB"] = "1024"
        env_json_py["nested_esxi_servers"]["vi_host_specs"][i]["CD_path"] = cd_path
        env_json_py["nested_esxi_servers"]["vi_host_specs"][i]["deploy_to_physical_host"] = 0
        env_json_py["nested_esxi_servers"]["vi_host_specs"][i]["deploy_to_datastore"] = 0
        i=i+1
    return env_json_py

def main(env_json_py):
    #env_json_py does not have to be populated - this variable is used only for the structure
    print("")
    print("")
    print("* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * ")
    print(" * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *")
    print("* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * ")
    print(" * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *")
    print("Welcome to the lab_environment.json quick start.")
    print("")
    print("The purpose of this script is to provide you with an accelerated, pain free process to populate configuration details for hesiod-vcf9. Here are some FAQs:")
    print("    Q: What is lab_environment.json?")
    print("    A: lab_environment.json is a configuration file that tells the automation how to connect to the resources in your lab and how to configure VCF.")
    print("    Q: Do I have to run this every time I want to build VCF?")
    print("    A: No. You should only have to run this once.")
    print("    Q: Can I edit the json directly?")
    print("    A: Yes. In fact, for more advanced automation capabilities it is recommended that you interact with the lab_environment.json directly.")
    print("    Q: Does the lab_environment.json file replace the planning and preparation workbook for VCF?")
    print("    A: Yes. But only in the context of this repository. Don't try to use lab_environment.json as an alternative for standard VCF deployments.")
    print("    Q: What do you mean by \"accelerated, pain free\" process to populate lab_environment.json file?")
    print("    A: Use this prompt if you don't care about naming conventions for VCF. This prompt will only ask you minimal questions so you can get started on the important stuff.")
    print("    Q: How do I know when this prompt is making assumptions?")
    print("    A: The prompt will tell you when it is blatently cutting corners. Look for the word \"ASSUMPTION\".")
    print("    Q: What if my prerequisites aren't done yet?")
    print("    A: No problem. The output of this script is nothing more than a json file. Run this as many times as you like. Nothing is actually deployed from this prompt.")
    print("    Q: What if I don't know the answer to a question?")
    print("    A: Hit Ctrl+C to cancel the process. When you know the answer, kick it off again.")
    print("    Q: If I cancel midway through this process, will it save my answers?")
    print("    A: No. This is designed to repave.")
    print("    Q: Can I edit the file AFTER I've completed this prompt?")
    print("    A: Yes. Run ls -l after you've completed the questions below. Then vi into the lab_environment.json file to make your edits.")
    print("    Q: How do I apply the configuration details to my next module?")
    print("    A: Replace json/lab_environment.json with the output of this prompt. Then run your next module.")
    print("")
    print("")
    ans1 = input("Would you like to proceed? [y/n]")
    if ans1.upper() == "Y":
        print("    Great! Let us begin...")
        print("")
        print("")
        print("* * * * * * PART 1 * * * * * * ")
        print("The following questions pertain to your physical network:")
        print("ASSUMPTION: for speed and efficiency this process will assume /24 CIDR block networks.")
        network_count = input("    How many physical networks do you want to incorporate into this lab environment? (Recommended: at least 4)")
        idx = int(network_count)
        i=0
        is_management_vlan = 0 #default
        while i < idx:
            print("        Network "+str(i)+":")
            env_json_py["physical_network"][i]["default_gateway"] = input("        Default Gateway: [example: 10.0.0.1]")
            env_json_py["physical_network"][i]["subnet_mask"] = "255.255.255.0"
            print("        Subnet Mask: 255.255.255.0 [hardcoded]")
            env_json_py["physical_network"][i]["cidr"] = "24"
            print("        CIDR: 24 [hardcoded]")
            env_json_py["physical_network"][i]["network_typ"] = input("        Network Type: [example: VCF 9 Management VLAN]")
            ans2 = input("        Is this network going to be used as the VCF Management VLAN (only answer \"y\" ONCE)? [y/n]")
            if ans2.upper() == "Y":
                is_management_vlan = i 
            else:
                is_management_vlan = 0
            i=i+1
        print("")
        print("")
        print("* * * * * * PART 2 * * * * * * ")
        print("The following questions pertain to your physical servers:")
        server_count = input("    How many physical servers do you want to incorporate into this lab environment? (Recommended: at least 1)")
        idx = int(server_count)
        i=0
        while i < idx:
            env_json_py["physical_server"][i]["username"] = input("        ESXi Host Username: [example: root]")
            env_json_py["physical_server"][i]["password"] = input("        ESXi Host Password: [example: VMw@re123!]")
            env_json_py["physical_server"][i]["ip_address"] = input("        ESXi Host IP Address: [example: 10.0.0.10]")
            env_json_py["physical_server"][i]["server_type"] = input("        ESXi Host Server Type (optional): [example: Supermicro 001]")
            env_json_py["physical_server"][i]["deploy_vms_to_this_network"] = input("        Network Port Group to Deploy VMs to: [example: VM Network]")
            datastore_count = input("        How many datastores are on this ESXi host?")
            idy = int(datastore_count)
            y = 0
            while y < idy:
                env_json_py["physical_server"][i]["deploy_vms_to_this_datastore"][y] = input("        Datastore "+str(y)+" Name: [example: Datastore"+str(y+1)+"]")
                y=y+1
            i=i+1
        print("")
        print("")
        print("* * * * * * PART 3 * * * * * * ")
        print("The following questions pertain to your password policy:")
        print("ASSUMPTION: for speed and efficiency this process will assume you want to use a compliant (easy to remember) password for everything.")
        env_json_py["universal_authentication"]["virtual_password"] = ""
        print("        Physical Password: blank [hardcoded]")
        env_json_py["universal_authentication"]["virtual_password"] = "VMw@re123!VMw@re123!"
        print("        Virtual Password: VMw@re123!VMw@re123! [hardcoded]")
        env_json_py["universal_authentication"]["mpc_password"] = "VMw@re123!VMw@re123!"
        print("        MPC Password: VMw@re123!VMw@re123! [hardcoded]")
        print("")
        print("")
        print("* * * * * * PART 4 * * * * * * ")
        print("The following questions pertain to your domain controllers:")
        dns_count = input("    How many DNS servers do you want to incorporate into this lab environment? (Recommended: at least 1, no more than 2)")
        idx = int(dns_count)
        i=0
        while i < idx:
            env_json_py["dns"] = input("        DNS Server "+str(i+1)+": [example: 10.0.0.9]")
            i=i+1
        env_json_py["ntp"]["server"] = input("        NTP Server: [example: pool.ntp.org]")
        env_json_py["domain"] = input("        Domain: [example: hesiod.local]")
        print("")
        print("")
        print("* * * * * * PART 5 * * * * * * ")
        print("The following questions pertain to the location of your ESXi ISO:")
        cd_path = input("        Path to your ESXi ISO: [example: [datastore1] ISO/VMware-ESXi-9.0.1.iso]")
        print("And that's it! The questions are completed. The rest will be done for you based on your answers above.")
        print("Filling in the rest now... (wait a second)")
        env_json_py = fill_in_the_rest(env_json_py, cd_path, is_management_vlan)
        print("Done. Now printing to lab_environment.json file... (wait a second)")
        dump_json_to_file(env_json_py, "lab_environment.json")
    else:
        return env_json_py
    
