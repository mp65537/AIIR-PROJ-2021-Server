import reader #from . import reader
import expand #from . import expand # chack local import
import rules
import targets

project_path = "examples/basic-c-app"

config_data = reader.read_build_config(project_path)
expanded_data = expand.expand_config_tree(config_data)
build_rules = rules.BuildRule.create_list(expanded_data)
targets = targets.BuildTarget.create_dict("all", build_rules)

print("done!!!")