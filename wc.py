import glob
import os
import sys

def main(args):
    fmt = "{:14,}{:14,} {}"
    total_line = total_byte = 0
    count = 0
    for arg in args:
        for file in glob.glob(arg):
            line, byte = wc(file)
            print(fmt.format(line, byte, file))
            total_line += line
            total_byte += byte
            count += 1
    if count > 1:
        print(fmt.format(total_line, total_byte, f"total({count}files)"))

def wc(file):
    size = os.stat(file).st_size
    with open(file, "rb") as fp:
        text = fp.read()
        return text.count(b"\n"), size

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("usage: python -m wc file [file..]")
        exit()
    try:
        main(sys.argv[1:])
    except BrokenPipeError:
        pass


