
import os
from os.path import join, expanduser, abspath, exists
import shutil
import platform
from enum import Enum
from typing import Optional


class OSName(Enum):
    WIN = "Windows"
    MAC = "Darwin"
    LINUX = "Linux"


def main(name_pkg: str, name_env: Optional[str] = None):
    
    cwd = os.getcwd()
    if name_pkg not in os.listdir(cwd):
        raise FileNotFoundError(
            "Given package was not found. " + 
            "The current working directory might be not root of the repository."
        )
    
    path_site = ""
    os_name = platform.system()
    
    if os_name == OSName.WIN.value:
        path_site = join(".venv", "Lib", "site-packages", name_pkg)
    elif os_name in (OSName.MAC.value, OSName.LINUX.value):
        path_site = join(expanduser("~"),
                        ".local",
                        "share",
                        "virtualenvs",
                        name_env,
                        "lib",
                        "python" + version_python, 
                        "site-packages", 
                        name_pkg)
    else:
        raise OSError(
            "This OS is not supported."
        )
    
    if exists(path_site):
        shutil.rmtree(path_site)

    shutil.copytree(name_pkg, path_site)
    
    
if __name__ == "__main__":
    name_pkg = "can09"
    name_env = ""                       # TODO add env name if in Mac or Linux
    version_python = "3.7"

    main(name_pkg, name_env)
