import os
from pathlib import Path

def get_home_directory():
    return str(Path.home())

def get_current_directory():
    return os.getcwd()
