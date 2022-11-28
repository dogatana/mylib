import glob
import os
import os.path
import sys


def get_paths():
    paths = []
    for env in ["PATH", "PYTHONPATH"]:
        paths.extend(p for p in os.environ[env].split(";") if p.strip() != "")
    return paths


def which(paths, arg):
    if has_ext(arg):
        scan_paths(paths, arg)
    else:
        scan_paths(paths, arg + ".*")


def scan_paths(paths, name):
    for path in paths:
        for file in glob.glob(os.path.join(path, name)):
            print(file)


def has_ext(path):
    return os.path.splitext(os.path.basename(path))[1]


if __name__ == "__main__":
    paths = get_paths()
    for arg in sys.argv[1:]:
        which(paths, arg)
