import os.path
from glob import glob

import geoip2.database

_reader = None


def get_city(addr):
    return _get_reader().city(addr)


def _get_reader():
    global _reader

    if _reader is not None:
        return _reader

    path = os.path.join(os.path.dirname(__file__), "GeoLite2-City*", "*.mmdb")
    file = sorted(glob(path))[-1]
    _reader = geoip2.database.Reader(file)

    return _reader
