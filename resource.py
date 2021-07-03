import sys
import os.path


def get_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)
