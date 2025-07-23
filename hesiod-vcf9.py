# Import Hesiod libraries
from hesiod import lib_general as libgen
from hesiod import lib_json as libjson
from hesiod import lib_logs_and_headers as liblog 
from hesiod import lib_paramiko as libpko 

# Import VCF libraries
from lib import vcf9_depot as depot

# Import Standard Python libraries
import os
import sys

# Import json configuration parameters
env_json_str = libjson.populate_var_from_json_file("json", "lab_environment.json")
env_json_py = libjson.load_json_variable(env_json_str)
vcf_json_str = libjson.populate_var_from_json_file("json", "vcf9_config_template.json")
vcf_json_py = libjson.load_json_variable(vcf_json_str)
depot_manifest_json_str = libjson.populate_var_from_json_file("json", "depot_manifest.json")
depot_manifest_json_py = libjson.load_json_variable(depot_manifest_json_str)
this_script_name = os.path.basename(__file__)
logfile_name = env_json_py["logs"][this_script_name]

# Hesiod Header and Log init
liblog.hesiod_print_header()
liblog.hesiod_log_header(logfile_name)
err = "Successfully imported Hesiod python libraries."
liblog.write_to_logs(err, logfile_name)
err = "Succesfully initialized logs to "+logfile_name
liblog.write_to_logs(err, logfile_name)
err = ""
liblog.write_to_logs(err, logfile_name)

# Local Functions
def _main_(args):
    err = "Retreiving user inputs:"
    liblog.write_to_logs(err, logfile_name)
    arg_len = len(args)
    err = "    "+str(arg_len)+" args passed."
    liblog.write_to_logs(err, logfile_name)

    err = "Initializing default user options."
    liblog.write_to_logs(err, logfile_name)
    user_options = ['n', 'n', 'n']

    err = "Matching user inputs to hesiod menu."
    liblog.write_to_logs(err, logfile_name)
    if '--help' in args:
        err = "    --help found. Initiating HELP menu."
        liblog.write_to_logs(err, logfile_name)
        help_menu()
        sys.exit() 
    if '-depot' in args:
        err = "    -depot found. Initiating depot config."
        liblog.write_to_logs(err, logfile_name)
        depot_config()
        sys.exit()
    else :
        err = "    No options found. Initiating HELP menu."
        liblog.write_to_logs(err, logfile_name)
        help_menu()
        sys.exit()

def depot_config():
    print("Building VCF9 Offline Depot.")
    print("")
    err = "    HOST PREP: Creating SSL and conf Folder structure."
    liblog.write_to_logs(err, logfile_name)
    depot.create_depot_parent_folder(depot_manifest_json_py["depot_config"]["ssl_folder_path"])
    depot.create_depot_parent_folder(depot_manifest_json_py["depot_config"]["htpasswd_folder_path"])
    depot.create_depot_parent_folder(depot_manifest_json_py["depot_config"]["httpd_folder_path"])
    depot.create_depot_parent_folder(depot_manifest_json_py["depot_config"]["nginx_folder_path"])
    err = "    HOST PREP: Generating basic auth with htpasswd."
    liblog.write_to_logs(err, logfile_name)
    depot.generate_htpasswd(depot_manifest_json_py["depot_config"]["username"], depot_manifest_json_py["depot_config"]["password"], depot_manifest_json_py["depot_config"]["htpasswd_path"])
    err = "    HOST PREP: Generating SSL certs with openssl."
    liblog.write_to_logs(err, logfile_name)
    depot.generate_ssl_cert(depot_manifest_json_py["depot_config"]["ssl_cert_path"], depot_manifest_json_py["depot_config"]["ssl_key_path"])
    err = "    HOST PREP: Copying conf files to respective "+depot_manifest_json_py["depot_config"]["local_volume_path"]+"/conf folders"
    liblog.write_to_logs(err, logfile_name)
    depot.copy_files("conf/httpd-auth.conf", depot_manifest_json_py["depot_config"]["httpd_auth_conf_path"])
    depot.copy_files("conf/nginx.conf", depot_manifest_json_py["depot_config"]["nginx_conf_path"])
    depot.copy_files("conf/offline_depot_img01.png", depot_manifest_json_py["depot_config"]["local_volume_path"])
    depot.copy_files("conf/offline_depot_img02.png", depot_manifest_json_py["depot_config"]["local_volume_path"])
    depot.copy_files("conf/index.html", depot_manifest_json_py["depot_config"]["local_volume_path"])
    err = "    HOST PREP: Creating VCF9 Folder structure."
    liblog.write_to_logs(err, logfile_name)
    err = "    "+depot.create_depot_parent_folder(depot_manifest_json_py["depot_config"]["local_volume_path"]+"/VCF9")
    liblog.write_to_logs(err, logfile_name)
    err = "    "+depot.create_depot_sub_folders(depot_manifest_json_py["depot_config"]["local_volume_path"]+"/VCF9", depot_manifest_json_py)
    liblog.write_to_logs(err, logfile_name)
    err = "    HOST PREP: Editing permissions of folder structure."
    liblog.write_to_logs(err, logfile_name)
    permissions_cmd = []
    permissions_cmd = "chmod", "-R", "755", "/usr/local/drop/"
    libgen.run_local_shell_cmd(permissions_cmd)
    err = "    STEP 1: Build docker network."
    liblog.write_to_logs(err, logfile_name)
    err = "        "+depot.create_docker_bridge_network(depot_manifest_json_py["depot_config"]["docker_network_name"])
    err = "    STEP 2: Apache Web Server."
    liblog.write_to_logs(err, logfile_name)
    err = "    Removing existing containers."
    liblog.write_to_logs(err, logfile_name)
    depot.remove_docker_container(depot_manifest_json_py["depot_config"]["httpd_container_name"])
    err = "    Creating HTTPD container."
    liblog.write_to_logs(err, logfile_name)
    depot.run_httpd_docker_container(depot_manifest_json_py["depot_config"]["httpd_container_image"], depot_manifest_json_py["depot_config"]["httpd_container_name"], depot_manifest_json_py["depot_config"]["local_volume_path"], depot_manifest_json_py["depot_config"]["httpd_auth_conf_path"], depot_manifest_json_py["depot_config"]["docker_network_name"])
    err = "    httpd Apache Depot created."
    liblog.write_to_logs(err, logfile_name)
    err = "    STEP 3: NGINX reverse proxy."
    liblog.write_to_logs(err, logfile_name)
    err = "    Removing existing containers."
    liblog.write_to_logs(err, logfile_name)
    depot.remove_docker_container(depot_manifest_json_py["depot_config"]["nginx_container_name"])
    err = "    Creating NGINX container."
    liblog.write_to_logs(err, logfile_name)
    depot.run_nginx_docker_container(depot_manifest_json_py["depot_config"]["nginx_container_image"], depot_manifest_json_py["depot_config"]["nginx_container_name"], depot_manifest_json_py["depot_config"]["nginx_conf_path"], depot_manifest_json_py["depot_config"]["ssl_cert_path"], depot_manifest_json_py["depot_config"]["ssl_key_path"], depot_manifest_json_py["depot_config"]["htpasswd_path"], depot_manifest_json_py["depot_config"]["docker_network_name"])


def help_menu():
    print("HELP MENU: hesiod-vcf9.py [options]")
    print("Options are mandatory. You are seeing this menu because you either entered no options or an unknown option.")
    print("Enter options 1x per run, do not add all parameters at once!")
    print("--help option to see this menu.")
    print("")
    print("")

    
_main_(sys.argv)