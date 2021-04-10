import reader #from . import reader
import expand #from . import expand # chack local import

file_data = reader.dict
out_data = expand.expand_config_tree(file_data)
print("done!!!")