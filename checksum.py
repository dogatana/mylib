import sys
from argparse import ArgumentParser, ArgumentTypeError


def main(args):
    ofs = args.offset
    with open(args.FILE, "rb") as fp:
        while True:
            block = fp.read(256)
            if block == b"":
                break
            dump(ofs, block)
            ofs += 256


def dump(addr, data):
    data = (data + b"0" * 255)[:256]

    column_sum = [0] * 16
    print("ADDR:", " ".join(f"+{n:X}" for n in range(16)))
    for y in range(16):
        print(f"{addr + y * 16:04X}: ", end="")
        ofs = y * 16
        line_sum = 0
        for x in range(16):
            b = data[ofs + x]
            print(f"{b:02X}", end=" ")
            line_sum += b
            column_sum[x] += b
        print(f":{line_sum & 0xff:02X}")
    print("-" * 57)
    print(
        "SUM :",
        " ".join([f"{column_sum[x] & 0xff:02X}" for x in range(16)]),
        f":{sum(column_sum) & 0xff:02X}",
    )
    print("")


def type_int(arg):
    try:
        return int(arg, 0)
    except Exception:
        raise ArgumentTypeError(f"invalid type {arg}")


def parse_args(argv):
    parser = ArgumentParser("checksum", description="hex dump with checksum")
    parser.add_argument(
        "--offset", "-o", type=type_int, default=0, help="address offset"
    )
    parser.add_argument("FILE", help="target file")
    return parser.parse_args(argv)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(args)
