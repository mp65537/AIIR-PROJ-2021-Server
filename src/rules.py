class BuildRule:
    def __init__(self):
        self._command = ""
        self._depends = []

    def match(target_name):
        # check if name match rule
        pass

    def get_depends(target_name):
        pass

    def get_command(target_name):
        pass

    # should be one method taking 
    # target and returning whole 
    # info or None

    # passing some target name
    # evaluating name with regex
    # and checking if pattern matched (saving match)
    # if not return None; if yes go on
    #
    # replacing this patterns:  
    # firs_dep_name         <-  $< 
    # target name           <-  $@  
    # regex group match     <-  $#N
    # returning {"name": target_name, 
    #   deps: [..], command: "<replaced_string>"}

def get_build_rules(build_data):
    build_vars = build_data["variables"]

    pass



# list of build rules


#RESULT OF WHOLE PARSING: build_env, shell, build_rules list, artifact path list