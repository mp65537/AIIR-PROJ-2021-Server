import re

class BuildRule:
    def __init__(self, rule_pattern, rule_data):
        self._target_re = re.compile(
            type(self)._re_expr_to_pattern(rule_pattern))
        self._command = ""
        self._depends = []

    def match(self, target_name):
        # check if name match rule
        
        pass

    def get_depends(self, target_name):
        pass

    def get_command(self, target_name):
        pass

    @staticmethod
    def _re_expr_to_pattern(input_string):
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
                        raise PatternSyntaxError("Expected ']' after '$[' token")
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
        return result_string

    @staticmethod
    def _re_sub_expr_to_text(input_string):
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
    
    # should be one method taking 
    # target and returning whole 
    # info or None

    # passing some target name
    # evaluating name with regex
    # and checking if pattern matched (saving match)
    # if not return None; if yes go on
    #
    # replacing this patterns:  
    # firs_dep_name         <-  $<   (command)
    # target name           <-  $@   (command)
    # regex group match     <-  $#N  (command and depends)
    # returning {"name": target_name, 
    #   deps: [..], command: "<replaced_string>"}

def get_build_rules(build_data):
    build_vars = build_data["variables"]

    pass



class PatternSyntaxError(Exception):
    pass


# list of build rules


#RESULT OF WHOLE PARSING: build_env, shell, build_rules list, artifact path list