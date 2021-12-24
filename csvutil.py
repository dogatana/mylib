def to_csvline(lst):
    def to_column(v):
        return '"' + str(v).replace('"', '""') + '"'
    return ",".join([to_column(v) for v in lst])
