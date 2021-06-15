from copy import deepcopy

from .errors import ExpandError

def expand_config(build_config):
    build_data = deepcopy(build_config)
    if "vars" not in build_data:
        return build_data
    raw_build_vars = build_data["vars"]
    validate_vars(raw_build_vars)
    build_vars = expand_vars_in_vars(raw_build_vars)
    del build_data["vars"]
    vaildate_dict(build_data)
    return expand_vars_in_dict(build_data, build_vars)

def expand_vars_in_dict(input_dict, vars_dict):
    result_dict = {}
    for item_name, item_value in input_dict.items():
        if isinstance(item_value, str):
            result_value = expand_vars_in_string(
                item_value, vars_dict)
        elif isinstance(item_value, list):
            result_value = expand_vars_in_list(
                item_value, vars_dict)
        elif isinstance(item_value, dict):
            result_value = expand_vars_in_dict(
                item_value, vars_dict)
        else:
            result_value = item_value
        result_dict[expand_vars_in_string(
                item_name, vars_dict)] = result_value
    return result_dict

def expand_vars_in_vars(raw_vars_dict):
    result_vars = {}
    missing_vars = []
    for var_name, raw_var_value in raw_vars_dict.items():
        try:
            if isinstance(raw_var_value, list):
                result_vars[var_name] = \
                    expand_vars_in_list(raw_var_value, result_vars)
            else:
                result_vars[var_name] = \
                    expand_vars_in_string(raw_var_value, result_vars)
        except VariableError:
            missing_vars.append(var_name)
    num_of_iter = len(missing_vars)
    for _ in range(0, num_of_iter):
        for var_index in range(len(missing_vars) - 1, -1, -1):
            var_name = missing_vars[var_index]
            raw_var_value = raw_vars_dict[var_name]
            try:
                if isinstance(raw_var_value, list):
                    result_vars[var_name] = \
                        expand_vars_in_list(raw_var_value, result_vars)
                else:
                    result_vars[var_name] = \
                        expand_vars_in_string(raw_var_value, result_vars)
                del missing_vars[var_index]
                break
            except VariableError:
                pass
    if len(missing_vars) > 0:
        raise VariableError("Undetermined values of variables: {}"
            .format(", ".join(missing_vars)))
    return result_vars

def expand_vars_in_list(input_list, vars_dict):
    result_list = []
    for item in input_list:
        if (item[:2] == "$(") and (item[-1:] == ")"):
            var_name = item[2:-1]
            var_value = vars_dict.get(var_name, None)
            if var_value is None:
                raise VariableError("Undeclared variable '{}'".format(var_name))
            if isinstance(var_value, list):
                result_list.extend(var_value)
            else:
                result_list.append(var_value)
            continue
        result_list.append(expand_vars_in_string(item, vars_dict))
    return result_list

def expand_vars_in_string(input_string, vars_dict):
    curr_offset = 0
    result_string = ""
    while True:
        dollar_offset = input_string.find("$", curr_offset)
        expr_offset = dollar_offset + 1
        if (dollar_offset < 0) or (expr_offset >= len(input_string)):
            break
        if input_string[expr_offset] == "(":
            result_string += input_string[curr_offset:dollar_offset]
            var_start_offset = expr_offset + 1
            var_end_offset = input_string.find(")", var_start_offset)
            if var_end_offset < 0:
                raise VarExprError("Expected ')' after '$(' token")
            var_name = input_string[var_start_offset:var_end_offset]
            var_value = vars_dict.get(var_name, None)
            if var_value is None:
                raise VariableError("Undeclared variable '{}'".format(var_name))
            if isinstance(var_value, list):
                var_value = " ".join(var_value)
            result_string += var_value
            curr_offset = var_end_offset + 1
        else:
            result_string += input_string[curr_offset:expr_offset]
            curr_offset = expr_offset
            after_escaped_offset = curr_offset + 2
            if (after_escaped_offset <= len(input_string)) and \
                (input_string[curr_offset:after_escaped_offset] == "$("):
                result_string += "("
                curr_offset = after_escaped_offset
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
            raise BadEntryTypeError("Entries have to be bools, strings, lists or dicts")

def validate_vars(vars_dict):
    for var_name, var_value in vars_dict.items():
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

class BadEntryTypeError(ExpandError):
    pass

class VarExprError(ExpandError):
    pass

class VariableError(ExpandError):
    pass
