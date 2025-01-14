import os.path
import re
from argparse import ArgumentParser


def main(args):
    infile = args.in_html
    outfile = args.out_html
    with open(infile, encoding="utf-8") as fp:
        text = fp.read()

    if args.script:
        text = remove_script(text)

    if args.css:
        text = insert_css(text)

    with open(outfile, "w", encoding="utf-8") as fp:
        fp.write(text)


def remove_script(text):
    # script 削除
    return re.sub(r"<script>.*?</script>", "", text, flags=re.DOTALL)


def insert_css(text):
    # css をインライン展開
    with open("c:/git/doc/markdown_pdf/markdown-pdf.css", encoding="utf-8") as fp:
        css_text = "\n<style>\n" + fp.read() + "\n</style>\n"

    return re.sub(r'<link rel.*?text/css">', css_text, text)


def parse_args():
    parser = ArgumentParser(description="remove css and/or javaScript")
    parser.add_argument(
        "-s", "--script", action="store_true", default=False, help="remove JavaScript"
    )
    parser.add_argument(
        "-c",
        "--css",
        action="store_true",
        default=False,
        help="insert a local css file",
    )
    parser.add_argument("in_html")
    parser.add_argument("out_html")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if not args.css and not args.script:
        print("There's nothing to do")
        exit()
    if not os.path.exists(args.in_html):
        print(args.in_html, "not found")
        exit()
    main(args)
