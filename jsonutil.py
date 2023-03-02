import json
from datetime import datetime


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


def to_json(obj, indent=None):
    return json.dumps(obj, ensure_ascii=False, indent=indent, default=_default_encoder)


def _default_encoder(obj):
    if isinstance(obj, datetime):
        return str(obj)
    raise TypeError(f"{obj} is not serializable")
