class BuildTarget:
    def __init__(self, name, command, check_exist = True, depends = ()):
        self._name = name
        self._check_exist = check_exist
        self._command = command
        self._depends = depends

    @property
    def name(self):
        return self._name

    @property
    def check_exist(self):
        return self._check_exist

    @property
    def command(self):
        return self._command

    @property
    def depends(self):
        return self._depends

    @classmethod
    def create_dict(cls, target_name, build_rules):
        targets_dict = {}
        cls._create_tree(target_name, build_rules, targets_dict)
        return targets_dict

    @classmethod
    def _create_tree(cls, target_name, build_rules, targets_dict):
        existing_target = targets_dict.get(target_name, None)
        if existing_target is not None:
            return existing_target
        target_data = None
        for rule in build_rules:
            target_data = rule.get_data_if_match(target_name)
            if target_data is not None:
                break
        if target_data is not None:
            dep_obj_list = []
            for target_dep in target_data["depends"]:
                dep_obj_list.append(cls._create_tree(
                    target_dep, build_rules, targets_dict))
            target_obj = cls(target_name,
                target_data["command"],
                target_data["check_exist"],
                tuple(dep_obj_list))
        else:
            target_obj = cls(target_name, None)
        targets_dict[target_name] = target_obj
        return target_obj
