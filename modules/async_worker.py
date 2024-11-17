import os


os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"


from modules.router import create_app
from modules.download import *

