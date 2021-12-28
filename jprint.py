"""
prity print for json
"""
import json
import yaml
import os.path
import argparse


def main(args):
    ext = os.path.splitext(args.file)[-1].lower()
    if args.json or ext == ".json":
        obj = load_json(args.file)
    elif args.yaml or ext == ".yml":
        obj = load_yaml(args.file)
    else:
        print(args.file, "unexpected file")
        exit()
    if obj is not None:
        print(json.dumps(obj, indent=args.indent, ensure_ascii=False))


def load_json(file):
    try:
        with open(file, encoding="utf-8") as fp:
            return json.load(fp)
    except Exception as e:
        print("*** json parse error")
        print(e)
        return None



def load_yaml(file):
    try:
        with open(file, "rb") as fp:
            return yaml.safe_load(fp)
    except Exception as e:
        print("*** yaml parse error")
        print(e)
        return None


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="jprint - pretty print for json and yaml"
    )
    parser.add_argument("-y", "--yaml", help="force yaml", action="store_true")
    parser.add_argument("-j", "--json", help="force json", action="store_true")
    parser.add_argument("-i", "--indent", help="indent leve, default is 4", type=int, default=4)
    parser.add_argument("file", help="file to print")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    main(args)
