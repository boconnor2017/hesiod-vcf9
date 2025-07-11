import docker
import os

# Configuration
image_name = "httpd:latest"
container_name = "chatgpt_apache_v4"
local_folder = "/usr/local/drop"
container_folder = "/usr/local/apache2/htdocs"



def test(image_name, container_name, local_folder, container_folder):
    client = docker.from_env()
    container = client.containers.run(
        image_name,
        name=container_name,
        ports={"80/tcp": 8080},  # Map port 80 in container to 8080 on host
        volumes={local_folder: {'bind': container_folder, 'mode': 'rw'}},
        detach=True
    )
    return container

container = test(image_name, container_name, local_folder, container_folder)