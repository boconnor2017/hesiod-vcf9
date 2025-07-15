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
folder_structure_json_str = libjson.populate_var_from_json_file("json", "depot_manifest.json")
folder_structure_json_py =libjson.load_json_variable(folder_structure_json_str)
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
    err = "    Removing existing containers."
    liblog.write_to_logs(err, logfile_name)
    depot.remove_docker_container("hesiod-depot")
    err = "    Creating Apache container."
    liblog.write_to_logs(err, logfile_name)
    depot.run_docker_container("httpd:latest", "hesiod-depot", "/usr/local/drop", "/usr/local/apache2/htdocs")
    err = "    Creating VCF9 Folder structure."
    liblog.write_to_logs(err, logfile_name)
    err = "    "+depot.create_depot_parent_folder("/usr/local/drop/VCF9")
    liblog.write_to_logs(err, logfile_name)
    err = "    "+depot.create_depot_sub_folders("/usr/local/drop/VCF9", folder_structure_json_py)
    liblog.write_to_logs(err, logfile_name)
    err = "    Editing permissions of folder structure."
    liblog.write_to_logs(err, logfile_name)
    err = libgen.run_local_shell_cmd('chmod -R 755 /usr/local/drop/')
    liblog.write_to_logs(err, logfile_name)


def help_menu():
    print("HELP MENU: hesiod-vcf9.py [options]")
    print("Options are mandatory. You are seeing this menu because you either entered no options or an unknown option.")
    print("Enter options 1x per run, do not add all parameters at once!")
    print("--help option to see this menu.")
    print("")
    print("")

    
_main_(sys.argv)