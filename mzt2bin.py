import sys


def main(in_file, out_file):
    with open(in_file, "rb") as fp:
        data = fp.read()
    with open(out_file, "wb") as fp:
        fp.write(data[128:])


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: py -m mzt2bin in-file out-file")
        exit(1)
    try:
        main(*sys.argv[1:])
        exit(0)
    except Exception as e:
        print(e)
        exit(1)
