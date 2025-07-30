import click
import requests
import os,time
import docker
import json
from requests.exceptions import SSLError
from docker.errors import DockerException

from typing import List, Dict, Any
from pathlib import Path

import vkube_cli.docker_config.credentials as credential
from vkube_cli.utils.decode import decode_token
from vkube_cli.utils.create_docker_client import create_client
from vkube_cli.utils.validate_vkubefile import ContainerValidator
from vkube_cli.utils.validate_vkubefile import VkubefileValidator
from vkube_cli.utils.image import validate_image_name, check_images_exist, get_ghcr_image_digest, get_docker_image_digest
from vkube_cli.utils.file_io import read_file_to_string, read_yaml
from vkube_cli.utils.version import version_check
from vkube_cli.constants import VKUBE_CONFIG_PATH
def create_docker_client():
    try:
        # 尝试通过环境变量创建 Docker 客户端
        client = create_client()
        if client is not None:
            return client
    except ConnectionError as e:
        # 捕获连接相关异常并处理
        print(f"Error: Unable to connect to Docker. {e}")
        return None
    except RuntimeError as e:
        # 捕获其他运行时异常并处理
        print(f"Error: Unexpected runtime error. {e}")
        return None
client = create_docker_client()
if client is None:
    print("Error: Docker client initialization failed. Please make sure Docker is running and try again.")
    exit(1)
@click.command(help="Deploy a containerized application using VKubefile configuration.")
@click.option('-f','--file',default="./VKubefile.yaml",type=click.Path(exists=True),help='Path to the build configuration file. Default is VKubefile.yaml in the current directory.')
@version_check
def deploy(file):
    documents = read_yaml(file)
    if not documents:
        click.echo("VKubefile not exist in current directory")
        return
    vkubefile_validator = VkubefileValidator()
    result, all_errors = vkubefile_validator.validate_vkubefile(documents)
    if not result:
        for error in all_errors:
            print(f"{error}")
        return
    else:
        print("All configurations successfully verified")
    print("------ start ------")
    # vkube deploy pameters
    deploy_cntr_params = []
    # vkube deploy registry auth info
    pvtLogin = []

    # local image digest dict
    local_image_digests = {}
    # remote image path dict
    remote_images = set()
    # docker build params dict
    docker_build_params = {}

    token = documents.get("token", "")
    global_image_registry = documents.get("imageRegistry", "docker")
    containers_configs = documents.get("containers", [])
    # Read the vkube cli configuration file
    config = read_yaml(VKUBE_CONFIG_PATH)
    if not config:
        click.echo("config is empty")
        return
    """Deploy using a VKubefile configuration."""
    registry_auths = {}
    registry_auths[global_image_registry] = get_registry_auth(global_image_registry, config)
    if not registry_auths[global_image_registry]:
        return
    global_registry_user_name = registry_auths[global_image_registry].get("username")

    api_address,secret = decode_token(token)
    us_info = user_service_info(api_address + "/api/v1/k8s/userService",secret)
    if us_info == None or us_info.get("status") not in ["ServicePending", "ServiceRunning", "ServiceStopped"]:
        print("Error: get user service info failed or user service is not available")
        return
    service_options = us_info.get("serviceOptions",{})
    buy_resource_unit_str = service_options.get("resourceUnit")
    container_validator = ContainerValidator(containers_configs)
    resource_validated,_ = container_validator.validate_resources(buy_resource_unit_str)
    if not resource_validated:
        print("Error: resourceUnit or ports validation failed")
        return
  
    for doc in containers_configs:
        registry = global_image_registry
        build_info = doc.get("build", None)
        remote_image_path = doc.get("registryImagePath", None)
        full_img_ref =get_full_img_ref(global_image_registry, global_registry_user_name, doc.get("imageName"), doc.get("tag"))
        if full_img_ref is not None:
           doc["deploy"]["imageName"] = full_img_ref
        # skip the public image that exist in image repository, such as nginx,redis,mysql and so on 
        if remote_image_path is not None:
            validate_tuple = validate_image_name(remote_image_path)
            # the case registry == "" is avoided when validate the VKubbefile.yaml
            if validate_tuple[1] == "docker.io":
               registry = "docker"
            if validate_tuple[1] == "ghcr.io": 
                registry = "ghcr"
            remote_images.add(remote_image_path)
            doc["deploy"]["imageName"] = remote_image_path
        elif build_info is not None:
            # build from local dockerfile
            remote_images.add(full_img_ref)
            # by default, every container using private image should append auth info in cntr deploy parameter
            if doc["tag"] == "":
                doc["tag"] = "latest"
            docker_build_params[full_img_ref] = build_info
        elif full_img_ref is not None:
            # deploy using the local image and push it to remote
            remote_images.add(full_img_ref)
            local_image_digests[full_img_ref] = None
        else:
            click.echo("Error: invalid build or full image path info")
            return
        auth_info = registry_auths.get(registry, None)
        if auth_info is None:
            auth_info = get_registry_auth(registry, config)
            registry_auths[registry] = auth_info
        if auth_info is None:
            return
        pvtLogin.append(auth_info)
        deploy_cntr_params.append(doc["deploy"])
    print("------ deployment start ------")

    # build stage
    for full_img_ref, build_info in docker_build_params.items():
        build_args = get_build_args_dict(build_info)
        context_path = build_info.get("contextPath", ".")
        dockerfile_path = build_info.get("dockerfilePath", "Dockerfile")
        # check dockerfile path
        # build image
        print(f"Image {dockerfile_path} building...")
        success, digest = build_docker_image(full_img_ref, build_args, context_path, dockerfile_path)
        if not success:
            print(f"Error: build image {full_img_ref} failed")
            return
        local_image_digests[full_img_ref] = digest

    # check local image digest
    for local_image_path, digest in local_image_digests.items():
        if digest:
            continue
        ok, digest = get_local_image_digest(local_image_path)
        if not ok:
            print(f"Error: get local image {local_image_path} digest failed")
            return
        local_image_digests[local_image_path] = digest

    # query remote image digest
    if len(remote_images) > 0:
        print("\n------ query remote image digest and check arch info ------")
        remote_image_digests, err_str = check_images_exist(list(remote_images), registry_auths)
        if err_str != "" and not "Image not found" in err_str:
            print(f"Error: check image exist failed, the error is {err_str}")
            return
        # check remoteImagePath if exist in the registry
        for remote_image_path, digest in remote_image_digests.items():
           if not digest and remote_image_path not in local_image_digests:
                print(f"Error: remote registry image path {remote_image_path} not found in the registry")
                return
        print("------ check remote image finished ------")
    # push stage
    pushed_images = []
    for local_image_path, local_digest in local_image_digests.items():
        related_remote_digest = remote_image_digests.get(local_image_path, None)
        if related_remote_digest and local_digest == related_remote_digest:
            print(f"Image {local_image_path} already exists in the remote repository with the same digest. Skipping push.")
            continue
        # push image
        print(f"Image {local_image_path} pushing...")
        if docker_push(local_image_path):
            pushed_images.append(local_image_path)
        else:
            print(f"Error: push image {local_image_path} failed")
            return
    if pushed_images:
        if not wait_for_image_available(pushed_images, registry_auths, max_retries=30, retry_interval=5):
            print(f"Error: One or more than one images is not available in registry after maximum retries")
            return
    # deploy
    if us_info.get("status") != "ServicePending":
        deploy_http_request(deploy_cntr_params, pvtLogin,secret, api_address+"/api/v1/k8s/deployment/update")
    else:
        deploy_http_request(deploy_cntr_params, pvtLogin,secret, api_address+"/api/v1/k8s/deployment")

def build_docker_image(full_img_ref, build_args, context_path=".", dockerfile_path="Dockerfile"):
    try:
        # Convert paths to absolute paths
        context_path = str(Path(context_path).absolute())
        dockerfile_path = str(Path(dockerfile_path).absolute())
        repository = full_img_ref
        build_logs: List[Dict[str, Any]] = []
        print(f"Start building image-->{repository}")
         # Stream build logs
        for line in client.api.build(
            path=context_path,
            dockerfile=dockerfile_path,
            tag=repository,
            rm=True,
            decode=True,
            buildargs=build_args,
            platform='linux/amd64'
        ):
            if 'stream' in line:
                print(line['stream'].strip())
                build_logs.append(line['stream'].strip())
            elif 'status' in line:
                print(line['status'].strip())
                build_logs.append(line['status'].strip())
            elif 'progress' in line:
                print(line['progress'].strip())
            elif 'error' in line:
                build_logs.append(line['error'].strip())
                raise docker.errors.BuildError(reason=line['error'], build_log=build_logs)
            elif 'errorDetail' in line:
                print(f"Error detail: {line['errorDetail']}")
            else:
                print(line)
        print(f"\nSuccessfully built image: {repository}")

        # Get image digest after successful build
        ok, digest = get_local_image_digest(repository)
        if ok and digest:
            print(f"Image digest: {digest}")
            return True, digest
        return True, None

    except DockerException as e:
        print(f"Error while building the image: {str(e)}")
        return False, None
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return False, None
def docker_push(full_img_ref) -> bool:
    
    success = True
    # jsondata = json.dumps(push_response)
    push_logs = []
    try:
        push_response = client.images.push(repository=full_img_ref,stream= True,decode=True)
        for log_line in push_response:
            if 'status' in log_line:
                print(f"Status: {log_line['status'].strip()}")
                push_logs.append(log_line['status'].strip())
            elif 'progress' in log_line:
                print(log_line['progress'].strip())
            elif 'errorDetail' in log_line:
                error_detail = log_line['errorDetail']
                print(f"Error Detail: {error_detail['message']}")
            else:
                print(f"Log Entry: {log_line}")
            if "error" in log_line:
                push_logs.append(log_line['error'].strip())
                success = False  # 如果出现错误，推送失败
                break  # 终止处理，错误已发生

    except Exception as e:
        print(f"pushing image : {e}")
    if success:
        print(f"Image {full_img_ref} pushed successfully!")
        return True
    else:
        print(f"Pushing image encounting error: {push_logs}")
        return False
def deploy_http_request(doc, pvtLogin, secret, deploy_request_url):

    converted_containers = [convert_container_config(container) for container in doc]
    data = {
        "containers": converted_containers,
        "pvtLogin":pvtLogin,
    }
    if secret == "":
        print("parameter invalid")
        return
    headers = {
        "secret":secret,
    }
    print("------ deployment preparation finished ------")
    try: 
        resp = requests.post(deploy_request_url,data=json.dumps(data),headers=headers)
        if resp.status_code != 200:
            print(f"deploy failed,the concrete error is sending http request to {deploy_request_url} failed")
            print(f"Response Body: {resp.text}")
            return 
        else:
            print("deploy successfully")
    except SSLError as ssl_err:
        print(f"SSL Error: {ssl_err}")
        # 可以尝试显式设置 TLS 版本或更新 OpenSSL
        print("Please ensure your OpenSSL and Python versions are up-to-date.")
    except Exception as e:
        print(f"Unexpected Error: {e}")
        print("Please check your code or environment configuration.")

def check_file_is_dockerfile(file_path):
    # directory is none
    if not file_path:
        click.echo("Error: 'dockerfile' entry is missing in the configuration file.", err=True)
        return False, ""
    # file_path is not a file
    if not os.path.isfile(file_path):
        click.echo(f"{file_path} is not a file", err=True)
        return False, ""
    # file endwith Dockerfile
    if file_path.endswith("Dockerfile"):
        path_without_dockerfile = file_path[:-len("Dockerfile")]
        return True, path_without_dockerfile + "."

    else:
        return False,""
def convert_container_config(container):
    config = container.get("configurations",{})
    real_configuration = {}
    for file_path, mount_path in config.items():
        real_configuration[mount_path] = read_file_to_string(file_path)
    new_config = {
        "mountPath": container.get("persistStorage", ""),
        "name": container.get("containerName"),
        "imageName": container.get("imageName"), 
        "resourceUnit": container.get("resourceUnit"), 
        "ports": container.get("ports",[]),
        "envs": container.get("env",[]),
        "configMap": real_configuration,
        "command": container.get("command",[]),
        "args": container.get("args",[])
    }
    return new_config

def user_service_info(request_url,secret):
    headers = {
        "secret":secret,
    }
    try: 
        resp = requests.get(request_url,headers=headers)
        if resp.status_code != 200:
            print(f"Error: get user service info failed,the concrete error is sending http request to {request_url} failed")
            return None
        else:
            print("get user service info successfully")
            return resp.json()
    except SSLError as ssl_err:
        print(f"SSL Error: {ssl_err}")
        # 可以尝试显式设置 TLS 版本或更新 OpenSSL
        print("Please ensure your OpenSSL and Python versions are up-to-date.")
    except Exception as e:
        print(f"Unexpected Error: {e}")
        print("Please check your code or environment configuration.")


def get_build_args_dict(build_doc):
    build_args = {}
    if "buildArgs" in build_doc:
        for build_arg in build_doc["buildArgs"]:
            name = build_arg.get("name", None)
            value = build_arg.get("value", None)
            if name and value:
                build_args[name] = str(value)
    return build_args
def get_full_img_ref(registry_name, username, image_name, tage):
    if not all([registry_name, username, image_name, tage]):
        return None
    
    if registry_name == "docker":
        return "docker.io/" + username + "/" + image_name + ":" + tage
    elif registry_name == "ghcr":
        return "ghcr.io/"  + username + "/" + image_name + ":" + tage
    else:
        click.echo("Error: support Docker and GHCR registries only!")
        return None

def get_local_image_digest(image_name) -> tuple[bool, str]:
    try:
        api_client = docker.APIClient()
        response = api_client.inspect_image(image_name)
        if 'Architecture' in response and 'Os' in response:
            arch = response['Architecture']
            os = response['Os']
            if os != 'linux' or arch not in ['amd64', 'x86_64']:
                print(f"Warning: Image architecture ({os}/{arch}) may not be compatible with linux/amd64")
        # image has been pushed
        if 'RepoDigests' in response and response['RepoDigests']:
            return True, response['RepoDigests'][0].split('@')[1]
        # image has not been pushed
        elif 'Id' in response:
            return True, response['Id']
        return False, "No digest found in image metadata"

    except docker.errors.NotFound:
        return False, "Image not found locally"
    except docker.errors.APIError as e:
        return False, f"API Error: {str(e)}"
    except Exception as e:
        return False, f"Unexpected Error: {str(e)}"

def get_registry_auth(registry_name, config)-> dict[str, str]:
    registry_user_name = credential.check_and_login(registry_name)
    if not registry_user_name:
        click.echo("Login registry failed")
        return None
    auth_info = {
        "username": registry_user_name,
    }
    if registry_name == "docker":
        auth_info["password"] = config.get("DockerhubToken", "")
    elif registry_name == "ghcr":
        auth_info["password"] = config.get("GHCRToken", "")
    if not auth_info["password"]:
        click.echo(f"Please configure the {registry_name} token first")
        return None
    return auth_info

def wait_for_image_available(pushed_images: list, registry_auths: dict, max_retries: int = 10, retry_interval: int = 1) -> bool:
    """check if the pushed images are available in the registry"""
    for i in range(max_retries):
        print(f"Checking if image {pushed_images} are all available in registry (attempt {i + 1}/{max_retries})...")
        remote_image_digests, err_str = check_images_exist(pushed_images, registry_auths)
        if err_str == "" and all(remote_image_digests.get(image) for image in pushed_images):
            print("All images are available in registry.")
            return True
        if i < max_retries - 1:
            print(f"Image not yet available, waiting {retry_interval} seconds before next check...")
            time.sleep(retry_interval)
    return False
    