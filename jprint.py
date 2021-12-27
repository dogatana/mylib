"""
prity print for json
"""
import json


def main(file):
    hash = read_json(file)
    print(json.dumps(hash, ensure_ascii=False, indent=2))


def read_json(file):
    with open(file, encoding="utf-8") as fp:
        return json.load(fp)


import sys
import os.path

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: jprint file")
        exit()

    file = sys.argv[1]
    if not os.path.exists(file):
        print(file, "not found")
        exit()

    main(file)
