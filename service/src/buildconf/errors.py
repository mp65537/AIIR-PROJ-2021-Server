class BuildConfError(Exception):
    pass

class ExpandError(BuildConfError):
    pass

class RuleError(BuildConfError):
    pass

class NoSectionError(BuildConfError):
    pass
