import re

class BuildRule:
    def __init__(self, rule_expr, rule_data):
        self._target_regex = type(self)._regex_expr_to_regex(rule_expr)
        self._deps_pattern = [
            type(self)._sub_expr_to_pattern(item) \
                for item in rule_data.get("deps", [])
        ]
        command_sub_expr = rule_data.get("command", None)
        if command_sub_expr is not None:
            self._command_pattern = \
                type(self)._sub_expr_to_pattern(command_sub_expr)
        else:
            self._command_pattern = None
        self._check_exist = rule_data.get("check_exist", True)

    def match(self, target_name):
        if self._target_regex.fullmatch(target_name) is None:
            return None
        target_deps = tuple(
            self._target_regex.sub(item, target_name) \
                for item in self._deps_pattern
        )
        if self._command_pattern is not None:
            target_command = self._target_regex.sub(
                self._command_pattern, target_name)
            target_command = target_command.replace("$@", target_name)
            if len(target_deps) > 0:
                target_command = target_command.replace("$<", target_deps[0])
        else:
            target_command = None
        return {"deps": target_deps, 
                "command": target_command,
                "check_exist": self._check_exist}
    
    @staticmethod
    def _regex_expr_to_regex(input_string):
        curr_offset = 0
        result_string = ""
        while True:
            dollar_offset = input_string.find("$", curr_offset)
            expr_offset = dollar_offset + 1
            if (dollar_offset < 0) or (expr_offset >= len(input_string)):
                break
            if input_string[expr_offset] == "[":
                result_string += re.escape(input_string[curr_offset:dollar_offset])
                re_start_offset = expr_offset + 1
                re_curr_offset = re_start_offset
                while True:
                    re_end_offset = input_string.find("]", re_curr_offset)
                    if re_end_offset < 0:
                        raise RegexExprError("Expected ']' after '$[' token")
                    if input_string[re_end_offset - 1] != "\\":
                        break
                    re_curr_offset = re_end_offset + 1
                re_string = "(" + input_string[re_start_offset:re_end_offset] \
                    .replace("\\[", "[").replace("\\]", "]") + ")"
                result_string += re_string
                curr_offset = re_end_offset + 1
            else:
                result_string += re.escape(input_string[curr_offset:expr_offset])
                curr_offset = expr_offset
                after_escaped_offset = curr_offset + 2
                if (after_escaped_offset <= len(input_string)) and \
                    (input_string[curr_offset:after_escaped_offset] == "$["):
                    result_string += re.escape("[")
                    curr_offset = after_escaped_offset
        result_string += re.escape(input_string[curr_offset:])
        return re.compile(result_string)

    @staticmethod
    def _sub_expr_to_pattern(input_string):
        curr_offset = 0
        result_string = ""
        while True:
            dollar_offset = input_string.find("$", curr_offset)
            expr_offset = dollar_offset + 1
            if (dollar_offset < 0) or (expr_offset >= len(input_string)):
                break
            if input_string[expr_offset] == "#":
                result_string += input_string[curr_offset:dollar_offset]
                result_string += "\\"
                curr_offset = expr_offset + 1
            else:
                result_string += input_string[curr_offset:expr_offset]
                curr_offset = expr_offset
                after_escaped_offset = curr_offset + 2
                if (after_escaped_offset <= len(input_string)) and \
                    (input_string[curr_offset:after_escaped_offset] == "$#"):
                    result_string += "#"
                    curr_offset = after_escaped_offset
        result_string += input_string[curr_offset:]
        return result_string

class RegexExprError(Exception):
    pass
