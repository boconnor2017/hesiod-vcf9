# Description: Installs and Configures an Apache Based Depot for VCF9 binaries
# Author: Brendan O'Connor
# Date: July 2025
# Version: 1.0

# Base imports
import os
import stat 
import shutil
import urllib
import requests
import docker 

def create_depot_parent_folder(dir_path):
    #Format of dir_path: /usr/local/drop/newfoldername
    try:
        os.mkdir(dir_path)
        return "Success!"
    except FileExistsError:
        return "ERR: Directory Already Exists."
    except PermissionError:
        return "ERR: Permission Denied."
    except Exception as e:
        return "ERR: An exception has occurred."

def create_depot_sub_folders(dir_path, folder_structure_json_py):
    #Convert the json to a python object before passing into this function
    errlist = []
    for i in range(len(folder_structure_json_py["folder_structure"])):
        try: 
            os.makedirs(dir_path+"/"+folder_structure_json_py["folder_structure"][i]["path"])
            errlist.append(folder_structure_json_py["folder_structure"][i]["path"]+" is a Success!")
        except FileExistsError:
            errlist.append(dir_path+"/"+folder_structure_json_py["folder_structure"][i]["path"]+" Already Exists.")
        except PermissionError:
            errlist.append("ERR: Permission Denied during creation of "+dir_path+"/"+folder_structure_json_py["folder_structure"][i]["path"])
        except Exception as e:
            errlist.append("ERR: An exception has occurred during creation of "+dir_path+"/"+folder_structure_json_py["folder_structure"][i]["path"])
    
    errstatement = ""
    for e in range(len(errlist)):
        errstatement = errstatement+"; "+errlist[e]
    return errstatement

def get_docker_container(container_name):
    client = docker.from_env()
    container = client.containers.get(container_name)
    return container

def remove_docker_container(container_name):
    try:
        container = get_docker_container(container_name)
        container.stop()
        container.remove()
    except docker.errors.NotFound:
        pass

def run_docker_container(image_name, container_name, local_folder, container_folder, htpasswd_path, httpd_conf_path):
    client = docker.from_env()
    container = client.containers.run(
        image_name,
        name=container_name,
        ports={"80/tcp": 8080},  # Map port 80 in container to 8080 on host
        volumes={
            local_folder: {'bind': container_folder, 'mode': 'rw'},
            htpasswd_path: {'bind': '/usr/local/apache2/conf/.htpasswd', 'mode': 'ro'},
            httpd_conf_path: {'bind': '/usr/local/apache2/conf/httpd-auth.conf', 'mode': 'ro'}
        },
        detach=True
    )
    return container

def set_folder_permissions(dir_path, permission):
    for root, dirs, files in os.walk(dir_path):
        for dirname in dirs:
            dirpath = os.path.join(root, dirname)
            os.chmod(dirpath, permission)
        #for filename in files:
        #    filepath = os.path.join(root, filename)
        #    os.chmod(filepath, permission)