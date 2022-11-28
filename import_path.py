import os.path
import re
import sys


def search(file):
    if not re.search(r"\.py$", file, flags=re.IGNORECASE):
        file += ".py"
    candidates = [os.path.join(dir, file) for dir in sys.path]
    results = [path for path in candidates if os.path.exists(path)]
    for path in results:
        print(path)


def usage():
    print("usage: python import_path.py name [name..]")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        usage()
    for arg in sys.argv[1:]:
        search(arg)
