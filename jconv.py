ZENKAKU = "\u3000" + "".join(chr(0xFF01 + i) for i in range(94))
HANKAKU = " " + "".join(chr(0x21 + i) for i in range(94))

ZEN2HAN = str.maketrans(ZENKAKU, HANKAKU)
HAN2ZEN = str.maketrans(HANKAKU, ZENKAKU)


def zen2han(s):
    return s.translate(ZEN2HAN)


def han2zen(s):
    return s.translate(HAN2ZEN)


if __name__ == "__main__":
    import sys

    for arg in sys.argv[1:]:
        print("zen2han:", zen2han(arg))
        print("han2zen:", han2zen(arg))
