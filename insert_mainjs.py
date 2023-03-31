""" main.js を main.min.js の内容で置き換える """

from argparse import ArgumentParser
import re


def main(in_html, in_js, out_html):
    in_text = read_file(in_html)
    js_text = read_file(in_js).replace("\\", "\\\\")
    # out_text = in_text.replace(
    #     '<script src="main.js"></script>', f"<script>{js_text}</script>"
    # )
    out_text = re.sub(r'<script src="main[0-9]*.js"></script>', f"<script>{js_text}</script>", in_text)
    write_file(out_html, out_text)


def read_file(file):
    with open(file, encoding="utf-8") as fp:
        return fp.read()


def write_file(file, text):
    with open(file, "w", encoding="utf-8") as fp:
        fp.write(text)


def parse_args():
    parser = ArgumentParser(description="insert main(.min).js to html")
    parser.add_argument("in_html", help="input html")
    parser.add_argument("in_js", help="input js")
    parser.add_argument("out_html", help="output html")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(args.in_html, args.in_js, args.out_html)
