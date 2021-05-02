import yaml

try:
    from yaml import CLoader as YamlLoader
except ImportError:
    from yaml import Loader as YamlLoader

from .expand import expand_config
from .rules import BuildRule

class BuildConfReader:
    def __init__(self, conf_text):
        self.expanded_data = expand_config(conf_text)
        self.rules = []
        for target_item in self.expanded_data["targets"].items():
             self.rules.append(BuildRule(*target_item))
    
    def _targets_func(self, target_name):
        out_dict = {}
        type(self)._create_target(
            target_name, self.rules, out_dict)
        return out_dict

    @property
    def container(self):
        return self.expanded_data["container"]

    @property
    def shell(self):
        return self.expanded_data["shell"]

    @property
    def targets_func(self):
        return self._targets_func

    @property
    def artifact(self):
        return self.expanded_data["artifact"]

    @classmethod
    def from_path(cls, file_path, encoding = "utf-8"):
        with open(file_path, "r", encoding = encoding) as file_obj:
            return cls.from_file(file_obj)
    
    @classmethod
    def from_file(cls, file_obj):
        return cls.from_text(yaml.load(file_obj, Loader = YamlLoader))

    @classmethod
    def from_text(cls, text):
        return cls(text)

    @staticmethod
    def _create_target(target_name, rules, out_dict):
        if target_name in out_dict:
            return
        target_data = None
        for rule in rules:
            target_data = rule.match(target_name)
            if target_data is not None:
                break
        if target_data is not None:
            for target_dep in target_data["deps"]:
                BuildConfReader._create_target(
                    target_dep, rules, out_dict)
        else:
            target_data = {
                "command": None,
                "check_exist": True,
                "deps": ()
            }
        out_dict[target_name] = target_data
