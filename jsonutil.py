import json


def load_json(file, encoding="utf-8"):
    with open(file, encoding=encoding) as fp:
        return json.load(fp)


def dump_json(obj, file, encoding="utf-8", ensure_ascii=False, indent=2):
    if indent is None:
        sep = (",", ":")
    else:
        sep = (",", ": ")
    with open(file, "w", encoding=encoding) as fp:
        return json.dump(
            obj, fp, ensure_ascii=ensure_ascii, indent=indent, separators=sep
        )
