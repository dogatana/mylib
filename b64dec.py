import base64
import os.path
import sys


def main(in_file, out_file):
    if not os.path.exists(in_file):
        print(in_file, "not found", file=sys.stderr)
        return
    elif not os.path.isfile(in_file):
        print(in_file, "not  a file", file=sys.stderr)
        return

    text = open(in_file, "rb").read()
    open(out_file, "wb").write(base64.b64decode(text))


def usage():
    print("usage: python -m b64dec in_file out_file")
    exit()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        usage()
    elif len(sys.argv) == 3:
        main(*sys.argv[1:3])
    else:
        usage()
