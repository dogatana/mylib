import sys
import os.path
import base64

import lxml.html

def main(in_html, out_html):
    doc = lxml.html.parse(in_html)
    for img in doc.xpath("//img"):
        src = img.attrib["src"]
        if src.startswith("http://") or src.startswith("https://"):
            continue
        new_src = replace_src(in_html, src)
        img.attrib["src"] = new_src
    doc.write(out_html, encoding="utf-8")

def replace_src(file, src):
    dir = os.path.dirname(file)
    img_path = os.path.join(dir, src)
    if not os.path.exists(img_path):
        raise FileNotFoundError(img_path)
    img_type = define_type(src)
    text = encode(img_path)
    new_src = f"data:{img_type};base64," + text
    print("#", new_src[:60], "...")
    return new_src

def define_type(src):
    ext = os.path.splitext(src)[1].lower()
    if ext == ".png":
        return "image/png"
    elif ext == ".jpg" or ext == ".jpeg":
        return "image/jpeg"
    elif ext == ".png":
        return "image/gif"
    else:
        raise ValueError("unknown type: "+ src)

def encode(img_file):
    img = open(img_file, "rb").read()
    return base64.b64encode(img).decode("ascii")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: python -m embed_iage im_html out_html")
        exit()

    in_html, out_html = sys.argv[1:3]
    if not os.path.exists(in_html):
        print(in_html, "not found")
        exit()

    main(in_html, out_html)
