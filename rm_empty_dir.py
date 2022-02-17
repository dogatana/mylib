import sys
import os
import os.path


def main(dir):
    rm_empty_dir(dir)


def rm_empty_dir(dir):
    paths = [os.path.join(dir, item) for item in os.listdir(dir)]
    if paths == []:
        print("# rmdir ", dir)
        os.rmdir(dir)
        return
    for dir in (path for path in paths if os.path.isdir(path)):
        rm_empty_dir(dir)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: rm_empty_dir dir")
        exit()
    main(sys.argv[1])
