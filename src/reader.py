import os
import yaml

try:
    from yaml import CLoader as YamlLoader
except ImportError:
    from yaml import Loader as YamlLoader

def read_build_config(project_path):
    with open(os.path.join(project_path, "build.yaml"), "r", encoding = "utf-8") as file:
        return yaml.load(file, Loader = YamlLoader)
