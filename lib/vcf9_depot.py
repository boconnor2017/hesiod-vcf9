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

# THIS NEEDS TO BE FIXED # # # # # # # # # # # # # # # # # 
def create_depot_sub_folders(dir_path, folder_structure_json_py):
    #Convert the json to a python object before passing into this function
    for folder in folder_structure_json_py["folder_structure"]:
        new_folder_name = folder.get("name")
        if new_folder_name:
            new_path = os.path.join(dir_path, new_folder_name)
            os.makedirs(new_path, exist_ok=True)
            subfolders = folder.get("child", [])
            if subfolders:
                create_depot_sub_folders(subfolders, new_path)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

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

def run_docker_container(image_name, container_name, local_folder, container_folder):
    client = docker.from_env()
    container = client.containers.run(
        image_name,
        name=container_name,
        ports={"80/tcp": 8080},  # Map port 80 in container to 8080 on host
        volumes={local_folder: {'bind': container_folder, 'mode': 'rw'}},
        detach=True
    )
    return container
