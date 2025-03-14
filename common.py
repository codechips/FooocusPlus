import os

# These pseudo globals are imported by several
# functions and are subject to change
GRADIO_ROOT = None
MODELS_INFO = None
torch_device = ''

# ROOT is used as a constant that
# is referenced by several modules
ROOT = os.path.dirname(os.path.abspath(__file__))

# Instead of disturbing the list exchange from webui
# to async_worker, do it the basic way
extra_variation = False
