import re
import sys


def main(infile, outfile):
    with open(infile, encoding="utf-8") as fp:
        text = fp.read()

    out_text = fix_text(text)

    with open(outfile, "w", encoding="utf-8") as fp:
        fp.write(out_text)


def fix_text(text):
    # script 削除
    result = re.sub(r"<script>.*?</script>", "", text, flags=re.DOTALL)

    # css をインライン展開
    with open("c:/git/doc/markdown_pdf/markdown-pdf.css", encoding="utf-8") as fp:
        css_text = "\n<style>\n" + fp.read() + "\n</style>\n"

    result = re.sub(r'<link rel.*?text/css">', css_text, result)

    return result


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: python -m insert_css infile outfile")
        exit()

    main(sys.argv[1], sys.argv[2])
