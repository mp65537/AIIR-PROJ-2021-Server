import os
import yaml

try:
    from yaml import CLoader as YamlLoader, CDumper as YamlDumper
except ImportError:
    from yaml import Loader as YamlLoader, Dumper as YamlDumper

project_path = "examples/basic-c-app"

with open(os.path.join(project_path, "build.yaml"), "r", encoding = "utf-8") as file:
    dict = yaml.load(file, Loader = YamlLoader)
print("done!")
