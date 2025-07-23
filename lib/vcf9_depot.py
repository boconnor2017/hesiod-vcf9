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
import subprocess

def copy_files(src_path, target_path):
    shutil.copy2(src_path, target_path)

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

def create_depot_sub_folders(dir_path, depot_manifest_json_py):
    #Convert the json to a python object before passing into this function
    errlist = []
    for i in range(len(depot_manifest_json_py["folder_structure"])):
        try: 
            os.makedirs(dir_path+"/"+depot_manifest_json_py["folder_structure"][i]["path"])
            errlist.append(depot_manifest_json_py["folder_structure"][i]["path"]+" is a Success!")
        except FileExistsError:
            errlist.append(dir_path+"/"+depot_manifest_json_py["folder_structure"][i]["path"]+" Already Exists.")
        except PermissionError:
            errlist.append("ERR: Permission Denied during creation of "+dir_path+"/"+depot_manifest_json_py["folder_structure"][i]["path"])
        except Exception as e:
            errlist.append("ERR: An exception has occurred during creation of "+dir_path+"/"+depot_manifest_json_py["folder_structure"][i]["path"])
    
    errstatement = ""
    for e in range(len(errlist)):
        errstatement = errstatement+"; "+errlist[e]
    return errstatement

def create_docker_bridge_network(network_name):
    client = docker.from_env()
    try:
        docker_net = client.networks.get(network_name)
        err = network_name+" already exists."
        return err
    except docker.errors.NotFound:
        docker_net = client.networks.create(network_name, driver="bridge")
        err = network_name+" created."
        return err

def get_docker_container(container_name):
    client = docker.from_env()
    container = client.containers.get(container_name)
    return container

def generate_ssl_cert(cert_path, key_path):
    #Runs openssl on the Photon OS
    subprocess.run([
        'openssl', 'req', '-x509', '-nodes', '-days', '365',
        '-newkey', 'rsa:2048',
        '-keyout', key_path,
        '-out', cert_path,
        '-subj', '/CN=localhost'
    ], check=True)

def remove_docker_container(container_name):
    try:
        container = get_docker_container(container_name)
        container.stop()
        container.remove()
    except docker.errors.NotFound:
        pass

def run_httpd_docker_container(image_name, container_name, local_folder, httpd_conf_path, httpd_network):
    client = docker.from_env()
    container = client.containers.run(
        image_name,
        name=container_name,
        ports={"80/tcp": 8080},  # Map port 80 in container to 8080 on host
        volumes={
            local_folder: {'bind': "/usr/local/apache2/htdocs", 'mode': 'rw'},
            httpd_conf_path: {'bind': '/usr/local/apache2/conf/httpd-auth.conf', 'mode': 'ro'}
        },
        detach=True,
        network=httpd_network
    )
    return container

def run_nginx_docker_container(image_name, container_name, nginx_conf_path, cert_path, key_path, htpasswd_path, nginx_network):
    client = docker.from_env()
    container = client.containers.run(
        image=image_name,
        name=container_name,
        ports={'443/tcp': '8443'}, # Map port 443 in container to 8443 on host
        volumes={
            nginx_conf_path: {'bind': '/etc/nginx/nginx.conf', 'mode': 'ro'},
            cert_path: {'bind': '/etc/nginx/cert.pem', 'mode': 'ro'},
            key_path: {'bind': '/etc/nginx/key.pem', 'mode': 'ro'},
            htpasswd_path: {'bind': '/etc/nginx/.htpasswd', 'mode': 'ro'},
        },  
        detach=True,
        network=nginx_network
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