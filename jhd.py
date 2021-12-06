
def main(file, encoding):

    data = open(file, "rb").read()

    start = 0
    pre = ""
    skip = 0
    for ofs in range(start, len(data), 16):
        if ofs >= len(data):
            break
        hex = dump(data[ofs: ofs + 16])
        block = data[ofs + skip: (ofs + 20)]
        print(f"{ofs:08x}: {hex}  |", end="")
        s, skip = convert(block, 16 - skip, encoding)
        if s.startswith("# error"):
            print(skip, s)
            break
        print(pre + s)
        pre = " " * skip


def dump(bstr):
   text =  " ".join("%02x" % c for c in bstr)
   if len(bstr) < 16:
       text = text + "   " * (16 - len(bstr))
   text = text[:23] + " " + text[23:]
   return text

def convert(bstr, row_len, encoding):
    src = bytearray((0x2e if b < 0x20 or b == 0x7f else b for b in bstr))
    size = row_len
    added = 0
    while True:
        try:
            return src[:size + added].decode(encoding), added
        except UnicodeDecodeError as e:
            if "invalid start" in e.reason:
                src[e.start] = 0x2e # "."
                continue
            if "unexpected end" in e.reason and len(src) > (size + added):
                src.append(src[size + added])
                added += 1
                continue
            if "invalid continuation" in e.reason:
                for pos in range(e.start, e.end):
                    src[pos] = 0x2e
                continue
            if "incomplete multibyte" in e.reason and len(src) > (size + added):
                src.append(src[size + added])
                added += 1
                continue
            if "illegal multibyte" in e.reason:
                src[e.start] = 0x2e # "."
                continue

            return f"# error {e}", added

import sys
import os.path
if __name__ == "__main__":
    def usage():
        print("usage: python -m jhd [-s] [-u] file")
        exit()

    encoding = "utf-8"
    args = sys.argv[1:]
    if "-s" in args:
        encoding = "cp932"
        args.remove("-s")
    if "-u" in args:
        encoding = "utf-8"
        args.remove("-u")
    if len(args) != 1:
        usage()

    file = args[0]
    if not os.path.exists(file):
        print(file, "not found")
        exit()

    main(file, encoding)

