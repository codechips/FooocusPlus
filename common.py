import os

# These pseudo globals are imported by several
# functions and are subject to change
GRADIO_ROOT = None
MODELS_INFO = None
torch_device = ''

# EV_Base is only used by the Extra Variation
# function in async_worker.py
EV_Base = 0

# ROOT is used as a constant that
# is referenced by several modules
ROOT = os.path.dirname(os.path.abspath(__file__))
