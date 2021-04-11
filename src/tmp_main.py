import reader #from . import reader
import expand #from . import expand # chack local import

project_path = "examples/basic-c-app"

config_data = reader.read_build_config(project_path)
expanded_data = expand.expand_config_tree(config_data)

print("done!!!")