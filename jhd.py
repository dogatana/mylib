"""jhd - Japanese Hexadecimal Dump"""

import argparse
import io
import os.path
import sys


def main(file, encoding, offset, length):
    setup_stdout_encoding()

    data = open(file, "rb").read()
    if offset >= len(data):
        print("offset exceeds the end of the file")
        exit()
    if length == 0:
        length = len(data)

    start = offset
    pre = ""
    skip = 0
    for ofs in range(start, start + length, 16):  # noqa: E203
        if ofs >= len(data):
            break

        hex_text = hex_dump(data[ofs : ofs + 16])  # noqa: E203
        print(f"{ofs:08x}: {hex_text}  |", end="")

        # utf-8 の 4バイト分を追加して文字列化
        block = data[ofs + skip : (ofs + 20)]  # noqa: E203
        ascii_text, skip = bin_to_ascii(block, 16 - skip, encoding)
        if ascii_text.startswith("# error"):
            print("\n", ascii_text)
            exit()
        print(pre + ascii_text)
        pre = "_" * skip


def setup_stdout_encoding():
    # 標準出力が端末でない場合、エンコーディングを utf-8 にする
    if not sys.stdout.isatty():
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def hex_dump(block):
    text = " ".join("%02x" % c for c in block)
    # 16 バイトに満たない場合は空白を追加
    if len(block) < 16:
        text = text + "   " * (16 - len(block))
    # 8バイト目の後に空白追加
    return text[:23] + " " + text[23:]


def bin_to_ascii(block, row_len, encoding):
    def isctrl(c):
        # 制御文字
        return c < 0x20 or c == 0x7F

    if encoding == "ascii":
        src = ""
        for c in block:
            if c < 0x20 or c >= 0x7F:
                src += "."
            else:
                src += chr(c)
        return src, 0

    src = bytearray((0x2E if isctrl(b) else b for b in block))
    size = row_len
    added = 0
    while True:
        try:
            return src[: size + added].decode(encoding), added
        except UnicodeDecodeError as e:
            # utf-8
            if "invalid start" in e.reason:
                src[e.start] = 0x2E  # "."
                continue
            elif "unexpected end" in e.reason and len(src) > (size + added):
                src.append(src[size + added])
                added += 1
                continue
            elif "invalid continuation" in e.reason:
                for pos in range(e.start, e.end):
                    src[pos] = 0x2E
                continue

            # shift_jis
            if "incomplete multibyte" in e.reason and len(src) > (size + added):
                src.append(src[size + added])
                added += 1
                continue
            elif "illegal multibyte" in e.reason:
                src[e.start] = 0x2E  # "."
                continue

            return f"# error {e}", added


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="jhd - Hexadecimal Dump with decoded Japanese string"
    )
    parser.set_defaults(encoding="ascii")
    parser.add_argument(
        "-s",
        "--shift_jis",
        dest="encoding",
        action="store_const",
        const="shift_jis",
        help="assume FILE's encoding is Shift_JIS",
    )
    parser.add_argument(
        "-u",
        "--utf-8",
        dest="encoding",
        action="store_const",
        const="utf-8",
        help="assume FILE's encoding is UTF-8 (default)",
    )
    parser.add_argument(
        "-a",
        "--ascii",
        dest="encoding",
        action="store_const",
        const="ascii",
        help="assume FILE's encoding is ascii",
    )
    parser.add_argument(
        "-o", "--offset", help="offset to start", default=0, type=lambda n: int(n, 0)
    )
    parser.add_argument(
        "-l", "--length", help="length", default=0, type=lambda n: int(n, 0)
    )

    parser.add_argument("file", metavar="FILE", help="file to dump")

    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(args.file, "not found")
        exit()

    return args


if __name__ == "__main__":
    args = parse_arguments()
    print(args)

    try:
        main(args.file, args.encoding, args.offset, args.length)
    except BrokenPipeError:
        pass
