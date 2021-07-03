import sys
import os
import os.path
import glob

def get_paths():
    return os.environ['PATH'].split(";")

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


