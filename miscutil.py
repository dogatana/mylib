import io
import sys
from glob import glob


def expand_files(args):
    files = []
    for arg in args:
        files.extend(glob(arg))
    return files


def stdout_utf8(enable=True):
    encoding = "utf-8" if enable else "cp932"
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding=encoding)
