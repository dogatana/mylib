""" json.load 時に attrdict.AttrDict 相当のオブジェクトとする

    Quiita のものを修正・追加
    https://qiita.com/icoxfog417/items/83a77a648b71a38a1bd5
    Python dictに対しAttributeでアクセスできるようにする - Qiita

    注意：json エンコードは不可。エンコードが必要な場合は attrdict を使用する

    >>> import json
    >>> data = '{ "number": 1, "nested": { "string": "hello" }}'
    >>> att = json.loads(data, object_hook=AttributeDict)
    >>> att.number
    1
    >>> att.number = 2
    >>> att.number
    2
    >>> att.nested.string
    'hello'

"""


class AttributeDict(object):
    def __init__(self, obj):
        self.obj = obj

    def __getstate__(self):
        return self.obj.items()

    def __setstate__(self, items):
        if not hasattr(self, "obj"):
            self.obj = {}
        for key, val in items:
            self.obj[key] = val

    def __getattr__(self, name):
        if name in self.obj:
            return self.obj.get(name)
        else:
            return None

    # def fields(self):
    #     return self.obj

    def __contains__(self, key):
        return key in self.obj

    def __repr__(self):
        return f"AttributeDict( {self.obj} )"

    def items(self):
        return self.obj.items()

    def values(self):
        return self.obj.values()

    def keys(self):
        return self.obj.keys()


if __name__ == "__main__":
    import doctest

    doctest.testmod()
