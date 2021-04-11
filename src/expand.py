from copy import deepcopy

def expand_config_tree(build_config):
    build_data = deepcopy(build_config)
    build_vars = build_data["vars"]
    del build_data["vars"]
    validate_vars(build_vars)
    vaildate_dict(build_data)
    return expand_vars_in_dict(build_data, build_vars)

def expand_vars_in_dict(input_dict, build_vars):
    result_dict = {}
    for item_name, item_value in input_dict.items():
        if isinstance(item_value, str):
            result_value = expand_vars_in_string(
                item_value, build_vars)
        elif isinstance(item_value, list):
            result_value = expand_vars_in_list(
                item_value, build_vars)
        elif isinstance(item_value, dict):
            result_value = expand_vars_in_dict(
                item_value, build_vars)
        else:
            result_value = item_value
        result_dict[expand_vars_in_string(
                item_name, build_vars)] = result_value
    return result_dict

def expand_vars_in_list(input_list, build_vars):
    result_list = []
    for item in input_list:
        if (item[:2] == "$(") and (item[-1:] == ")"):
            var_name = item[2:-1]
            var_value = build_vars.get(var_name, None)
            if var_value is None:
                raise DeclarationError("Undeclared variable '{}'".format(var_name))
            if isinstance(var_value, list):
                result_list.extend(var_value)
            else:
                result_list.append(var_value)
            continue
        result_list.append(expand_vars_in_string(item, build_vars))
    return result_list

def expand_vars_in_string(input_string, build_vars):
    curr_offset = 0
    result_string = ""
    while True:
        dollar_offset = input_string.find("$", curr_offset)
        if dollar_offset < 0:
            break
        if input_string[dollar_offset + 1] == "(":
            result_string += input_string[curr_offset:dollar_offset]
            var_start_offset = dollar_offset + 2
            var_end_offset = input_string.find(")", var_start_offset)
            if var_end_offset < 0:
                raise ExpandError("Expected ')' after '$(' token")
            var_name = input_string[var_start_offset:var_end_offset]
            var_value = build_vars.get(var_name, None)
            if var_value is None:
                raise DeclarationError("Undeclared variable '{}'".format(var_name))
            if isinstance(var_value, list):
                var_value = " ".join(var_value)
            result_string += var_value
            curr_offset = var_end_offset + 1
        else:
            new_offset = dollar_offset + 1
            result_string += input_string[curr_offset:new_offset]
            curr_offset = new_offset
    result_string += input_string[curr_offset:]
    return result_string

def vaildate_dict(input_dict):
    for item_name, item_value in input_dict.items():
        if not isinstance(item_name, str):
            raise BadEntryTypeError("Entry names have to be strings")
        if isinstance(item_value, list):
            validate_list(item_value)
        elif isinstance(item_value, dict):
            vaildate_dict(item_value)
        elif not (isinstance(item_value, str) or isinstance(item_value, bool)):
            raise BadEntryTypeError("Variables have to be strings or lists")

def validate_vars(build_vars):
    for var_name, var_value in build_vars.items():
        if not isinstance(var_name, str):
            raise BadEntryTypeError("Variable names have to be strings")
        if isinstance(var_value, list):
            validate_list(var_value)
        elif not isinstance(var_value, str):
            raise BadEntryTypeError("Variables have to be strings or lists")

def validate_list(input_list):
    for item in input_list:
        if not isinstance(item, str):
            raise BadEntryTypeError("Lists could only have string items")

class ExpandError(Exception):
    pass

class BadEntryTypeError(ExpandError):
    pass

class DeclarationError(ExpandError):
    pass
