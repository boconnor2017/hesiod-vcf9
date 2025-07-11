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
