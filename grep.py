import argparse
import encodings
import glob
import os.path
import re
from encodings.aliases import aliases


def main(args):
    pattern = re.compile(args.pattern)
    files = collect_files(args.file)
    args.show_name = len(files) > 1

    for file in files:
        if not os.path.exists(file):
            print(file, "not found")
            continue
        grep(file, pattern, args)


def collect_files(file_args):
    files = []
    for arg in file_args:
        files.extend(glob.glob(arg))
    return files


def grep(file, pattern, option):
    count = 0
    for n, raw_line in enumerate(open(file, encoding=option.encoding), start=1):
        line = raw_line[: len(raw_line) - 1]  # remove \n at the end
        m = pattern.search(line)
        if m is None:
            continue
        if option.count:
            count += 1
            continue
        if option.show_name:
            print(f"{file}:", end="")
        if option.number:
            print(f"{n}:", end="")
        print(line)
    if option.count:
        print(f"{file}:{count}")


ENCODINGS = list(aliases.keys()) + list(aliases.values())


def parse_arguments():
    parser = argparse.ArgumentParser(description="grep - python regexp grep")
    parser.add_argument(
        "-c",
        "--count",
        action="store_true",
        default=False,
        help="count the numbers of lines that includ the pattern",
    )
    parser.add_argument(
        "-n",
        "--number",
        action="store_true",
        default=False,
        help="output the line number",
    )
    parser.add_argument(
        "-e",
        "--encoding",
        metavar="ENCODING",
        default="utf-8",
        help="file encoding, default is utf-8",
    )
    parser.add_argument("pattern", help="regexp pattern")
    parser.add_argument("file", nargs="+", help="file to be grep-ed")
    args = parser.parse_args()
    if encodings.normalize_encoding(args.encoding) not in ENCODINGS:
        print(args.encoding, "invalid encoding")
        exit()
    return args


if __name__ == "__main__":
    args = parse_arguments()
    main(args)
