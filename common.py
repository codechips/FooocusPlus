import os

# These pseudo globals are imported by several
# functions and are subject to change
GRADIO_ROOT = None
MODELS_INFO = None
torch_device = ''

# ROOT is used as a constant that
# is referenced by several modules
ROOT = os.path.dirname(os.path.abspath(__file__))

# Toggle any variable, with optional console msg
def toggle(var_name,var_string):
  var_name = not var_name
  if var_name:
    bool_string = 'Enabled'
  else:
    bool_string = 'Disabled'    
  try:
    print(f'{var_string} is {bool_string}')
  except:
return var_name
