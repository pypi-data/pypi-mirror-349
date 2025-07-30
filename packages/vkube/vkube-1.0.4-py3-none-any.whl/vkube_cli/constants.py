import os

PACKAGE_NAME = "vkube"
VERSION_CHECK_INTERVAL = 24 * 3600  # 24 hours
DOCKER_URL = "https://index.docker.io/v1/"
DOCKER_IMAGE_TAG_URL = "https://hub.docker.com/v2/repositories"
GHCR_URL = "https://ghcr.io"
GHCR_IMAGE_TAG_URL = "https://ghcr.io/v2"
ARCH_X86 = "amd64"

HOME_DIR = os.path.expanduser("~")
VKUBE_CONFIG_PATH = os.path.join(HOME_DIR,".vkube","config.yaml")
DOCKER_CONFIG_PATH = os.path.join(HOME_DIR, ".docker", "config.json")
